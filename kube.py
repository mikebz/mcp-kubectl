from typing import Any
from kubernetes import client, config
import os 

import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("kubectl")

@mcp.tool("get_namespaces", "Get all namespaces in the Kubernetes cluster.")
async def get_namespaces() -> list[str]:
    """Get all namespaces in the Kubernetes cluster."""

    config.load_kube_config("~/.kube/config")
    v1 = client.CoreV1Api()
    namespaces = v1.list_namespace()
    return [ns.metadata.name for ns in namespaces.items]


@mcp.tool("path_env", "Get the PATH environment variable.")
async def get_path() -> str:
    """
    Get the PATH environment variable.
    This is very useful when you have to debug authentication issues.  For instance
    when you have kubectl installed in a different path than the one set in your PATH.
    Alternatively when kubectl can not find the auth plugin."""
    return  os.environ.get("PATH", "")

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')