"""Shared functions for all tests."""
import os
from typing import List

import yaml


def get_clients(client_type: str) -> List:
    """Get a list of of client Objects for the supplied types."""
    file_name = os.path.join(os.path.dirname(__file__), f"{client_type}s.yml")

    with open(file_name) as fp:
        clients = yaml.safe_load(fp)

    return clients["clients"]
