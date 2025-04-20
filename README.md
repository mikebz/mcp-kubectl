# mcp-kubectl
A simple implementation of the Model Context Protocol for kubectl operations in Kubernetes environments. This tool allows AI assistants like Claude to interact directly with your Kubernetes clusters to perform operations and gather information.

## Features

- Execute kubernetes commands directly through an AI assistant
- Get information about pods, services, deployments and other Kubernetes resources
- Update resources using natural language instructions

## Prerequisites

-   Python 3.11
-   uv https://docs.astral.sh/uv/
-   authentication to your cluster (I only tested with gcloud and kubectl)

## Installation

1.  Clone the repository:

```bash
git clone <repository_url>
cd mcp-kubectl
```

2.  Install the required Python packages:

```bash
uv run kube.py
```

## Usage

1.  Update the MCP config for Caude desktop

Create/edit `~/Library/Application\ Support/Claude/claude_desktop_config.json`

Example file:

```
{
    "mcpServers": {
        "kubectl": {
            "command": "uv",
            "args": [
                "--directory",
                "/Users/mikebz/src/mcp-kubectl",
                "run",
                "kube.py"
            ],
            "env": {
                "PATH": "/Users/mikebz/google-cloud-sdk/bin:/Users/mikebz/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin:/usr/local/go/bin"
            }
        }
    }
}
```
After that you can use Claud Desktop https://claude.ai/download to use the tool

2.  Interact with the server using the MCP inspector.

[tutorial for installing and using the inspector](https://modelcontextprotocol.io/docs/tools/inspector)

```bash
    npx @modelcontextprotocol/inspector \
    uv \
    --directory /Users/mikebz/src/mcp-kubectl \
    run \
    kube.py
```

## Development

-   The main logic is in `kube.py`.
-   The MCP server is initialized and run at the end of `kube.py`.
-   New tools can be added by creating new functions and decorating them with `@mcp.tool`.


### Testing

Testing is done using pytest

```bash
uv run pytest
```

### Linting

Linting is done using pylint

```
uv run pylint $(git ls-files '*.py')
```

You might also find https://code.visualstudio.com/docs/python/linting useful


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
