# -*- coding: utf-8 -*-
"""
Test module for the generate module.
Copyright (c) 2025, Google LLC.
"""
from generate import list_k8s_function
from generate import num_params

def test_list():
    """Test the list_k8s_function function."""
    # Test with a pattern that should match some functions
    matching_functions = list_k8s_function(r"^list_.*")
    assert isinstance(matching_functions, list)
    assert len(matching_functions) > 0
    for func_name in matching_functions:
        assert func_name.startswith("list_")

def test_nonexistent():
    """Test the list_k8s_function function with a non-existent pattern."""
    # Test with a pattern that should match no functions
    no_matching_functions = list_k8s_function(r"^nonexistent_.*")
    assert isinstance(no_matching_functions, list)
    assert len(no_matching_functions) == 0

def test_specific_function():
    """Test the list_k8s_function function with a specific function name."""
    # Test with a pattern that should match a specific function
    specific_function = list_k8s_function(r"^list_namespace$")
    assert isinstance(specific_function, list)
    assert len(specific_function) == 1
    assert specific_function[0] == "list_namespace"


def test_num_params():
    # pylint: disable=unused-argument
    """Test the num_params function with different method signatures."""

    def no_params():
        """Test function with no parameters."""
    assert num_params(no_params) == 0

    def one_required(x):
        """Test function with one required parameter."""
    assert num_params(one_required) == 1

    def mixed_params(a, b, c=None, d=1):
        """Test function with mixed parameters."""
    assert num_params(mixed_params) == 2

    def kwargs_only(**kwargs):
        """Test function with kwargs only."""
    assert num_params(kwargs_only) == 0

    def complex_signature(a, b, *args, c=None, **kwargs):
        """Test function with complex signature."""
    assert num_params(complex_signature) == 2
