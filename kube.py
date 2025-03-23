from typing import Any
from kubernetes import client, config

import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("kubectl")

@mcp.tool()
async def get_namespaces() -> list[str]:
    """Get all namespaces in the Kubernetes cluster."""
    config.load_kube_config()
    v1 = client.CoreV1Api()
    namespaces = v1.list_namespace()
    return [ns.metadata.name for ns in namespaces.items]

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')