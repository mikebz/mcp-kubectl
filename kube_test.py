"""
Test the kube module.
Copyright (c) 2025, Google LLC.
"""
import os
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
        # NOTE: if you are creating test objects
        # that are not config maps or services
        # in the default namespace, you will need to
        # change this clean up code.
        v1.delete_collection_namespaced_config_map(
            namespace="default",
            label_selector="env=test",
            body=client.V1DeleteOptions(
                propagation_policy="Foreground",
                grace_period_seconds=5,
            ),
        )

        v1.delete_collection_namespaced_service(
            namespace="default",
            label_selector="env=test",
            body=client.V1DeleteOptions(
                propagation_policy="Foreground",
                grace_period_seconds=5,
            ),
        )

        v1.create_namespaced_config_map(
            namespace="default",
            body={"apiVersion": "v1",
                "kind": "ConfigMap",
                "metadata": {"name": "test-configmap",
                             "labels": {"env": "test"}}},
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

@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_from_yaml():
    """Test the create_from_yaml function."""
    _kube_setup()

    # Get the directory containing the test file
    test_dir = os.path.dirname(__file__)
    # Construct the full path to the YAML file
    yaml_path = os.path.join(test_dir, "test_data", "two_resources.yaml")

    # Load the YAML content from the file
    with open(yaml_path, 'r', encoding='utf-8') as f:
        # Use safe_load for single YAML document or safe_load_all for multiple
        yaml_data = f.read()

    # Call the create_from_yaml function
    result = await k.create_from_yaml("default", yaml_data)

    # Check that the result is a dictionary
    assert isinstance(result, list)
    # Check that the result contains the expected keys
    assert len(result) == 2
    obj1 = result[0]
    assert "api_version" in obj1
    assert "kind" in obj1
    assert "metadata" in obj1
    assert "name" in obj1["metadata"]
    assert obj1["metadata"]["name"] == "t2"

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
