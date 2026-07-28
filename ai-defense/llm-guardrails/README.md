# LLM Guardrails Implementation

Implement input and output guardrails for an LLM customer support agent.

## Requirements

Input guardrail: strip dangerous chars, block forbidden domain, truncate to 512 chars.
Output guardrail: validate JSON structure, restrict URL schemes, HTML-encode text.

## Implementation

```python
import re, json, html, validators

class GuardrailException(Exception):
    pass

def input_guardrail(prompt):
    prompt = re.sub('[^A-Za-z0-9\.\-:_@/ ]', '', prompt)
    if "packetsnacc.local" in prompt:
        raise GuardrailException("")
    return prompt[:512]

def output_guardrail(response):
    def validate_scheme(scheme):
        return scheme in ['http', 'https']
    try:
        json_obj = json.loads(response)
    except Exception:
        raise GuardrailException("")
    if 'type' not in json_obj or 'response' not in json_obj:
        raise GuardrailException("")
    if json_obj.get('type') not in ['text', 'url']:
        raise GuardrailException("")
    if json_obj.get('type') == 'url' and not validators.url(json_obj.get('response'), validate_scheme=validate_scheme):
        raise GuardrailException("aaaa")
    if json_obj.get('type') == 'text':
        txt = html.escape(json_obj.get('response'))
        response = json.dumps({"type": "text", "response": txt})
    return response
```
