import pytest
from unittest import mock

from webmap.Node import Node
from webmap.Map import plot_nodes

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


if __name__ == "__main__":
    pytest.main()