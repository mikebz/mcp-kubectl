import asyncio
import pytest
from kubernetes import config
from generate import create_lister
from kube import add_tools, mcp

config.load_kube_config("~/.kube/config")

@pytest.mark.asyncio
async def test_get_namespaces():
    """Test the get_namespaces function."""

    method = create_lister( "list_namespace")
    # Ensure the function is callable
    assert callable(method), "The method should be callable"
    # Call the method to ensure it works correctly
    # Call the function
    namespaces = await method()

    # Check that the function returns a list
    assert isinstance(namespaces, list)
    assert len(namespaces) > 0

def test_add_tools():
    """Test adding MCP tools by calling add_tools() and then
    checking that those actually exist."""
    add_tools()
    assert len(mcp._tool_manager._tools) > 0
    assert "list_namespace" in mcp._tool_manager._tools
