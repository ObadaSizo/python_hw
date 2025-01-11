import numpy as np
import networkx as nx

class TSPSolver:
    def __init__(self, cities, distances):
        self.cities = cities
        self.distances = distances
        self.graph = self._build_graph()
        
    def _build_graph(self):
        G = nx.Graph()
        # Create a mapping of database IDs to sequential numbers
        self.id_map = {city.id: i for i, city in enumerate(self.cities)}
        self.reverse_map = {i: city.id for i, city in enumerate(self.cities)}
        
        # Add nodes with positions for visualization
        for city in self.cities:
            G.add_node(self.id_map[city.id], pos=(city.x_coord, city.y_coord))
        
        # Add edges with manual distances
        for distance in self.distances:
            G.add_edge(
                self.id_map[distance.city1.id],
                self.id_map[distance.city2.id],
                weight=distance.distance
            )
        
        return G
    
    def _calculate_mst_cost(self, nodes):
        """Calculate minimum spanning tree cost for the given nodes."""
        if len(nodes) <= 1:
            return 0
        
        subgraph = self.graph.subgraph(nodes)
        try:
            mst = nx.minimum_spanning_tree(subgraph)
            return sum(mst[u][v]['weight'] for u, v in mst.edges())
        except nx.NetworkXNoPath:
            return float('inf')  # No valid MST exists
    
    def _heuristic(self, current_path, remaining_nodes):
        """
        A* heuristic function using MST lower bound.
        Returns estimated cost to complete the tour from current state.
        """
        if not remaining_nodes:
            # If no remaining nodes, just need to return to start
            return self.graph[current_path[-1]][current_path[0]]['weight']
        
        # Cost of MST of remaining nodes
        mst_cost = self._calculate_mst_cost(remaining_nodes)
        
        # Minimum cost to connect current path to remaining nodes
        min_to_remaining = float('inf')
        min_from_remaining = float('inf')
        
        last_node = current_path[-1]
        for node in remaining_nodes:
            if self.graph.has_edge(last_node, node):
                min_to_remaining = min(min_to_remaining, self.graph[last_node][node]['weight'])
            if self.graph.has_edge(node, current_path[0]):
                min_from_remaining = min(min_from_remaining, self.graph[node][current_path[0]]['weight'])
        
        if min_to_remaining == float('inf') or min_from_remaining == float('inf'):
            return float('inf')  # No valid path exists
            
        return mst_cost + min_to_remaining + min_from_remaining
    
    def solve(self):
        """
        Solve the TSP using A* search algorithm.
        Returns the optimal tour as a list of city IDs.
        """
        if len(self.cities) < 2:
            return None
            
        start_node = 0  # Start with first node (0-based index)
        remaining_nodes = set(range(len(self.cities))) - {start_node}
        
        # Priority queue for A* [(f_score, current_path, remaining_nodes)]
        queue = [(self._heuristic([start_node], remaining_nodes), [start_node], remaining_nodes)]
        visited = set()
        
        while queue:
            f_score, current_path, remaining = queue.pop(0)
            
            if not remaining:  # Complete tour found
                if self.graph.has_edge(current_path[-1], current_path[0]):
                    # Convert back to database IDs
                    return [self.reverse_map[node] for node in current_path]
                continue
            
            # Generate next possible paths
            current = current_path[-1]
            path_key = (current, tuple(sorted(remaining)))
            
            if path_key in visited:
                continue
                
            visited.add(path_key)
            
            # Try all possible next cities
            for next_node in remaining:
                if self.graph.has_edge(current, next_node):
                    new_path = current_path + [next_node]
                    new_remaining = remaining - {next_node}
                    
                    # Calculate g_score (actual cost so far)
                    g_score = sum(self.graph[new_path[i]][new_path[i+1]]['weight'] 
                                for i in range(len(new_path)-1))
                    
                    # Calculate h_score (estimated cost to complete)
                    h_score = self._heuristic(new_path, new_remaining)
                    
                    if h_score == float('inf'):
                        continue  # Skip if no valid path exists
                    
                    # Calculate f_score
                    f_score = g_score + h_score
                    
                    # Add to priority queue
                    queue.append((f_score, new_path, new_remaining))
            
            # Sort queue by f_score
            queue.sort(key=lambda x: x[0])
        
        return None  # No valid tour found
    
    def get_tour_distance(self, tour):
        """Calculate the total distance of a tour."""
        if not tour:
            return float('inf')
        
        total_distance = sum(self.graph[self.id_map[tour[i]]][self.id_map[tour[i+1]]]['weight'] 
                           for i in range(len(tour)-1))
        # Add distance back to start
        total_distance += self.graph[self.id_map[tour[-1]]][self.id_map[tour[0]]]['weight']
        
        return total_distance 