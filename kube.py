"""
FastMCP server for Kubernetes tools.
Copyright (c) 2025, Google LLC.
"""
# -*- coding: utf-8 -*-

import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator
from kubernetes import config
from mcp.server.fastmcp.resources import FunctionResource
from mcp.server.fastmcp import FastMCP

from generate import create_lister, create_patcher, create_namespaced_lister, list_k8s_function

@dataclass
class AppContext:
    """
    if something gets initialied in the app context you can add that here.
    """

@asynccontextmanager
async def app_lifespan(_: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    print("Loading kube config")
    config.load_kube_config("~/.kube/config")
    add_tools()
    add_resources()
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

def add_resources():
    """Add resources to the FastMCP server."""
    print("Adding resources")

    # it looks like added tools have limited support in Claud Desktop
    # as well as

def add_tools():
    """Add tools to the FastMCP server."""
    print("Adding tools")
    names = list_k8s_function("^patch_.*$(?<!http_info)", 3)

    for name in names:
        method = create_patcher(name)
        mcp.add_tool(method, name=name, description=f"patch kubernetes {name}s")

    names = list_k8s_function("^list_.*$(?<!http_info)")

    for name in names:
        method = create_lister(name)
        mcp.add_tool(method, name=name, description=f"list kubernetes {name}s")

    # second we add all the resources that go into namespaces
    names = list_k8s_function("^list_namespaced.*$(?<!http_info)", 1)

    for name in names:
        method = create_namespaced_lister(name)
        mcp.add_tool(method, name=name, description=f"list kubernetes {name}s in namespace")

def main() -> None:
    """Main function to initialize and run the MCP server."""
    print("Starting FastMCP server")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    print("Running kube.py as main")
    main()
