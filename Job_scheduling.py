
from typing import List, Dict
import random
import math
import time

# Define the job scheduling problem
jobs = {
    'Job1': {
        'duration': 5,
        'dependencies': []
    },
    'Job2': {
        'duration': 3,
        'dependencies': ['Job1']
    },
    'Job3': {
        'duration': 2,
        'dependencies': ['Job1']
    },
    'Job4': {
        'duration': 4,
        'dependencies': ['Job2', 'Job3']
    },
    'Job5': {
        'duration': 3,
        'dependencies': ['Job3']
    }
}

# Define the backtracking search algorithm


def get_cost(assignment):
    cost = 0
    for var in jobs:
        for neighbor in jobs[var]['dependencies']:
            if assignment[var] == assignment[neighbor]:
                cost += 1
    return cost


def select_unassigned_variable(assignment):
    unassigned_vars = [var for var in jobs if assignment[var] is None]
    return min(unassigned_vars, key=lambda var: len(jobs[var]['dependencies']))


def order_domain_values(var, assignment):
    return sorted(range(1, jobs[var]['duration'] + 1))


def is_consistent(var, value, assignment):
    for neighbor in jobs[var]['dependencies']:
        if assignment[neighbor] == value:
            return False
    return True


def backtracking_search(assignment):
    # Check if assignment is complete
    if all(assignment[key] is not None for key in jobs):
        return assignment

    # Select an unassigned variable
    var = select_unassigned_variable(assignment)

    # Try assigning each value to the variable
    for value in order_domain_values(var, assignment):
        # Check if the value is consistent with the current assignment
        if is_consistent(var, value, assignment):
            # Update the assignment
            assignment[var] = value

            # Check the number of nodes explored
            global node_count
            node_count += 1

            # Recursively search for a solution
            result = backtracking_search(assignment)

            # If a solution is found, return it
            if result is not None:
                return result

            # Otherwise, backtrack
            assignment[var] = None

    # If no solution is found, return None
    return None


# Test the algorithm
initial_assignment = {var: None for var in jobs}
node_count = 0
solution = backtracking_search(initial_assignment)
print("Solution:", solution)
print("Cost:", get_cost(solution))
print("Nodes explored:", node_count)


# Define the forward checking algorithm
def get_cost(assignment):
    cost = 0
    for var in jobs:
        for neighbor in jobs[var]['dependencies']:
            if assignment[var] == assignment[neighbor]:
                cost += 1
    return cost


def forward_checking(assignment, domains):
    # Check if assignment is complete
    if all(assignment[key] is not None for key in assignment):
        return assignment

    # Select an unassigned variable
    var = select_unassigned_variable(assignment)

    # Try assigning each value to the variable
    for value in order_domain_values(var, assignment):
        # Check if the value is consistent with the current assignment
        if is_consistent(var, value, assignment):
            # Update the assignment
            assignment[var] = value

            # Check the number of nodes explored
            global node_count
            node_count += 1

            # Forward checking
            new_domains = domains.copy()
            for neighbor in jobs[var]['dependencies']:
                if new_domains[neighbor] is not None:
                    new_domains[neighbor].discard(value)
                    if not new_domains[neighbor]:
                        # If a domain becomes empty, backtrack
                        assignment[var] = None
                        break

            if assignment[var] is not None:
                # Recursively search for a solution
                result = forward_checking(assignment, new_domains)

                # If a solution is found, return it
                if result is not None:
                    return result

                # Otherwise, backtrack
                assignment[var] = None

    # If no solution is found, return None
    return None


# Test the algorithm
initial_assignment = {var: None for var in jobs}
domains = {var: set(range(1, jobs[var]['duration'] + 1)) for var in jobs}
node_count = 0
solution = forward_checking(initial_assignment, domains)
print("Solution:", solution)
print("Cost:", get_cost(solution))
print("Nodes explored:", node_count)


# Define the hill-climbing search algorithm
def hill_climbing_search(jobs):
    # Compute the dependencies for each job
    dependencies = {job: set(jobs[job]['dependencies']) for job in jobs}
    for job in jobs:
        if job not in dependencies:
            dependencies[job] = set()

    # Initialize the start times for each job
    start_times = {job: 0 for job in jobs}

    # Define a function to compute the makespan for the current schedule
    def compute_makespan():
        finish_times = {job: start_times[job] +
                        jobs[job]['duration'] for job in jobs}
        return max(finish_times.values())

    # Initialize the best makespan and best schedule
    best_makespan = compute_makespan()
    best_schedule = [job for job in jobs]

    # Iterate until no improvement can be made
    start_time = time.time()
    while True:
        # Compute the neighbors of the current schedule by swapping adjacent jobs
        neighbors = []
        for i in range(len(jobs) - 1):
            new_schedule = best_schedule[:]
            new_schedule[i], new_schedule[i +
                                          1] = new_schedule[i + 1], new_schedule[i]
            neighbors.append(new_schedule)

        # Evaluate the neighbors and select the best one
        neighbor_makespans = [compute_makespan() for schedule in neighbors]
        best_neighbor_index = min(
            range(len(neighbors)), key=lambda i: neighbor_makespans[i])
        best_neighbor_makespan = neighbor_makespans[best_neighbor_index]
        best_neighbor_schedule = neighbors[best_neighbor_index]

        # Check if the best neighbor is better than the current schedule
        if best_neighbor_makespan < best_makespan:
            best_makespan = best_neighbor_makespan
            best_schedule = best_neighbor_schedule
            start_times = {job: max(start_times[dep] + jobs[dep]['duration']
                                    for dep in dependencies[job]) for job in best_schedule}
        else:
            break

    # Return the optimal schedule and the time spent in seconds
    end_time = time.time()
    time_spent = end_time - start_time
    return best_schedule, best_makespan, time_spent


# Call the hill-climbing search algorithm and print the output
schedule, cost, time_spent = hill_climbing_search(jobs)
print("Optimal Schedule:", schedule)
print("Cost:", cost)
print("Time Spent:", time_spent, "seconds")
