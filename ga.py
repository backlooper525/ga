import random
import sys
import test_package.ga_fitness2
import multiprocessing

bnf_grammar = {
    "<comp>": ["+","-"],
    "<op>": ["<->","<>"],
    "<int>": ["<0>", "<01>", "<02>", "<03>", "<04>", "<05>", "<06>", "<07>", "<08>", "<09>"],
    "<ma>": ["<MA10>","<MA20>","<MA50>","<MA100>"],
    "<expr>": ["<ma>,<op>0.<int>,<ma>,<op>0.<int>,<comp>,<comp>"]
}

symb = "MU"
population_size = 100
generations = 50
mutation_rate = 0.5
elite_percentage = 0.3  # Protsent indiviididest, kes moodustavad eliidi

def generate_individual(individual = None):
    def expand(symbol):
        if symbol in bnf_grammar:
            expansion = random.choice(bnf_grammar[symbol])
            return ''.join(expand(s) for s in expansion.split())
        else:
            return symbol
    
    if individual is None: individual = expand("<expr>")
        
    #teeb BNF asja 
    while "<int>" in individual:
        individual = individual.replace("<int>", random.choice(bnf_grammar["<int>"]), 1)  
    while "<op>" in individual:
        individual = individual.replace("<op>", random.choice(bnf_grammar["<op>"]), 1)  
    while "<ma>" in individual:
        individual = individual.replace("<ma>", random.choice(bnf_grammar["<ma>"]), 1)   
    while "<comp>" in individual:
        individual = individual.replace("<comp>", random.choice(bnf_grammar["<comp>"]), 1)       
        
    individual = individual.replace("<", "").replace(">", "")
    # print(individual)
    # sys.exit()
    return individual
    

# Hinda indiviidi
def evaluate_individual(individual, data):
    #print(test_package.ga_fitness2.trade(individual)
    try:
        return test_package.ga_fitness2.trade(individual, data)
    
    except:
        return -float('inf')  # Kui error, siis l6pmatus


def main():
    test_package.ga_fitness2.read(symb)
    print(test_package.ga_fitness2.buynhold(test_package.ga_fitness2.data['Close']))

    
    population = [generate_individual() for _ in range(population_size)]
      
    for generation in range(generations):
        # Hinda populatsiooni
        #evaluated_population = [{'individual': ind, 'fitness': evaluate_individual(ind)} for ind in population]

    
        # Loo multiprocessing Pool
        with multiprocessing.Pool(processes=4) as pool:
            data = test_package.ga_fitness2.data
            # Kaardista funktsioon iga numbri jaoks massiivis ja saa tulemused.
            fitness_results = pool.starmap(evaluate_individual, [(ind, data) for ind in population])

        pool.join()
        

        # Liida indiviidid nende fitness skooriga
        evaluated_population = [{'individual': ind, 'fitness': fitness} for ind, fitness in zip(population, fitness_results)]


        # Sordi fitnessi p6hjal
        evaluated_population.sort(key=lambda x: x['fitness'], reverse=True)
  
        # Vali eliit 
        elite_count = int(elite_percentage * population_size)
        elite = [x['individual'] for x in evaluated_population[:elite_count]]
    
        # Print best individual in current generation
        best_individual = evaluated_population[0]['individual']
        best_fitness = evaluated_population[0]['fitness']
        print(f"Generation {generation}: Best individual - {best_individual} (Fitness: {best_fitness})")
    

        # Vali vanemad eliidist ja lase neil paarituda, synnib uus generatsioon
        new_population = elite[:]
        while len(new_population) < population_size:
            parent1 = random.choice(elite)
            parent2 = random.choice(elite)
            
            parent1_parts = parent1.split(',')
            parent2_parts = parent2.split(',')
            crossover_point = random.randint(1, len(parent1_parts) - 1)
            child_parts = parent1_parts[:crossover_point] + parent2_parts[crossover_point:]
            child = ','.join(child_parts)
            #print("1: " + child)
            
            # Muteeri
            if random.random() < mutation_rate:                
                values = child.split(',')
                mutation_index = random.randint(0, len(values) - 1)  
                mutated_value = bnf_grammar["<expr>"][0].split(',')[mutation_index]                   
                values[mutation_index] = mutated_value
                # Loo individual koos muteerunud v22rtusega
                child = ','.join(values)
                child = generate_individual(child)
                #print(child)

            new_population.append(child)
    
        population = new_population

if __name__ == "__main__":
    main()
