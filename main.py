import networkx as nx
import random
import matplotlib.pyplot as plt
import heapq

def create_graph(num_vertices=150, max_degree=30):
    G = nx.Graph()
    G.add_nodes_from(range(num_vertices))

    for node in G.nodes():
        potential_edges = set(range(num_vertices)) - {node} - set(G.neighbors(node))
        while len(potential_edges) > 0 and G.degree(node) < max_degree:
            new_edge = potential_edges.pop()
            G.add_edge(node, new_edge)

    # Remove excess edges to ensure max degree is not exceeded
    for node in G.nodes():
        while G.degree(node) > max_degree:
            G.remove_edge(node, random.choice(list(G.neighbors(node))))

    return G

def initialize_colors(graph, num_colors=32):
    colors = {node: random.randint(1, num_colors) for node in graph.nodes()}
    return colors

def evaluate_solution(graph, colors):
    conflicts = sum(colors[edge[0]] == colors[edge[1]] for edge in graph.edges())
    return -conflicts

def scouts_bees_step(graph, colors, num_scouts=3):
    conflict_nodes = [(sum(colors[n] == colors[neigh] for neigh in graph.neighbors(n)), n) for n in graph.nodes()]
    heapq.heapify(conflict_nodes)
    for _ in range(num_scouts):
        _, node = heapq.heappop(conflict_nodes)
        colors[node] = random.randint(1, max(colors.values()))
    return colors

def worker_bees_step(graph, colors, num_workers=22):
    for _ in range(num_workers):
        node = random.choice(list(graph.nodes()))
        available_colors = set(range(1, max(colors.values()) + 1)) - {colors[neigh] for neigh in graph.neighbors(node)}
        if available_colors:
            colors[node] = min(available_colors)
    return colors

def bee_algorithm(graph, max_iter=100):
    colors = initialize_colors(graph)
    best_solution = colors.copy()
    best_quality = evaluate_solution(graph, colors)
    quality_record = [best_quality]

    for iteration in range(1, max_iter):
        colors = scouts_bees_step(graph, colors)
        colors = worker_bees_step(graph, colors)
        current_quality = evaluate_solution(graph, colors)
        if current_quality > best_quality:
            best_quality = current_quality
            best_solution = colors.copy()
        if iteration % 2 == 0:
            quality_record.append(best_quality)

    return best_solution, quality_record

def plot_results(quality_record):
    plt.plot(quality_record)
    plt.xlabel('Iterations (multiply by 20)')
    plt.ylabel('Solution Quality')
    plt.title('Solution Quality vs. Number of Iterations')
    plt.show()

graph = create_graph()
best_solution, quality_record = bee_algorithm(graph)
plot_results(quality_record)
