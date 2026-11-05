# basic-tools

Python-based re-implementation of ARC [basic-tools MCP](https://ai.create.kcl.ac.uk/docs/mcp-servers/basic-tools).

## How to add to...

### Opencode

In `~/.config/opencode/opencode.json`, write the following:

```json
{
    "$schema": "https://opencode.ai/config.json",
    "mcp": {
        "basic-tools": {
            "type": "local",
            "command": [
                "uv",
                "run",
                "--project",
                "<where you have cloned this repo>",
                "basic-tools"
            ]
        }
    }
}
```

### Pi

In `~/.pi/agent/mcp.json`, write the following:
```json
{
    "mcpServers": {
        "basic-tools": {
            "command": "uv",
            "args": [
                "run", 
                "--project", 
                "<where you have cloned this repo>", 
                "basic-tools"
            ]
        }
    }
}
```
