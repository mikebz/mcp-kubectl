import pytest
from generate import list_k8s_function

def test_list():
    """Test the list_k8s_function function."""
    # Test with a pattern that should match some functions
    matching_functions = list_k8s_function(r"^list_.*")
    assert isinstance(matching_functions, list)
    assert len(matching_functions) > 0
    for func_name in matching_functions:
        assert func_name.startswith("list_")

def test_nonexistend():
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
