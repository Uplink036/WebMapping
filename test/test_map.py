import pytest
from unittest import mock

from webmap.node import Node
from webmap.map import plot_nodes, node_to_dot

class TestMap():
    def test_plot_nodes(self):
        with mock.patch('webmap.go.Figure.show') as mock_draw:
            node1 = Node("www.google.com")
            node2 = Node("www.facebook.com")
            node3 = Node("www.twitter.com")
            node1.add_edge(node2)
            node1.add_edge(node3)
            plot_nodes(node1)
            mock_draw.assert_called()

    def test_node_to_dot(self):
        node1 = Node("www.google.com")
        node2 = Node("www.facebook.com")
        node3 = Node("www.twitter.com")
        node1.add_edge(node2)
        node1.add_edge(node3)
        node_to_dot(node1)


if __name__ == "__main__":
    pytest.main()