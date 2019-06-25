# Ozan SAHIN - 15253055
import math
import numpy as np
import sys
import matplotlib.pyplot as plt
count = 0

lines = [line.rstrip('\n').split(",") for line in open(sys.argv[1])]

random_list = list(map(float, lines[0])) 
population_size = int(lines[1][0])
number_of_tournament_members = int(lines[2][0])
mutation_rate = float(lines[3][0])
iteration_count = int(lines[4][0])
knapsack_size = int(lines[5][0])
weights = list(map(int, lines[6]))
values = list(map(int, lines[7]))
population = []

def get_random():
        global count
        count = (count+1)%len(random_list)
        return random_list[count-1]

def get_formulized_i():
        return math.ceil((float(get_random())*population_size)) - 1

def create_population():
        for i in range(population_size):
                individual=""
                individual_value = 0
                individual_weight = 0
                for j in range(len(weights)):
                        if float(get_random()) >= 0.5:
                                individual+="1"
                                individual_value = individual_value + int(values[j])  
                                individual_weight = individual_weight + int(weights[j])
                                if individual_weight > knapsack_size: #evaluate
                                        individual_value=0
                        else:
                                individual+="0"
                population.append((individual,individual_value))
        return population

population=create_population()
best_of_population = []
worst_of_population = []
avarage_of_population = int()
avarages_of_population = []

iteration = 0
while iteration < iteration_count:
        def tournament_selection():
                iter_population = 0
                chosens=[]
                best_individuals=[]
                best_chosen=""
                while iter_population < len(population):
                        for k in range(number_of_tournament_members):
                                formulized_i=int(get_formulized_i())
                                chosens.append((population[formulized_i][0],population[formulized_i][1]))
                                chosens.sort(key = lambda x:x[1])
                                best_chosen=chosens[-1]
                        iter_population+=1
                        best_individuals.append(best_chosen)
                        chosens.clear()
                return best_individuals

        tournament_output = list(tournament_selection())
        pop_size = population_size

        def recombine(): #caprazlama
                iter_recombine = 0
                parents = []
                children = []
                
                while iter_recombine < len(tournament_output):
                        if len(tournament_output) % 2 != 0:
                                tournament_output.remove(tournament_output[-1])
                        else:
                                parent1 = tournament_output[iter_recombine][0]
                                parent2 = tournament_output[iter_recombine+1][0]                

                                cut_point = math.ceil(float(get_random())*len(weights)) -1

                                child1 = parent1[0:cut_point] + parent2[cut_point:] #caprazlama islemi
                                child2 = parent2[0:cut_point] + parent1[cut_point:]

                                iter_recombine = iter_recombine + 2
                                parents.append((parent1, parent2))
                                children.append(child1)
                                children.append(child2)
                                parent1 = ""
                                parent2 = ""
                
                return children

        children_for_mut = list(recombine())
        def mutation():
                iter_mutation = 0
                mutateds = []
                
                while iter_mutation < len(children_for_mut):
                        new_child=[]
                        mutating_child = children_for_mut[iter_mutation]
                        #print(mutating_child)
                        for i in mutating_child:
                                rand=float(get_random())
                                if rand < mutation_rate:
                                        if(i == "0"):
                                                new_child.append(1)
                                        elif(i == "1"):
                                                new_child.append(0)
                                else:
                                        new_child.append(str(i))
                                        
                        new_child = ''.join(map(str, new_child)) 
                        #print(new_child)
                        individual_value = 0
                        individual_weight = 0
                        for j in range(len(new_child)):
                                if(new_child[j]=='1'):
                                        individual_value = individual_value + int(values[j])  
                                        individual_weight = individual_weight + int(weights[j])
                                        if individual_weight > knapsack_size:
                                                individual_value=0
                        iter_mutation += 1
                        mutateds.append((new_child, individual_value))
                return mutateds
        
        iteration += 1

        mutated_children = list(mutation())
        new_population = population + mutated_children
        new_population.sort(key = lambda x:x[1])
        new_population.reverse()
        new_population=new_population[0:population_size]
        population=new_population
        best_of_population.append(population[0][1])
        worst_of_population.append(population[-1][1])
        avarage_of_population = sum(n for _, n in population) / len(population)
        avarages_of_population.append(avarage_of_population)


plt.grid()
plt.scatter(range(0,iteration_count),worst_of_population,c="blue")
plt.scatter(range(0,iteration_count),avarages_of_population,c="red")
plt.scatter(range(0,iteration_count),best_of_population,c="brown")
plt.plot(range(0,iteration_count),worst_of_population,c="blue")
plt.plot(range(0,iteration_count),avarages_of_population,c="red")
plt.plot(range(0,iteration_count),best_of_population,c="brown")
plt.legend(["min","ortalama","max"])
plt.xlabel("İterasyon")
plt.ylabel("Fitness")
plt.show()

print("popopopo", population)

print(best_of_population)
print("\n")
print(worst_of_population)
print("\n")
print(avarages_of_population)