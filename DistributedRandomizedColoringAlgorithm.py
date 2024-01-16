import networkx as nx
import random

random.seed(25)

# Generates color set of size delta + 1
def create_color_set(size):
    return list(range(size + 1))

# Select a random color from the set
def select_random_candidate_color(colors):
    return random.choice(colors) 

def exchange_candidate_colors(graph):
    for node in graph.nodes:
        graph.nodes[node]["neighbors_candidate_color"] = []  # Clear previous candidate colors of neighbors 
        for neighbor_node in graph.nodes[node]["neighbors"]:            
            graph.nodes[node]["neighbors_candidate_color"].append(graph.nodes[neighbor_node]["candidate_color"])
            
            # Save colors of permanently colored neighbours to be used in the recolor_nodes function
            if graph.nodes[neighbor_node]["permanently_colored"]:
                if graph.nodes[neighbor_node]["candidate_color"] not in graph.nodes[node]["permantently_colored_neighbors_colors"]:
                    graph.nodes[node]["permantently_colored_neighbors_colors"].append(graph.nodes[neighbor_node]["candidate_color"])

def recolor_nodes(graph):
    for node in graph.nodes:        
        if not graph.nodes[node]["permanently_colored"]:
            # Find valid colors by taking the difference of the sets of all colors (available colors) 
            # and the colors of permanently colored neighbors
            valid_colors = list(set(graph.nodes[node]["available_colors"]) - 
                                set(graph.nodes[node]["permantently_colored_neighbors_colors"]))
            if len(graph.nodes[node]["neighbors"]) != 0: 
                graph.nodes[node]["candidate_color"] = select_random_candidate_color(valid_colors)
            else:
                # In case a node from the randomly generated graph has degree 0
                graph.nodes[node]["candidate_color"] = select_random_candidate_color(graph.nodes[node]["available_colors"])

# Ensures that all nodes are permanently colored and that they have a valid color selected
def check_if_all_nodes_colored(graph):
    for node in graph.nodes:
        if graph.nodes[node]["permanently_colored"] == False or graph.nodes[node]["candidate_color"] == None:
            return False
    
    return True
      
def set_or_discard_color(graph, debug):
    if debug:
        print(f"_______________________________________________________________________________")
    
    for node in graph.nodes:
        if graph.nodes[node]["permanently_colored"]:
            continue
        if graph.nodes[node]["candidate_color"] not in graph.nodes[node]["neighbors_candidate_color"]:
            graph.nodes[node]["permanently_colored"] = True
            
            if debug:
                print(f"Permantently set color of node: {node}, to color: {graph.nodes[node]["candidate_color"]}")
        else:
            if debug:
                print(f"Discarded color of node: {node}, with candidate color: {graph.nodes[node]["candidate_color"]}")
            graph.nodes[node]["candidate_color"] = None
        
        # Outputs a list of candidate colors from neighbors from current node 
        if debug: 
            print(f"Candidate colors of neighbors: {graph.nodes[node]["neighbors_candidate_color"]}")
            print(f"_______________________________________________________________________________")
    
    if debug:    
        print("\n")
    
    # Outputs extensive informations about the nodes and the graph
    # print("\nAfter exchange and setting:")
    # print_graph_info(graph)

# Initializes all nodes in the graph with default values
def initialize(graph, colors):
    for node in graph.nodes:
        graph.nodes[node]["candidate_color"] = None                             # Current candidate color
        graph.nodes[node]["permanently_colored"] = False                        # If true the candidate color is the permanent color
        graph.nodes[node]["available_colors"] = colors.copy()                   # List of possible colors
        graph.nodes[node]["neighbors"] = sorted(list(graph.neighbors(node)))    # Sorted (for debugging) list of neighbors
        graph.nodes[node]["neighbors_candidate_colors"] = []                    # Candidate colors of the neighbors
        graph.nodes[node]["permantently_colored_neighbors_colors"] = []         # Colors of permanently colored neighbors
        
    print(f"_______________________________________________________________________________")
    # Outputs extensive informations about the nodes and the graph
    # print("Initialized graph.")
    # print_graph_info(graph)

# Calculates the size of the final coloring of the graph and the colors that are in it
def calculate_coloring(graph):
    final_coloring = []
    for node in graph.nodes:
        final_coloring.append(graph.nodes[node]["candidate_color"])
    final_colors_set = set(final_coloring)
    return final_colors_set, len(final_colors_set)

def distributed_randomized_coloring_algorithm(graph, delta, debug, final_state_output):
    color_set = create_color_set(delta)
    iterations = 0
    # Initialize graph
    initialize(graph, color_set)
    
    while not check_if_all_nodes_colored(graph):
        iterations += 1
        
        if debug:
            print(f"Round: {iterations}")
        
        recolor_nodes(graph)
        exchange_candidate_colors(graph)
        set_or_discard_color(graph, debug)

    print("Finished simulation.\n")
    print_final_state_of_graph(graph, final_state_output) 
    colors_set, colors_count = calculate_coloring(graph)
    print(f"\nDelta + 1: {delta + 1}.\nNumber of nodes: {len(graph.nodes)}.\nColored graph with {colors_count} colors.")
    print(f"Final set of colors:\n {colors_set}")
    print(f"\nNumber of simulated rounds done to achieve the coloring: {iterations}.")
    print(f"Verify validity of coloring: {verify_coloring_validity(graph)}")
    print(f"_______________________________________________________________________________")    

# For debugging
def print_graph_info(graph):
    for node in sorted(graph.nodes):
        print("Node:", node, "| Node informations:", graph.nodes[node])

# Prints out the final coloring of each node and its neighbors candidate color sets
def print_final_state_of_graph(graph, final_state_output):
    if final_state_output:
        print("Final state of graph:")
        print(f"_______________________________________________________________________________")
        
        for node in graph.nodes:
            print(f"Permantent color of node: {node} is color: {graph.nodes[node]["candidate_color"]}")
            print(f"Degree of node: {len(graph.nodes[node]["neighbors"])}")
            print(f"Final state of candidate colors of neighbors: {graph.nodes[node]["neighbors_candidate_color"]}")
            print(f"_______________________________________________________________________________")

def very_basic_testcases_on_regular_graphs(debug, final_state_output):
    for i in range(1, 11):
        print(f"Very basic testcase {i}:")
        DELTA = i
        num_nodes = DELTA * 2
        # Generates a regular graph
        G = nx.random_regular_graph(DELTA, num_nodes)
        distributed_randomized_coloring_algorithm(G, DELTA, debug, final_state_output)
        print("\n")

def generate_random_graphs(degree_min, degree_max, num_nodes_min, num_nodes_max, debug, final_state_output):
    # Generate random maximum degree in the given range
    DELTA = random.randrange(degree_min, degree_max)

    # Generate random number of nodes in the given reange
    num_nodes = random.randrange(num_nodes_min, num_nodes_max)

    # Define the probability of an edge between any two nodes
    probability = DELTA / num_nodes

    # Generate a random graph with inputed parameters
    # Uses the Erdős–Rényi model
    G = nx.fast_gnp_random_graph(num_nodes, probability, directed=False)
    distributed_randomized_coloring_algorithm(G, DELTA, debug, final_state_output)

def verify_coloring_validity(graph):
    for node in graph.nodes():
        assert graph.nodes[node]["permanently_colored"] == True and graph.nodes[node]["candidate_color"] != None
        
        for neighbor_node in graph.nodes[node]["neighbors"]:
            assert graph.nodes[node]["candidate_color"] != graph.nodes[neighbor_node]["candidate_color"]

    return "VALID COLORING!"

def main():
    DEBUG = 0
    FINAL_STATE_OUTPUT = 0
    # Tests regular graphs up to degree 10
    print("Very basic testcases:")
    very_basic_testcases_on_regular_graphs(DEBUG, FINAL_STATE_OUTPUT)
    
    # Basic testcases with a small graph where the degrees of nodes are different
    print("Basic testcase:")
    generate_random_graphs(degree_min=5, degree_max=10, num_nodes_min=10, num_nodes_max=20, debug=DEBUG, final_state_output=FINAL_STATE_OUTPUT)
    
    # More advanced testcases with a couple hundred nodes
    print("Advanced testcase 1:")
    generate_random_graphs(degree_min=10, degree_max=100, num_nodes_min=100, num_nodes_max=400, debug=DEBUG, final_state_output=FINAL_STATE_OUTPUT)
    print("Advanced testcase 2:")
    generate_random_graphs(degree_min=20, degree_max=200, num_nodes_min=200, num_nodes_max=600, debug=DEBUG, final_state_output=FINAL_STATE_OUTPUT)
    print("Advanced testcase 3:")
    generate_random_graphs(degree_min=40, degree_max=400, num_nodes_min=400, num_nodes_max=800, debug=DEBUG, final_state_output=FINAL_STATE_OUTPUT)
    print("Advanced testcase 4:")
    generate_random_graphs(degree_min=200, degree_max=800, num_nodes_min=800, num_nodes_max=1200, debug=DEBUG, final_state_output=FINAL_STATE_OUTPUT)
    

if __name__ == "__main__":
    main()