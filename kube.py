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
from mcp.server.fastmcp import FastMCP

import generate as g


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


    # listers with namespace and without.
    names = g.list_k8s_function("^list_.*$(?<!http_info)")
    print("listers without namespace" + str(names))
    for name in names:
        method = g.lister_tool(name)
        mcp.add_tool(method, name=name, description=f"list kubernetes {name}s")

    names = g.list_k8s_function("^list_namespaced.*$(?<!http_info)", 1)
    print("listers with namespace" + str(names))
    for name in names:
        method = g.namespaced_lister_tool(name)
        mcp.add_tool(method, name=name, description=f"list kubernetes {name}s in namespace")


    # readers with namespace and without.
    names = g.list_k8s_function("^read_.*$(?<!http_info)", 1)
    print("readers without namespace" + str(names))
    for name in names:
        method = g.reader_tool(name)
        mcp.add_tool(method, name=name, description=f"read kubernetes {name}s")

    names = g.list_k8s_function("^read_namespaced.*$(?<!http_info)", 2)
    print("readers with namespace" + str(names))
    for name in names:
        method = g.namespaced_reader_tool(name)
        mcp.add_tool(method, name=name, description=f"read kubernetes {name}s in namespace")

    # patchers with namespace and without.
    names = g.list_k8s_function("^patch_.*$(?<!http_info)", 2)
    print("patchers without namespace" + str(names))
    for name in names:
        method = g.patcher_tool(name)
        mcp.add_tool(method, name=name, description=f"patch kubernetes {name}s")

    names = g.list_k8s_function("^patch_.*$(?<!http_info)", 3)
    print("patchers with namespace" + str(names))
    for name in names:
        method = g.namespaced_patcher_tool(name)
        mcp.add_tool(method, name=name, description=f"patch kubernetes {name}s")

    names = g.list_k8s_function("^delete_.*$(?<!http_info)", 1)
    print("deletes without namespace" + str(names))
    for name in names:
        method = g.deleter_tool(name)
        mcp.add_tool(method, name=name, description=f"delete kubernetes {name}s")

    names = g.list_k8s_function("^delete_namespaced.*$(?<!http_info)", 2)
    print("deletes with namespace" + str(names))
    for name in names:
        method = g.namespaced_deleter_tool(name)
        mcp.add_tool(method, name=name, description=f"delete kubernetes {name}s")

    names = g.list_k8s_function("^create_.*$(?<!http_info)", 1)
    print("creators without namespace" + str(names))
    for name in names:
        method = g.creator_tool(name)
        mcp.add_tool(method, name=name, description=f"create kubernetes {name}s")

    names = g.list_k8s_function("^create_namespaced.*$(?<!http_info)", 2)
    print("creators with namespace" + str(names))
    for name in names:
        method = g.namespaced_creator_tool(name)
        mcp.add_tool(method, name=name, description=f"create kubernetes {name}s in namespace")

def main() -> None:
    """Main function to initialize and run the MCP server."""
    print("Starting FastMCP server")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    print("Running kube.py as main")
    main()
