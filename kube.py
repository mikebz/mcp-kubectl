from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import AsyncIterator
from kubernetes import client, config
import os 
from mcp.server.fastmcp import FastMCP

from generate import create_lister, list_k8s_function

@dataclass
class AppContext:
    """
    if something gets initialied in the app context you can add that here.
    """
    pass

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    print("Loading kube config")
    config.load_kube_config("~/.kube/config")
    add_tools()
    yield AppContext

# Initialize FastMCP server
mcp = FastMCP("kubectl", lifespan=app_lifespan)

@mcp.tool("path_env", "Get the PATH environment variable.")
async def get_path() -> str:
    """
    Get the PATH environment variable.
    This is very useful when you have to debug authentication issues.  For instance
    when you have kubectl installed in a different path than the one set in your PATH.
    Alternatively when kubectl can not find the auth plugin."""
    return  os.environ.get("PATH", "")


def add_tools():
    """Add tools to the FastMCP server."""
    print("Adding tools")
    names = list_k8s_function("^list_.*$(?<!http_info)")

    for name in names:
        method = create_lister(name)
        mcp.add_tool(method, name=name, description=f"kubernetes {name}s")

def main() -> None:
    """Main function to initialize and run the MCP server."""
    print("Starting FastMCP server")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    print("Running kube.py as main")
    main()