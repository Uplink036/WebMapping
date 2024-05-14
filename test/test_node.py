import pytest
from hypothesis import given, assume
from hypothesis import strategies as st
from webmap.Node import Node

class TestNode():
    @given(st.text())
    def test_init_node(self, website):
        try:
            node = Node(website)
        except ValueError:
            return
        assert node.website == website
        assert node.edges == {}
        assert node.visited == False

    @given(st.text(min_size=1), st.text(min_size=1))
    def test_add_edge(self, website_one, website_two):
        assume(website_one != website_two)
        node1 = Node(website_one)
        node2 = Node(website_two)
        node1.add_edge(node2)
        assert node1.edges == {website_two: node2}
        assert node2.edges == {website_one: node1}

    @given(st.text(min_size=1), st.text(min_size=1))
    def test_get_edge(self, website_one, website_two):
        assume(website_one != website_two)
        node1 = Node(website_one)
        node2 = Node(website_two)
        node1.add_edge(node2)
        assert node1.get_edge(website_two) == node2
        assert node1.get_edge(website_one) == None
    
    @given(st.text(min_size=1), st.text(min_size=1))
    def test_get_edges(self, website_one, website_two):
        assume(website_one != website_two)
        node1 = Node(website_one)
        node2 = Node(website_two)
        node1.add_edge(node2)
        assert node1.get_edges() == {website_two: node2}
    
    @given(st.text(min_size=1), st.text(min_size=1))
    def test_get_number_of_edges(self, website_one, website_two):
        assume(website_one != website_two)
        node1 = Node(website_one)
        node2 = Node(website_two)
        node1.add_edge(node2)
        assert node1.get_number_of_edges() == 1

    @given(st.text())
    def test_get_website(self, website):
        node = Node(website)
        assert node.get_website() == website

    @given(st.text())
    def test_dunder_str(self, website):
        node = Node(website)
        assert str(node) == website

if __name__ == "__main__":
    pytest.main()