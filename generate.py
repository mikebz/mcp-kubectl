import inspect
import re
from kubernetes import client

def list_k8s_function(regex_pattern: str, max_params: int = None) -> list[str]:
    """
    Lists all functions in client.CoreV1Api that match a given regex pattern.

    Args:
        regex_pattern: The regex pattern to match against function names.

    Returns:
        A list of function names that match the regex pattern.
    """

    if max_params is None:
        max_params  = 0

    api_class = client.CoreV1Api
    matching_functions: list[str] = []
    for name in dir(api_class):
        attr = getattr(api_class, name)

        if callable(attr) and re.match(regex_pattern, name):
            if num_params(attr) <= max_params:
                matching_functions.append(name)
    return matching_functions

def num_params(method: callable) -> int: 
    """
    Calculate the number of required positional parameters for a given method.

    This function inspects the signature of the provided method and counts the
    number of parameters that are positional (either positional-only or positional-or-keyword)
    and do not have default values.

    Args:
        method (callable): The method or function to analyze.

    Returns:
        int: The number of required positional parameters.
    """
    sig = inspect.signature(method)
    result = 0 

    for param in sig.parameters.values():
        if param.name != "self" and param.default is param.empty and param.kind in (param.POSITIONAL_OR_KEYWORD, param.POSITIONAL_ONLY):
            result += 1
    return result 


def create_lister(name: str) -> callable:
    """
    Create a lister function for a specific Kubernetes resource.

    Args:
        name: the method name to call on the CoreV1Api client (e.g., "list_pods",
        "list_nodes").

    Returns:
        A function that lists the specified resource.
    """
    async def lister() -> dict:
        """List the specified Kubernetes resource."""
        v1 = client.CoreV1Api()
        method = getattr(v1, name)
        r = method()
        return r.to_dict()

    return lister