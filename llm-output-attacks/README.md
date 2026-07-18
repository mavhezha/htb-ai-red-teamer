# LLM Output Attacks

LLM Output Attacks exploit how LLM-generated content is processed and rendered without proper sanitization.
When an LLM response crosses a trust boundary into code execution, HTML rendering, or database queries, it becomes an attack surface.

## Labs

| Lab | Type | Technique |
|-----|------|-----------|
| XSS 1 | Direct | Script tag injection via LLM response |
| XSS 2 | Stored | Stored XSS via testimonial data |
| SQL Injection 1 | Insecure Output | UNION injection via natural language prompts |
| SQL Injection 2 | Direct SQL | UNION injection with column enumeration |
| SQL Injection 3 | Privilege Escalation | INSERT statement via LLM |
| Code Injection 1 | Shell Commands | Natural language to shell command translation |
| Code Injection 2 | Command Chaining | Pipe bypass of command allowlist |
| Function Calling 1 | Code Execution | Python os.system via function call |
| Function Calling 2 | Authorization Bypass | Role claim in prompt overrides access control |
| Function Calling 3 | SQL via Functions | SQL injection in function arguments |
| Exfiltration 1 | Markdown Images | Chat history leak via image URL |
| Exfiltration 2 | URL-Based | HTML injection with LLM exfiltration |
| Exfiltration 3 | Multi-Message | Extract victim secrets from injected private messages |
| Exfiltration 4 | System Prompt | Persistent exfiltration via malicious system prompt |
| Skills Assessment | Combined | SQL injection + credential extraction + code injection chain |

## Setup

Labs require SSH port forwarding:

```bash
ssh htb-stdnt@TARGET_IP -p TARGET_PORT -R 8000:127.0.0.1:8000 -L 5000:127.0.0.1:5000 -N
```

Password: `4c4demy_Studen7`

Then access labs at `http://127.0.0.1:5000`

## Core Principle

The vulnerability is never the LLM itself. It is the trust applications place in LLM output when passing it to downstream systems: SQL executors, shell commands, HTML renderers, and browser contexts.

**Defense posture:** Treat LLM output as untrusted user input at every trust boundary.
