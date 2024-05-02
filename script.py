import random
import networkx as nx
import matplotlib.pyplot as plt

class Interaction:
    def __init__(self):
        self.proteins = self.read_proteins()
        self.adj_list = {}
        self.degrees = {}
        self.G = nx.Graph()  # Initialize an empty graph

    def read_proteins(self):
        nom_fichier = "proteines.txt"
        try:
            with open(nom_fichier, 'r') as f:
                proteines = [prot.strip() for prot in f.readlines()]
            return proteines
        except FileNotFoundError:
            print(f"Le fichier {nom_fichier} n'a pas été trouvé.")
            return []

    def add_interaction(self, protein1, protein2):
        if protein1 not in self.adj_list:
            self.adj_list[protein1] = []
        if protein2 not in self.adj_list:
            self.adj_list[protein2] = []
        
        self.adj_list[protein1].append(protein2)
        self.adj_list[protein2].append(protein1)
        self.G.add_edge(protein1, protein2)  # Add edge to the graph

    def generer_interactions(self):
        p = int(input("Entrer le nombre d'interactions : "))
        if p < len(self.proteins) - 1:
            raise ValueError("Le nombre d'interactions est insuffisant pour former un réseau connexe.")
        
        interactions = set()
        visited = set()
        start_node = random.choice(self.proteins)
        queue = [start_node]
        
        while queue:
            current_node = queue.pop(0)
            if current_node not in visited:
                visited.add(current_node)
                if current_node not in self.adj_list:
                    self.adj_list[current_node] = []
                possible_interactions = [protein for protein in self.proteins if protein != current_node and protein not in self.adj_list[current_node]]
                if possible_interactions:
                    new_interaction = random.choice(possible_interactions)
                    interactions.add((current_node, new_interaction))
                    self.add_interaction(current_node, new_interaction)
                    queue.append(new_interaction)
                else:
                    queue.extend([protein for protein in self.proteins if protein != current_node])
        
        extra_interactions = p - len(interactions)
        while extra_interactions > 0:
            protein1, protein2 = random.sample(self.proteins, 2)
            if (protein1, protein2) not in interactions and (protein2, protein1) not in interactions:
                interactions.add((protein1, protein2))
                self.add_interaction(protein1, protein2)
                extra_interactions -= 1
        
        return interactions

    def ecrire_interactions(self, interactions):
        nom_fichier = "interactions.txt"
        with open(nom_fichier, 'w') as f:
            for interaction in interactions:
                f.write(f"{interaction[0]} \t {interaction[1]}\n")
        print(f"Les interactions ont été écrites dans le fichier {nom_fichier}.")

    def Dist(self, source, target):
        try:
            distance = nx.dijkstra_path_length(self.G, source=source, target=target)
            return distance
        except nx.NetworkXNoPath:
            return None

    def characteristic_distance(self):
        total_distance = 0
        pair_count = 0

        # Iterate over all pairs of proteins
        for source in self.G.nodes():
            for target in self.G.nodes():
                if source != target:
                    distance = self.Dist(source, target)
                    if distance is not None:  # If a path exists
                        total_distance += distance
                        pair_count += 1

        # Calculate the average distance
        if pair_count > 0:
            characteristic_distance = total_distance / pair_count
            return characteristic_distance
        else:
            return None

    def is_small_world(self):
        # Calculate characteristic distance of the network
        network_distance = self.characteristic_distance()

        while True:
            try:
                # Generate a random graph with the same number of nodes and edges
                random_graph = nx.gnm_random_graph(len(self.proteins), self.G.number_of_edges())

                # Calculate characteristic distances of random graph
                random_distance = nx.average_shortest_path_length(random_graph)

                # If no exception is raised, break the loop
                break
            except nx.NetworkXError:
                # If the graph is not connected, regenerate it
                continue

        # Generate a lattice graph with the same number of nodes
        lattice_graph = nx.grid_2d_graph(int(len(self.proteins) ** 0.5), int(len(self.proteins) ** 0.5))

        # Calculate characteristic distances of lattice graph
        lattice_distance = nx.average_shortest_path_length(lattice_graph)

        # Determine if the network has small-world properties
        is_small_world = network_distance < random_distance and network_distance < lattice_distance
        return is_small_world
        
    def node_degree(self, node):
        # Check if the node exists in the graph
        if node in self.G:
            # Calculate and return the degree of the node
            return self.G.degree(node)
        else:
            return None
    def draw_network(self):
        # Draw the network
        nx.draw(self.G, with_labels=True, node_size=300, node_color='skyblue', font_size=8)
        plt.title("Protein Interaction Network")
        plt.show()

def main(interaction):
    interactions = interaction.generer_interactions()
    interaction.draw_network()

    protein1 = input("Entrez la première protéine : ")
    protein2 = input("Entrez la deuxième protéine : ")

    distance = interaction.Dist(protein1, protein2)
    if distance is not None:
        print(f"La distance entre {protein1} et {protein2} est : {distance}")
    else:
        print(f"Il n'y a pas de chemin entre {protein1} et {protein2} dans le réseau d'interaction.")

    average_distance = interaction.characteristic_distance()
    print("Average distance (R) of the network:", average_distance)

    is_small_world = interaction.is_small_world()
    print("Is the network a small-world network?", is_small_world)

    node = input("Enter the node you want to check the degree for: ")
    degree = interaction.node_degree(node)
    if degree is not None:
        print(f"Degree of node {node}: {degree}")
    else:
        print(f"Node {node} does not exist in the network.")

if __name__ == "__main__":
    interaction = Interaction()
    main(interaction)