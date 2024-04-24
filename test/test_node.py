import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from src.Node import Node

class TestNode():
    def test_init_node(self):
        node = Node("www.google.com")
        assert node.website == "www.google.com"
        assert node.edges == {}
        assert node.visited == False

if __name__ == "__main__":
    pytest.main()