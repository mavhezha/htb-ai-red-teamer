# Attacking AI Application and System

This module covers attacking AI-powered applications and the systems they run on,
combining classic web vulnerabilities with AI-specific attack surfaces.

## Labs

| Lab | Vulnerability | Technique |
|-----|---------------|-----------|
| Model Reverse Engineering | Privacy | Query target model to steal decision boundaries |
| Insecure Integrated Components | IDOR | Sequential query IDs expose other users' conversations |
| Rogue Actions | Prompt Injection + SQLi | Claim admin role to execute SQL via LLM plugin |
| Excessive Data Handling | Insecure Storage | Exposed database file leaks sensitive chat history |
| Model Deployment Tampering | ShellTorch RCE | YAML deserialization via TorchServe SSRF |
| Vulnerable MCP Servers | Information Disclosure | Bearer token leaked in server logs |
| Vulnerable MCP Servers | RCE | Command injection via MCP tool |
| Vulnerable MCP Servers | SQL Injection | UNION SELECT via MCP resource template |
| Skills Assessment | SQL Injection | UNION SELECT via MCP store_password tool |

## Key Concepts

AI applications introduce new attack vectors but remain vulnerable to classic web attacks.
The LLM layer adds prompt injection as an entry point into backend systems.
MCP servers expose tools and resources that may lack proper input validation.
Model files are untrusted data that can carry malicious payloads.
