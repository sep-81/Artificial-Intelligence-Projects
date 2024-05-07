import random

# TODO assign numbers to variables below
crossoverProbability = 0.3  # probabality
carryPercentage = 0.1  # prob
crossoverWidth = 4  # number
nextGenParentPercentage = 0.5  # prob
populationSize = 8000  # size


def interleaved(operand, operator):
    myStr = ""
    flagTrun = True
    for i in range(2 * len(operator)+1):
        index = int(i/2)
        nextEl = str(operand[index]) if flagTrun else operator[index]
        # print(nextEl, index, flagTrun)
        myStr += nextEl
        flagTrun = not flagTrun
    return myStr


def calCrossover(chromosome1, chromosome2):
    size = len(chromosome1)
    width = 0
    if size <= crossoverWidth:
        width = 1
    else:
        width = len(chromosome1) // crossoverWidth

    ind = random.randint(0, size-width)
    child = []
    if random.random() < 0.5:
        child = chromosome1[:ind] + \
            chromosome2[ind:ind+width] + chromosome1[ind+width:]
    else:
        child = chromosome2[:ind] + \
            chromosome1[ind:ind+width] + chromosome2[ind+width:]

    return child


class EquationBuilder:

    def __init__(self, operators, operands, equationLength, goalNumber):
        self.operators = operators
        self.operands = operands
        self.equationLength = equationLength
        self.goalNumber = goalNumber

        # Create the earliest population at the begining
        self.population = self.makeFirstPopulation()

    def makeFirstPopulation(self):
        # TODO create random chromosomes to build the early population, and return it
        gen0 = []
        oprands = []
        operators = []
        chromozm = []  # [[operand] [operator]]
        for i in range(populationSize):
            chromozm = []
            oprands = random.choices(
                self.operands, k=int(self.equationLength+1/2))
            operators = random.choices(
                self.operators, k=int(self.equationLength/2))
            chromozm.append(oprands)
            chromozm.append(operators)
            gen0.append(chromozm)
        gen0 = [interleaved(*gen0[i]) for i in range(populationSize)]
        return gen0

    def findEquation(self):
        # Create a new generation of chromosomes, and make it better in every iteration
        while (True):
            random.shuffle(self.population)

            fitnesses = []
            for i in range(populationSize):
                # TODO calculate the fitness of each chromosome
                # chromosome = self.population[i]
                # eqStr = interleaved(*chromosome)
                # self.population[i] = eqStr
                eqStr = self.population[i]
                eq = eval(eqStr)
                fit = -abs(self.goalNumber - eq)
                fitnesses.append(fit)
                # TODO return chromosome if a solution is found, else save the fitness in an array
                if fit == 0:
                    return eqStr

            print(max(fitnesses))

            # TODO find the best chromosomes based on their fitnesses, and carry them directly to the next generation (optional)
            carriedChromosomes = []
            bestChromosomeInd = sorted(
                range(len(fitnesses)), key=lambda k: fitnesses[k], reverse=True)
            self.sortedInd = bestChromosomeInd
            for i in range(0, int(populationSize*carryPercentage)):
                carriedChromosomes.append(
                    self.population[bestChromosomeInd[i]])

            # A pool consisting of potential candidates for mating (crossover and mutation)
            matingPool = self.createMatingPool()
            # print(len(matingPool))
            # The pool consisting of chromosomes after crossover
            crossoverPool = self.createCrossoverPool(matingPool)

            # Delete the previous population
            self.population.clear()

            # Create the portion of population that is undergone crossover and mutation
            print(len(crossoverPool), populationSize)
            for i in range(populationSize - int(populationSize*carryPercentage)):
                self.population.append(self.mutate(crossoverPool[i]))

            # Add the prominent chromosomes directly to next generation
            self.population.extend(carriedChromosomes)

    def createMatingPool(self):
        # TODO make a brand new custom pool to accentuate prominent chromosomes (optional)
        matingPool = []
        customPool = [self.population[i] for i in self.sortedInd[:int(
            populationSize*nextGenParentPercentage)]]
        # TODO create the matingPool using custom pool created in the last step and return it
        for i in range(populationSize - int(populationSize*carryPercentage)):
            matingPool.append((random.choice(customPool),
                              random.choice(customPool)))
        return matingPool

    def createCrossoverPool(self, matingPool):
        crossoverPool = []
        for i in range(len(matingPool)):
            if random.random() > crossoverProbability:
                # TODO don't perform crossover and add the chromosomes to the next generation directly to crossoverPool
                if random.random() > 0.5:
                    crossoverPool.append(matingPool[i][1])
                else:
                    crossoverPool.append(matingPool[i][0])
            else:
                # TODO find 2 child chromosomes, crossover, and add the result to crossoverPool
                child = calCrossover(matingPool[i][0], matingPool[i][1])
                crossoverPool.append(child)
        return crossoverPool

    def mutate(self, chromosome):
        # TODO mutate the input chromosome
        return chromosome

    # def calcFitness(self, chromosome):
    #     # TODO define the fitness measure here


operands = [1, 2, 3, 4, 5, 6, 7, 8]
operators = ['+', '-', '*']
equationLength = 21
goalNumber = 18019

equationBuilder = EquationBuilder(
    operators, operands, equationLength, goalNumber)
equation = equationBuilder.findEquation()
print(equation)
