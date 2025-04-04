"""
Module for generating Kubernetes API functions dynamically.
Copyright (c) 2025, Google LLC.
"""
from __future__ import annotations

import inspect
import re
from typing import Any, Callable

from kubernetes import client

def list_k8s_function(regex_pattern: str, nparams: int | None = None) -> list[str]:
    """
    List all functions in client.CoreV1Api that match a given regex pattern.

    Args:
        regex_pattern: The regex pattern to match against function names.
        nparams: Optional number of parameters to filter by.

    Returns:
        A list of function names that match the regex pattern.
    """
    if nparams is None:
        nparams = 0

    api_class = client.CoreV1Api
    matching_functions: list[str] = []
    for name in dir(api_class):
        attr = getattr(api_class, name)

        if callable(attr) and re.match(regex_pattern, name):
            if num_params(attr) == nparams:
                matching_functions.append(name)
    return matching_functions

def num_params(method: Callable[..., Any]) -> int:
    """
    Calculate the number of required positional parameters for a given method.

    Args:
        method: The method or function to analyze.

    Returns:
        The number of required positional parameters.
    """
    sig = inspect.signature(method)
    return sum(
        1 for param in sig.parameters.values()
        if param.name != "self"
        and param.default is param.empty
        and param.kind in (param.POSITIONAL_OR_KEYWORD, param.POSITIONAL_ONLY)
    )

def create_lister(method_name: str) -> Callable[[], list[str]]:
    """
    Create a lister function for a specific Kubernetes resource.

    Args:
        method_name: The method name to call on the CoreV1Api client.

    Returns:
        An async function that lists the specified resource.
    """
    async def lister() -> list[str]:
        """List the specified Kubernetes resource."""
        v1 = client.CoreV1Api()
        method = getattr(v1, method_name)
        items = method()
        return [item.metadata.name for item in items.items]

    return lister


def create_namespaced_lister(method_name: str) -> Callable[[str], list[str]]:
    """
    Create a namespaced lister function for a specific Kubernetes resource.

    Args:
        name: The method name to call on the CoreV1Api client.

    Returns:
        An async function that lists the specified resource in a namespace.
    """
    async def namespaced_lister(namespace: str) -> list[str]:
        """List the specified Kubernetes resource in a namespace."""
        v1 = client.CoreV1Api()
        method = getattr(v1, method_name)
        items = method(namespace)
        return [item.metadata.name for item in items.items]

    return namespaced_lister


def create_reader(method_name: str) -> Callable[[str, str], dict]:
    """
    Create a getter function for a specific Kubernetes resource.

    Args:
        name: The method name to call on the CoreV1Api client.

    Returns:
        An async function that gets the specified resource.
    """
    async def reader(name: str, namespace: str) -> dict:
        """Get the specified Kubernetes resource."""
        v1 = client.CoreV1Api()
        method = getattr(v1, method_name)
        obj = method(name,namespace)
        return obj.to_dict()

    return reader

def create_patcher(method_name: str) -> Callable:
    """
    Create a patcher function for a specific Kubernetes resource.

    Args:
        name: The method name to call on the CoreV1Api client.

    Returns:
        An async function that patches the specified resource.
    """
    async def patcher(name: str, namespace: str, body: dict) -> dict:
        """Patch the specified Kubernetes resource."""
        v1 = client.CoreV1Api()
        method = getattr(v1, method_name)
        obj = method(name,namespace,body)
        return obj.to_dict()

    return patcher
