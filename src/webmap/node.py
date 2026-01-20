class Node:
    def __init__(self, website):
        if not self._is_valid(website):
            raise ValueError
        self.website: str = website
        self.edges: dict[str, str] = {}
        self.visited: bool = False

    def add_edge(self, node: Node) -> None:
        self.edges[node.website] = node
        if node.get_edge(self.website) is None:
            node.add_edge(self)

    def get_edge(self, name: str) -> str | None:
        if name in self.edges:
            return self.edges[name]
        return None

    def get_edges(self) -> dict[str, str]:
        return self.edges
    
    def get_number_of_edges(self) -> int:
        return len(self.edges)

    def get_website(self) -> str:
        return self.website 
    
    def _is_valid(self, website: str) -> bool:
        if website is None:
            return False
        return True

    def __str__(self) -> str:
        return self.website