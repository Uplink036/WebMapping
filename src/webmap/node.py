class Node:
    def __init__(self, website):
        if not self._is_valid(website):
            raise ValueError
        self.website = website
        self.edges = {}
        self.visited = False

    def add_edge(self, node):
        self.edges[node.website] = node
        if node.get_edge(self.website) is None:
            node.add_edge(self)

    def get_edge(self, name):
        if name in self.edges:
            return self.edges[name]
        return None

    def get_edges(self):
        return self.edges
    
    def get_number_of_edges(self):
        return len(self.edges)

    def get_website(self):
        return self.website 
    
    def _is_valid(self, website):
        if website is None:
            return False
        return True

    def __str__(self):
        return self.website