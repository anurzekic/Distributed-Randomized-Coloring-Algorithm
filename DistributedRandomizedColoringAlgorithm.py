import networkx as nx
import random
import matplotlib.pyplot as plt

def create_color_set(size):
    return list(range(size + 1))

def select_random_candidate_color(colors):
    return random.choice(colors) 

# Delta + 1 coloring
def exchange_candidate_colors(graph):
    for node in graph.nodes:
        node_color = graph.nodes[node]["candidate_color"]
        is_node_color_unique = True
        for neighbor_node in graph.nodes[node]["neighbors"]:            
            neighbor_node_color = graph.nodes[neighbor_node]["candidate_color"]
            is_neighbor_node_permanently_colored = graph.nodes[neighbor_node]["permanently_colored"]
            
            if is_neighbor_node_permanently_colored and neighbor_node_color in graph.nodes[node]["available_colors"]:
                # print(graph.nodes[node]["available_colors"])
                # print(neighbor_node_color)
                graph.nodes[node]["available_colors"].remove(neighbor_node_color)
            
            if node_color == neighbor_node_color:
                is_node_color_unique = False
        
        if is_node_color_unique:
            graph.nodes[node]["permanently_colored"] = True
    
    print("\nAfter exchange:")        
    print_graph_info(graph)

def recolor_nodes(graph):
    for node in graph.nodes:
        is_node_permanently_colored = graph.nodes[node]["permanently_colored"]
        if not is_node_permanently_colored:
            graph.nodes[node]["candidate_color"] = select_random_candidate_color(graph.nodes[node]["available_colors"])
            
        
def check_if_all_nodes_colored(graph):
    for node in graph.nodes:
        is_node_permanently_colored = graph.nodes[node]["permanently_colored"]
        if not is_node_permanently_colored:
            return False
        
        for neighbor_node in graph.nodes[node]["neighbors"]:
            node_color = graph.nodes[node]["candidate_color"]
            neighbor_node_color = graph.nodes[neighbor_node]["candidate_color"]
            if node_color == neighbor_node_color:
                return False
    return True

# For debugging
def print_graph_info(graph):
    for node in sorted(graph.nodes):
        print("Node:", node, "| Node informations:", graph.nodes[node])
        

def initialize(graph, colors):
    for node in graph.nodes:
        graph.nodes[node]["candidate_color"] = select_random_candidate_color(colors)
        graph.nodes[node]["permanently_colored"] = False
        graph.nodes[node]["available_colors"] = colors.copy()
        graph.nodes[node]["neighbors"] = sorted(list(graph.neighbors(node)))
    print("Initialize:")
    print_graph_info(graph)

def distributed_randomized_coloring_algorithm(graph, delta):
    color_set = create_color_set(delta)
    # Initialize
    initialize(graph, color_set)        
    exchange_candidate_colors(graph)
    
    while not check_if_all_nodes_colored(graph):
        recolor_nodes(graph)
        exchange_candidate_colors(graph)

    
    print("Success")
    

def main():
    DELTA = 5
    # Generate a random 5-regular graph
    color_mapping = ["red", "green", "blue", "yellow", "orange"]
    G = nx.random_regular_graph(DELTA, 10)  # 10 nodes
    distributed_randomized_coloring_algorithm(G, DELTA)
    nx.draw(G, with_labels=True, font_weight='bold', node_color=[G.nodes[node]["candidate_color"] for node in G.nodes], edge_color='gray')
    plt.show()

if __name__ == "__main__":
    main()