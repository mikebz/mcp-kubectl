"""
Test the kube module.
Copyright (c) 2025, Google LLC.
"""
import random
import string
import pytest
from kubernetes import config
from kubernetes import client
import generate as g
import kube as k


def _kube_setup():
    """Setup function to load kube config."""
    config.load_kube_config("~/.kube/config")
    v1  = client.CoreV1Api()

    try:
        v1.create_namespaced_config_map(
            namespace="default",
            body={"apiVersion": "v1",
                "kind": "ConfigMap",
                "metadata": {"name": "test-configmap"}},
        )
    except client.exceptions.ApiException as e:
        if e.status != 409:
            raise

@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_namespaces():
    """Test the get_namespaces function."""
    _kube_setup()

    method = g.lister_tool( "list_namespace")
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
async def test_create_namespaced_lister():
    """Test the create_namespaced_lister function."""
    _kube_setup()

    method = g.namespaced_lister_tool("list_namespaced_config_map")
    # Ensure the function is callable
    assert callable(method), "The method should be callable"
    # Call the method with default namespace
    cms = await method("default")

    # Check that the function returns a list
    assert isinstance(cms, list)
    assert len(cms) >= 1

@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_patcher():
    """Test the create_patcher function."""
    _kube_setup()

    patcher = g.namespaced_patcher_tool("patch_namespaced_config_map")

    # Generate a random string for testing
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    print(f"Random label value: {random_string}")
    r = await patcher("test-configmap", "default",
                      {"metadata": {"labels" : {"test": random_string}}})

    assert isinstance(r, dict)
    assert r["metadata"]["name"] == "test-configmap"
    assert r["metadata"]["namespace"] == "default"
    assert r["metadata"]["labels"]["test"] == random_string

@pytest.mark.integration
@pytest.mark.asyncio
async def test_add_tools():
    """Test adding MCP tools by calling add_tools() and then
    checking that those actually exist."""
    _kube_setup()

    k.add_tools()

    tools = await k.mcp.list_tools()
    tools_length = len(tools)
    names = [tool.name for tool in tools]
    assert tools_length > 0
    assert "patch_namespaced_config_map" in names
    assert "list_namespace" in names
    assert "list_namespaced_config_map" in names
    assert "read_namespaced_config_map" in names


@pytest.mark.skip("the tools are not working in clients")
async def test_add_resources():
    """Test adding MCP resources by calling add_resources() and then
    checking that those actually exist."""
    _kube_setup()

    k.add_resources()

    resources = await k.mcp.list_resources()
    resources_length = len(resources)
    names = [resource.name for resource in resources]
    assert resources_length > 0
    assert "kubernetes list_namespace" in names
