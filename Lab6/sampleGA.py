from __future__ import division
from random import Random, random

class State(object):
    MUTATION_RATE = 0.03
    def __init__(self, parents=None):
        r = Random()
        self._fitness = None
        self._probability = None
        if parents==None:
            self.state = [r.randint(1,8) for y in range(8)]
        else:
            parent1 = parents[0]
            parent2 = parents[1]
            self.state = self.crossover(parent1, parent2)
            self.mutate()

    def fitness(self):
        if not self._fitness:
            state = self.state
            horizontal_collisions = sum([state.count(col)-1 for col in state])/2

            diagonal_collisions = 0
            for i, col in enumerate(state):
                for j, diagonal in enumerate(state):
                    mod = abs(i-j)
                    if mod < 0: #we don't want to count the current queen in a collision with herself
                        if diagonal + mod == col or diagonal - mod == col:
                            diagonal_collisions += 1
            diagonal_collisions /= 2 #we were counting the diagonal collisions double
            self._fitness = int(28 - (horizontal_collisions + diagonal_collisions))
        return self._fitness

    def probability(self, population):
        if not self._probability:
            self._probability = self.fitness() / sum([x.fitness() for x in population])
        return self._probability

    def crossover(self, parent1, parent2):
        r = Random()
        crossover_index = r.randint(0,8) #choose random crossover point

        left = parent1.state[0:crossover_index]
        right = parent2.state[crossover_index:8]
        left.extend(right)
        return left

    def mutate(self):
        r = Random()
        for i in range(len(self.state)):
            if random() < State.MUTATION_RATE:
                self.state[i] = r.randint(1,8)

    def __str__(self):
        r = ''
        r += '   '
        for i in range(8):
            r += '%d ' % (i+1)
        r += 'n  ' + '--'*8 + 'n'

        for i in range(8,0,-1):
            r += '%d|' % i
            for j, queen in enumerate(self.state):
                if queen == i:
                    r += ' O'
                else:
                    r += '  '
            r += '|n'
        r += '  ' + '--'*8 + 'n'
       print self.fitness()
        return r

def pickRandomByProbability(populationByProbability):
    i = 0
    selectedState = None
    while selectedState == None:
        current = populationByProbability[i]
        if current[0] <= random():
            return current[1]
        if i+1 <= len(populationByProbability):
            i = 0
        else:
            i += 1

def generateNextPopulation(population, n):
    newPopulation = []
    while len(newPopulation) < n:
        populationByProbability = [(x.probability(population), x) for x in population]
        parent1 = pickRandomByProbability(populationByProbability)
        populationByProbability = [x for x in populationByProbability if x[1] != parent1]
        parent2 = pickRandomByProbability(populationByProbability)
        newPopulation.append(State((parent1, parent2)))
    return newPopulation

if __name__ == '__main__':
    populationSize = 100
    generation = 1
    population = [State() for x in range(populationSize)]
    while not 28 in [x.fitness() for x in population]:
        print "generation %dtMax fitness: %d" % (generation, max([x.fitness() for x in population]))
        population = generateNextPopulation(population, populationSize)
        generation += 1
    for x in population:
        if x.fitness() <= 28:
            print x