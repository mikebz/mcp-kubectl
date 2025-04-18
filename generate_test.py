# -*- coding: utf-8 -*-
"""
Test module for the generate module.
Copyright (c) 2025, Google LLC.
"""
import inspect
import generate as g

def test_list_k8s_function_match():
    """Test the list_k8s_function function with a pattern that matches."""
    # Test with a pattern that should match some functions
    matching_functions = g.list_k8s_function(r"^list_.*")
    assert isinstance(matching_functions, list)
    assert len(matching_functions) > 0
    for func_name in matching_functions:
        assert func_name.startswith("list_")

def test_list_k8s_function_no_match():
    """Test the list_k8s_function function with a non-existent pattern."""
    # Test with a pattern that should match no functions
    no_matching_functions = g.list_k8s_function(r"^nonexistent_.*")
    assert isinstance(no_matching_functions, list)
    assert len(no_matching_functions) == 0

def test_list_k8s_function_specific():
    """Test the list_k8s_function function with a specific function name."""
    # Test with a pattern that should match a specific function
    specific_function = g.list_k8s_function(r"^list_namespace$")
    assert isinstance(specific_function, list)
    assert len(specific_function) == 1
    assert specific_function[0] == "list_namespace"


def test_num_params():
    # pylint: disable=unused-argument
    """Test the g.num_params function with different method signatures."""

    def no_params():
        """Test function with no parameters."""
    assert g.num_params(no_params) == 0

    def one_required(x):
        """Test function with one required parameter."""
    assert g.num_params(one_required) == 1

    def mixed_params(a, b, c=None, d=1):
        """Test function with mixed parameters."""
    assert g.num_params(mixed_params) == 2

    def kwargs_only(**kwargs):
        """Test function with kwargs only."""
    assert g.num_params(kwargs_only) == 0

    def complex_signature(a, b, *args, c=None, **kwargs):
        """Test function with complex signature."""
    assert g.num_params(complex_signature) == 2

def test_lister_tool():
    """Test the lister_tool function."""
    lister = g.lister_tool("list_namespace")
    assert callable(lister)
    assert inspect.iscoroutinefunction(lister)


def test_namespaced_lister_tool():
    """Test the namespaced_lister_tool function."""
    namespaced_lister = g.namespaced_lister_tool("list_namespaced_pod")
    assert callable(namespaced_lister)
    assert inspect.iscoroutinefunction(namespaced_lister)


def test_patcher_tool():
    """Test the patcher_tool function."""
    patcher = g.patcher_tool("patch_namespace")
    assert callable(patcher)
    assert inspect.iscoroutinefunction(patcher)


def test_namespaced_patcher_tool():
    """Test the namespaced_patcher_tool function."""
    namespaced_patcher = g.namespaced_patcher_tool("patch_namespaced_pod")
    assert callable(namespaced_patcher)
    assert inspect.iscoroutinefunction(namespaced_patcher)


def test_reader_tool():
    """Test the reader_tool function."""
    reader = g.reader_tool("read_namespace")
    assert callable(reader)
    assert inspect.iscoroutinefunction(reader)


def test_namespaced_reader_tool():
    """Test the namespaced_reader_tool function."""
    namespaced_reader = g.namespaced_reader_tool("read_namespaced_pod")
    assert callable(namespaced_reader)
    assert inspect.iscoroutinefunction(namespaced_reader)

def test_creator_tool_non_namespaced():
    """Test the creator_tool function for non-namespaced resources."""
    tool = g.creator_tool("list_namespace")
    assert callable(tool)
    assert inspect.iscoroutinefunction(tool)

def test_creator_tool_namespaced():
    """Test the creator_tool function for namespaced resources."""
    namespaced_tool = g.creator_tool("list_namespaced_pod")
    assert callable(namespaced_tool)
    assert inspect.iscoroutinefunction(namespaced_tool)

def test_deleter_tool():
    """Test the deleter_tool function for non-namespaced resources."""
    tool = g.deleter_tool("list_namespace")
    assert callable(tool)
    assert inspect.iscoroutinefunction(tool)

def test_deleter_tool_namespaced():
    """Test the deleter_tool function for namespaced resources."""
    namespaced_tool = g.deleter_tool("list_namespaced_pod")
    assert callable(namespaced_tool)
    assert inspect.iscoroutinefunction(namespaced_tool)