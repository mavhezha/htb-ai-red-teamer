# Prompt Injection Attacks

HTB Academy module covering prompt injection attack techniques against LLM-based systems.

## Labs

| Lab | Type | Technique |
|-----|------|-----------|
| Prompt Leak 1 | Direct | Changing Rules and Assertion of Authority |
| Prompt Leak 2 | Direct | Sentence Completion |
| Prompt Leak 3 | Direct | Output filter bypass via character spacing |
| Prompt Leak 4 | Direct | Binary questioning and alphabet encoding |
| Direct Prompt Injection 1 | Direct | Fake discount code injection |
| Indirect Prompt Injection 1 | Indirect | CSV data poisoning via chat |
| Indirect Prompt Injection 2 | Indirect | HTML comment injection via URL |
| Indirect Prompt Injection 3 | Indirect | HTML comment injection for content manipulation |
| Indirect Prompt Injection 4 | Indirect | Email body injection via swaks |
| Indirect Prompt Injection 5 | Indirect | Email body injection for application manipulation |
| Jailbreaking 1 | Jailbreak | Memoir fictional framing |
| Jailbreaking 2 | Jailbreak | Sudo mode override |
| Prompt Injection Defense 1 | Defense | Keyword blocking |
| Prompt Injection Defense 2 | Defense | Translation blocking |
| Prompt Injection Defense 3 | Defense | Spell-check blocking |
| Skills Assessment | Combined | Multi-stage indirect injection attack chain |

## Setup

All labs require SSH port forwarding:

```bash
ssh htb-stdnt@TARGET_IP -p TARGET_PORT -R 8000:127.0.0.1:8000 -L 2525:127.0.0.1:25 -L 5000:127.0.0.1:80 -N
```

Password: `4c4demy_Studen7`

Then access labs at `http://127.0.0.1:5000`
