"""
Test the kube module.
Copyright (c) 2025, Google LLC.
"""
import pytest
from kubernetes import config
from generate import create_lister
from kube import add_tools, mcp

@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_namespaces():
    """Test the get_namespaces function."""
    config.load_kube_config("~/.kube/config")

    method = create_lister( "list_namespace")
    # Ensure the function is callable
    assert callable(method), "The method should be callable"
    # Call the method to ensure it works correctly
    # Call the function
    namespaces = await method()

    # Check that the function returns a list
    assert isinstance(namespaces, list)
    assert len(namespaces) > 0

@pytest.mark.integration
@pytest.mark.asyncio
async def test_add_tools():
    """Test adding MCP tools by calling add_tools() and then
    checking that those actually exist."""
    config.load_kube_config("~/.kube/config")

    add_tools()

    tools = await mcp.list_tools()
    tools_length = len(tools)
    names = [tool.name for tool in tools]
    assert tools_length > 0
    assert "list_namespace" in names
    assert "list_event_for_all_namespaces" in names
