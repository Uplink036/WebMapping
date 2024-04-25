import pytest
from webmap.Node import Node

class TestNode():
    def test_init_node(self):
        node = Node("www.google.com")
        assert node.website == "www.google.com"
        assert node.edges == {}
        assert node.visited == False

    def test_add_edge(self):
        node1 = Node("www.google.com")
        node2 = Node("www.facebook.com")
        node1.add_edge(node2)
        assert node1.edges == {"www.facebook.com": node2}
        assert node2.edges == {"www.google.com": node1}

    def test_get_edge(self):
        node1 = Node("www.google.com")
        node2 = Node("www.facebook.com")
        node1.add_edge(node2)
        assert node1.get_edge("www.facebook.com") == node2
        assert node1.get_edge("www.google.com") == None

    def test_get_edges(self):
        node1 = Node("www.google.com")
        node2 = Node("www.facebook.com")
        node1.add_edge(node2)
        assert node1.get_edges() == {"www.facebook.com": node2}
    
    def test_get_number_of_edges(self):
        node1 = Node("www.google.com")
        node2 = Node("www.facebook.com")
        node1.add_edge(node2)
        assert node1.get_number_of_edges() == 1

    def test_get_website(self):
        node = Node("www.google.com")
        assert node.get_website() == "www.google.com"

    def test_dunder_str(self):
        node = Node("www.google.com")
        assert str(node) == "www.google.com"


if __name__ == "__main__":
    pytest.main()