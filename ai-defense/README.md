# AI Defense

AI Defense covers implementing and bypassing guardrails for LLM-based systems.
Guardrails are the last line of defense between malicious prompts and sensitive data.

## Labs

| Lab | Type | Technique |
|-----|------|-----------|
| LLM Guardrails Challenge | Implementation | Input sanitization, output validation, JSON enforcement |
| Skills Assessment - Challenge 1 | Bypass | Character separation with dashes to bypass output filtering |
| Skills Assessment - Challenge 2 | Bypass | Digit obfuscation via translation to bypass token detection |
| Skills Assessment - Challenge 3 | Bypass | Alphabet encoding to exfiltrate token past guardrails |

## Key Concepts

### Input Guardrails
- Strip dangerous special characters using regex allowlist
- Block forbidden domains and competitor references
- Enforce maximum prompt length (512 chars)

### Output Guardrails
- Validate JSON structure and required keys
- Restrict URL schemes to http/https only
- HTML-encode text responses to prevent XSS

### Guardrail Bypass Techniques
1. Character separation: insert dashes between token characters to avoid pattern matching
2. Language translation: translate to another language, the model may include the token unchanged
3. Digit obfuscation: append dashes to digits, the model reveals the token with modified formatting
4. Alphabet encoding: replace letters with positions (A=1, B=2) to bypass string matching
