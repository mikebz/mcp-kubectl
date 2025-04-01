import re
from kubernetes import client

def list_k8s_function(regex_pattern: str) -> list[str]:
    """
    Lists all functions in client.CoreV1Api that match a given regex pattern.

    Args:
        regex_pattern: The regex pattern to match against function names.

    Returns:
        A list of function names that match the regex pattern.
    """
    api_class = client.CoreV1Api
    matching_functions = []
    for name in dir(api_class):
        if callable(getattr(api_class, name)) and re.match(regex_pattern, name):
            matching_functions.append(name)
    return matching_functions


def create_lister(name: str) -> callable:
    """
    Create a lister function for a specific Kubernetes resource.

    Args:
        name: the method name to call on the CoreV1Api client (e.g., "list_pods",
        "list_nodes").

    Returns:
        A function that lists the specified resource.
    """
    async def lister() -> list[str]:
        """List the specified Kubernetes resource."""
        v1 = client.CoreV1Api()
        method = getattr(v1, name)
        items = method()
        return [item.metadata.name for item in items.items]

    return lister