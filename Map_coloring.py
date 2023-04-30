import random
import math

########### Map color problem

# Define the map as a graph
map = {
    "WA": ["NT", "SA"],
    "NT": ["WA", "SA", "Q"],
    "SA": ["WA", "NT", "Q", "NSW", "V"],
    "Q": ["NT", "SA", "NSW"],
    "NSW": ["Q", "SA", "V"],
    "V": ["SA", "NSW"],
    "T": ["U", "ACT"],
    "U": ["T", "ACT", "NSW"],
    "ACT": ["U", "T", "NSW"],
}

# Define the list of possible colors
colors = ["red", "green", "blue", "yellow"]

## Backtracking Search


def backtracking_search(assignment):
    if len(assignment) == len(map):
        return assignment
    var = select_unassigned_variable(assignment)
    for value in order_domain_values(var, assignment):
        if is_consistent(var, value, assignment):
            assignment[var] = value
            result = backtracking_search(assignment)
            if result is not None:
                return result
            del assignment[var]
    return None


def select_unassigned_variable(assignment):
    for var in map:
        if var not in assignment:
            return var


def order_domain_values(var, assignment):
    return colors


def is_consistent(var, value, assignment):
    for neighbor in map[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True


def backtracking_search(assignment, explored):
    explored.append(assignment)
    if len(assignment) == len(map):
        return assignment
    var = select_unassigned_variable(assignment)
    for value in order_domain_values(var, assignment):
        if is_consistent(var, value, assignment):
            assignment[var] = value
            result = backtracking_search(assignment, explored)
            if result is not None:
                return result
            del assignment[var]
    return None


# Test the algorithms and measure the number of explored nodes
explored_nodes = []
print("Backtracking Search: ", backtracking_search({}, explored_nodes))
print("Nodes explored: ", len(explored_nodes))

## Forward Checking


def forward_checking(assignment, domains):
    if len(assignment) == len(map):
        return assignment
    var = select_unassigned_variable(assignment)
    for value in order_domain_values(var, assignment):
        if is_consistent(var, value, assignment):
            assignment[var] = value
            new_domains = forward_checking_update(var, value, domains.copy())
            result = forward_checking(assignment, new_domains)
            if result is not None:
                return result
            del assignment[var]
            domains = new_domains
    return None


def forward_checking_update(var, value, domains):
    for neighbor in map[var]:
        if neighbor not in domains:
            continue
        if value in domains[neighbor]:
            domains[neighbor].remove(value)
            if len(domains[neighbor]) == 0:
                return None
    return domains


def forward_checking(assignment, domains, explored):
    explored.append(assignment)
    if len(assignment) == len(map):
        return assignment
    var = select_unassigned_variable(assignment)
    for value in order_domain_values(var, assignment):
        if is_consistent(var, value, assignment):
            assignment[var] = value
            new_domains = forward_checking_update(var, value, domains.copy())
            result = forward_checking(assignment, new_domains, explored)
            if result is not None:
                return result
            del assignment[var]
            domains = new_domains
    return None


# Test the algorithms and measure the number of explored nodes
explored_nodes = []
print(
    "Forward Checking: ",
    forward_checking({}, {var: colors.copy() for var in map}, explored_nodes),
)
print("Nodes explored: ", len(explored_nodes))


#  Simulated Annealing
# Define the cost function
def get_cost(assignment):
    cost = 0
    for var in map:
        for neighbor in map[var]:
            if assignment[var] == assignment[neighbor]:
                cost += 1
    return cost


def simulated_annealing(initial_state, temperature, alpha):
    current_state = initial_state
    current_cost = get_cost(current_state)
    best_state = current_state
    best_cost = current_cost
    nodes_explored = 0  # initialize the counter
    while temperature > 1e-10:
        new_state = current_state.copy()
        var = random.choice(list(map.keys()))
        value = random.choice(colors)
        new_state[var] = value
        new_cost = get_cost(new_state)
        delta_cost = new_cost - current_cost
        if delta_cost < 0 or math.exp(-delta_cost / temperature) > random.random():
            current_state = new_state
            current_cost = new_cost
        if current_cost < best_cost:
            best_state = current_state
            best_cost = current_cost
        temperature *= alpha
        nodes_explored += 1  # increment the counter
    # print the result
    print("Nodes explored:", nodes_explored)
    return best_state


# Test the algorithm
initial_state = {var: random.choice(colors) for var in map}
best_state = simulated_annealing(initial_state, 100, 0.99)
print("Simulated Annealing", "\n", best_state)


# Hill climbing search
def hill_climbing_search(graph, colors):
    # Initialize the state
    state = {node: random.choice(colors) for node in graph}

    # Evaluate the initial state
    cost = count_conflicts(graph, state)

    # Repeat until a solution is found or the search space is exhausted
    while True:
        # Find the best successor
        best_successor = None
        best_cost = cost
        for node in graph:
            for color in colors:
                successor = state.copy()
                successor[node] = color
                successor_cost = count_conflicts(graph, successor)
                if successor_cost < best_cost:
                    best_successor = successor
                    best_cost = successor_cost

        # If no better successor, return the current state
        if best_cost >= cost:
            return state

        # Update the current state and cost
        state = best_successor
        cost = best_cost


def count_conflicts(graph, state):
    conflicts = 0
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if state[node] == state[neighbor]:
                conflicts += 1
    return conflicts


# Perform the search and print the results
start_state = hill_climbing_search(map, colors)
print("Hill climbing search: ", "Found solution:", start_state)
print("Number of nodes explored:", 0)
