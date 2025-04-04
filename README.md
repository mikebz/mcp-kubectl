# mcp-kubectl

This project provides a set of tools for interacting with Kubernetes clusters, exposed as a service via the MCP (Microservice Control Plane) framework.

## Features

NOTE: these are always expanding

-   **Get Namespaces:** Retrieve a list of all namespaces in the connected Kubernetes cluster.
-   **Get PATH:** Retrieve the current system's PATH environment variable, useful for debugging `kubectl` configuration and authentication issues.

## Prerequisites

-   Python 3.11
-   uv https://docs.astral.sh/uv/

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

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
