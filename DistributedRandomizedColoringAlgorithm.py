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
        graph.nodes[node]["neighbors_candidate_color"] = []
        for neighbor_node in graph.nodes[node]["neighbors"]:            
            graph.nodes[node]["neighbors_candidate_color"].append(graph.nodes[neighbor_node]["candidate_color"])
            
            if graph.nodes[neighbor_node]["permanently_colored"]:
                if graph.nodes[neighbor_node]["candidate_color"] not in graph.nodes[node]["permantently_colored_neighbors_colors"]:
                    graph.nodes[node]["permantently_colored_neighbors_colors"].append(graph.nodes[neighbor_node]["candidate_color"])

def recolor_nodes(graph):
    for node in graph.nodes:        
        if not graph.nodes[node]["permanently_colored"]:
            valid_colors = list(set(graph.nodes[node]["available_colors"]) - set(graph.nodes[node]["permantently_colored_neighbors_colors"]))
            graph.nodes[node]["candidate_color"] = select_random_candidate_color(valid_colors)
            
def check_if_all_nodes_colored(graph):
    for node in graph.nodes:
        if graph.nodes[node]["permanently_colored"] == False or graph.nodes[node]["candidate_color"] == None:
            return False
        
    return True

# For debugging
def print_graph_info(graph):
    for node in sorted(graph.nodes):
        print("Node:", node, "| Node informations:", graph.nodes[node])
        
def set_or_discard_color(graph):
    for node in graph.nodes:
        if graph.nodes[node]["permanently_colored"]:
            continue
        if graph.nodes[node]["candidate_color"] not in graph.nodes[node]["neighbors_candidate_color"]:
            graph.nodes[node]["permanently_colored"] = True
        else:
            graph.nodes[node]["candidate_color"] = None            
            # graph.nodes[node]["neighbors_candidate_color"] = []
    print("\nAfter exchange and setting:")
    print_graph_info(graph)

def initialize(graph, colors):
    for node in graph.nodes:
        graph.nodes[node]["candidate_color"] = None
        graph.nodes[node]["permanently_colored"] = False
        graph.nodes[node]["available_colors"] = colors.copy()
        graph.nodes[node]["neighbors"] = sorted(list(graph.neighbors(node)))
        graph.nodes[node]["neighbors_candidate_color"] = []
        graph.nodes[node]["permantently_colored_neighbors_colors"] = []
    print("Initialize:")
    print_graph_info(graph)

def calculate_coloring(graph):
    final_coloring = []
    for node in graph.nodes:
        final_coloring.append(graph.nodes[node]["candidate_color"])
    return len(set(final_coloring))

def distributed_randomized_coloring_algorithm(graph, delta):
    color_set = create_color_set(delta)
    # Initialize
    initialize(graph, color_set)        
    
    while not check_if_all_nodes_colored(graph):
        recolor_nodes(graph)
        exchange_candidate_colors(graph)
        set_or_discard_color(graph)

    print(f"Colored graph with {calculate_coloring(graph)} colors. Delta of graph + 1: {delta + 1}.")
    print("Success")
    

def main():
    DELTA = 5
    # Generate a random 5-regular graph
    G = nx.random_regular_graph(DELTA, 36)  # 10 nodes
    distributed_randomized_coloring_algorithm(G, DELTA)
    nx.draw(G, with_labels=True, font_weight='bold', node_color=[G.nodes[node]["candidate_color"] for node in G.nodes], edge_color='gray')
    plt.show()

if __name__ == "__main__":
    main()