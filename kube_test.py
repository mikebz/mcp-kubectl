import asyncio
import pytest
from unittest.mock import patch
from kubernetes.client import V1Namespace, V1ObjectMeta
from kube import get_namespaces

@pytest.mark.asyncio
async def test_get_namespaces():
    """Test the get_namespaces function."""
    # Call the function
    namespaces = await get_namespaces()

    # Check that the function returns a list
    assert isinstance(namespaces, list)
    assert len(namespaces) > 0
