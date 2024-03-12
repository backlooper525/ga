import random
import sys
import test_package.ga3


#viga = test_package.ga3.fitness("0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.0")
#print(f"Average error: {viga}")


# BNF Grammar
bnf_grammar = {
    "<op>": ["<->","<>"],
    "<int>": ["<0>", "<1>", "<2>", "<3>", "<4>", "<5>", "<6>", "<7>", "<8>", "<9>"],
    "<expr>": ["<op>0.<int>,<op>0.<int>,<op>0.<int>,<op>0.<int>,<op>0.<int>,<op>0.<int>,<op>0.<int>"]
}

population_size = 100
generations = 100
mutation_rate = 0.3
elite_percentage = 0.2  # Percentage of fittest individuals to be preserved as elite

def generate_individual():
    def expand(symbol):
        if symbol in bnf_grammar:
            expansion = random.choice(bnf_grammar[symbol])
            return ''.join(expand(s) for s in expansion.split())
        else:
            return symbol
    
    individual = expand("<expr>")
    while "<int>" in individual:
        individual = individual.replace("<int>", random.choice(bnf_grammar["<int>"]), 1)  # Replace one occurrence at a time
    while "<op>" in individual:
        individual = individual.replace("<op>", random.choice(bnf_grammar["<op>"]), 1)  # Replace one occurrence at a time
        
    return individual.replace("<", "").replace(">", "")


# Evaluate individual
def evaluate_individual(individual):
    try:
        #result = eval(individual)
        #return abs(result - 10)  # Fitness is the absolute difference from the target value
        return test_package.ga3.fitness(individual)
    
    except:
        return float('inf')  # Return infinity if there's an error (e.g., invalid individual)

# Main function
def main():
    # Perform genetic algorithm
    population = [generate_individual() for _ in range(population_size)]
    for generation in range(generations):
        # Evaluate population
        evaluated_population = [{'individual': ind, 'fitness': evaluate_individual(ind)} for ind in population]
    
        # Sort population by fitness
        evaluated_population.sort(key=lambda x: x['fitness'])
    
        # Select elite individuals
        elite_count = int(elite_percentage * population_size)
        elite = [x['individual'] for x in evaluated_population[:elite_count]]
    
        # Print best individual in current generation
        best_individual = evaluated_population[0]['individual']
        best_fitness = evaluated_population[0]['fitness']
        print(f"Generation {generation}: Best individual - {best_individual} (Fitness: {best_fitness})")
    
        # Select parents only from the elite individuals and perform crossover to create new population
        new_population = elite[:]
        while len(new_population) < population_size:
            parent1 = random.choice(elite)
            parent2 = random.choice(elite)
            crossover_point = random.randint(1, len(parent1) - 1)
            child = parent1[:crossover_point] + parent2[crossover_point:]
            
            # Apply mutation
            if random.random() < mutation_rate:
                mutation_point = random.randint(0, len(child) - 1)
                if child[mutation_point].isdigit():
                    mutation_char = random.choice(bnf_grammar["<int>"])
                    child = child[:mutation_point] + mutation_char + child[mutation_point + 1:]
                    child = child.replace("<", "").replace(">", "")
                    #print("child: " + child)
                
            new_population.append(child)
    
        population = new_population

if __name__ == "__main__":
    main()