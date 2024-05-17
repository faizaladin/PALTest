#Phase1
#bit 0 direction of movement 0 - right 1 - left
#bit 1-3 amount of curve for bit 0 movement 8 different turns
#bit 4 direction of turn 0 - right 1 - left
#bit 5-6 amount of turn for bit 4 

#Phase2
#bit 7 direction of movement 0 - right 1 - left
#bit 8-10 amount of curve for bit 7 movement 8 different turns
#bit 11 direction of turn 0 - right 1 - left
#bit 12-13 amount of turn for bit 11

#Loop
#bit 14-16 number of times to loop through can loop 8 times 

#17 bits total 

#import gridtracker
#import reset
import random
import simulation
import tkinter as tk
import random
import time
import math

# Define the gene sequence
GENE_LENGTH = 17

# Define the parameters for the genetic algorithm
POPULATION_SIZE = 100
MUTATION_RATE = 0.01
NUM_GENERATIONS = 10

# Define the fitness function (you should customize this for your specific problem)
def fitness_function(individual):
    # print(individual)
    grid_squares = [21, 22, 23, 24, 25, 20, 19, 18, 17, 16, 11, 12, 13, 14, 15, 10, 9, 8, 7, 6, 1, 2, 3, 4, 5]
    direction_of_movement_1 = individual[0]  # Bit 0: 0 - right, 1 - left
    amount_of_curve_1 = int("".join(map(str, individual[1:4])), 2)  # Bits 1-3: Amount of curve for movement
    direction_of_turn_1 = individual[4]  # Bit 4: 0 - right, 1 - left
    amount_of_turn_1 = int("".join(map(str, individual[5:7])), 2)  # Bits 5-6: Amount of turn
    direction_of_movement_2 = individual[7]  # Bit 7: 0 - right, 1 - left
    amount_of_curve_2 = int("".join(map(str, individual[8:11])), 2)  # Bits 8-10: Amount of curve for movement
    direction_of_turn_2 = individual[11]  # Bit 11: 0 - right, 1 - left
    amount_of_turn_2 = int("".join(map(str, individual[12:14])), 2)  # Bits 12-13: Amount of turn
    number_of_loops = int("".join(map(str, individual[14:17])), 2)  # Bits 14-16: Number of times to loop through

    fitness = 0
    counter = 0
    grids_hit, robot_positions = simulation.start_simulation(direction_of_movement_1, amount_of_curve_1, direction_of_turn_1, amount_of_turn_1, direction_of_movement_2, amount_of_curve_2, direction_of_turn_2, amount_of_turn_2, number_of_loops)
    for i in range(len(grid_squares)):
        #print(grids_hit)
        if grid_squares[i] in grids_hit:
            fitness += 1
        if i != 0 and i % 5 == 0 and fitness % 5 != 0:
            break

    # print(fitness)
    return fitness, robot_positions

def punctuated_fitness_function(individual):
    # Decode the individual
    direction_of_movement_1 = individual[0]  # Bit 0: 0 - right, 1 - left
    amount_of_curve_1 = int("".join(map(str, individual[1:4])), 2)  # Bits 1-3: Amount of curve for movement
    direction_of_turn_1 = individual[4]  # Bit 4: 0 - right, 1 - left
    amount_of_turn_1 = int("".join(map(str, individual[5:7])), 2)  # Bits 5-6: Amount of turn
    direction_of_movement_2 = individual[7]  # Bit 7: 0 - right, 1 - left
    amount_of_curve_2 = int("".join(map(str, individual[8:11])), 2)  # Bits 8-10: Amount of curve for movement
    direction_of_turn_2 = individual[11]  # Bit 11: 0 - right, 1 - left
    amount_of_turn_2 = int("".join(map(str, individual[12:14])), 2)  # Bits 12-13: Amount of turn
    number_of_loops = int("".join(map(str, individual[14:17])), 2)  # Bits 14-16: Number of times to loop through
    
    # Perform whatever operation or simulation using the decoded parameters
    grids_hit = gridtracker.gridtracking(direction_of_movement_1, amount_of_curve_1, direction_of_turn_1, amount_of_turn_1, direction_of_movement_2, amount_of_curve_2, direction_of_turn_2, amount_of_turn_2, number_of_loops)
    print(grids_hit)
    return len(grids_hit)

# Generate a random individual
def generate_individual():
    return [random.randint(0, 1) for _ in range(GENE_LENGTH)]

# Generate an initial population
def generate_population(size):
    return [generate_individual() for _ in range(size)]

# Mutation function
def mutate(individual):
    for i in range(GENE_LENGTH):
        if random.random() < MUTATION_RATE:
            individual[i] = 1 - individual[i]  # Flip the bit
    return individual

# Crossover function
def crossover(parent1, parent2):
    crossover_point = random.randint(1, GENE_LENGTH - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Roulette wheel selection
def roulette_selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]
    selected_parents = random.choices(population, weights=probabilities, k=POPULATION_SIZE)
    return selected_parents

def draw_points(points):
    drawn_points = []
    for i in range(len(points)):
        x = points[i][0]
        y = points[i][1]
        canvas.create_oval(x-3, y-3, x+3, y+3, fill='black')  # Adjust the size of the point as needed
        drawn_points.append((x, y))
            
    # Draw lines between consecutive drawn points
    for i in range(len(drawn_points)-1):
        x1, y1 = drawn_points[i]
        x2, y2 = drawn_points[i+1]
        canvas.create_line(x1, y1, x2, y2, fill='blue')  # Adjust the color as needed


# Genetic algorithm main function
def genetic_algorithm():
    population = generate_population(POPULATION_SIZE)
    for generation in range(NUM_GENERATIONS):
        fitness_scores = []
        all_positions = []
        #print(f"generation: {generation}")
        # Evaluate fitness
        for i in range(len(population)):
            fitness, robot_positions = fitness_function(population[i])
            fitness_scores.append(fitness)
            all_positions.append(robot_positions)
        #fitness_scores = [fitness_function(individual) for individual in population]
        print(f"generation: {generation}", f"fitness score: {max(fitness_scores)}")

        # Select parents for crossover using roulette wheel selection
        selected_parents = roulette_selection(population, fitness_scores)
        # Create next generation
        next_generation = []
        for i in range(0, POPULATION_SIZE, 2):
            parent1 = selected_parents[i]
            parent2 = selected_parents[i + 1]
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            next_generation.extend([child1, child2])

        population = next_generation

    # Return the best individual found
    best_fitness_score = 0
    for x in range(len(population)):
            fitness, robot_positions = fitness_function(population[x])
            fitness_scores.append(fitness)
            all_positions.append(robot_positions)
            # Track the best individual
            if fitness > best_fitness_score:
                best_fitness_score = fitness
                best_individual_index = x

    list_of_points = all_positions[best_individual_index]
    return list_of_points

def destroy_all_windows():
    # Loop through all tkinter windows
    for window in tk._default_root.children.values():
        # Destroy the window
        window.destroy()
# best_individual = genetic_algorithm()
# print("Best Individual:", best_individual)
# print("Fitness Score:", fitness_function(best_individual))

root = tk.Tk()
destroy_all_windows()
root.title("Draw Points")

# Create a canvas widget
canvas = tk.Canvas(root, width=800, height=600, bg='white')
canvas.pack()
canvas.delete("all")
list_of_points = genetic_algorithm()
draw_points(list_of_points)
root.mainloop()