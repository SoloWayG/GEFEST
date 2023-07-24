import copy
import math
import random
from random import randint

import numpy as np

from gefest.core.opt.individual import Individual
from gefest.core.opt.setup import Setup
from gefest.core.viz.struct_vizualizer import StructVizualizer


class BaseGA:
    """The base optimization class.
    The class contains basic optimization functions which allow to use different
    way of optimization algorithm via legacy from the :obj:`class BaseGA`.
    """

    def __init__(self, params,
                 evolutionary_operators,
                 task_setup: Setup):
        """
         Genetic algorithm (GA)
        """

        self.params = params

        self.operators = evolutionary_operators

        self.task_setup = task_setup

        self.__init_operators()
        self._pop = []

        self.visualiser = StructVizualizer(self.task_setup.domain)

    def __init_operators(self):
        self.crossover = self.operators.crossover
        self.mutation = self.operators.mutation

    def init_populations(self, population):
        self._pop = [Individual(genotype=gen) for gen in population]

    def init_fitness(self, performance):
        for i, ind in enumerate(self._pop):
            ind.fitness = performance[i]
        self._pop = [ind for ind in self._pop if ind.fitness is not None]

    def init_performance(self, performance):
        for i, ind in enumerate(self._pop):
            ind.objectives = performance[i]
        self._pop = [ind for ind in self._pop if ind is not None]
        self.initial_graphs = self._pop

    class Params:
        def __init__(self, pop_size, crossover_rate, mutation_rate, mutation_value_rate):
            self.pop_size = pop_size
            self.crossover_rate = crossover_rate
            self.mutation_rate = mutation_rate
            self.mutation_value_rate = mutation_value_rate

    def solution(self, verbose=True, **kwargs):
        """Method for finding a solution via choosen algorithm
        Args:
            verbose: Full description of finding the best solution if ``True``, otherwise - ``False``. Defaults to True.
        """
        pass

    def random_selection(self, group_size):
        return [self._pop[randint(0, len(self._pop) - 1)] for _ in range(group_size)]
    def tournament_selection(self, fraction=0.1):
        """The method allows to select the best ones from whole population
        Args:
            fraction: value for separating the best part of population from another. Defaults to 0.1.
        Returns:
            The best individuals from given population. Their number is equal to ``'initial_number' * fraction``
        """
        group_size = math.ceil(len(self._pop) * fraction)
        min_group_size = 2 if len(self._pop) > 1 else 1
        group_size = max(group_size, min_group_size)
        chosen = []
        n_iter = 0
        while len(chosen) < self.params.pop_size:
            n_iter += 1
            group = self.random_selection(group_size)
            best = min(group, key=lambda ind: ind.fitness)
            if best not in chosen:
                chosen.append(best)
            elif n_iter > self.params.pop_size + 100:
                n_iter = 0
                rnd = self._pop[randint(0, len(self._pop) - 1)]
                chosen.append(rnd)
        return chosen



    def roulette_selection(self):
        """The method allows to select the best ones from whole population.
        relative probability based on reversed fitness
        Returns:
            The best individuals from given population. Their number is equal to ``'initial_number' * fraction``
        """
        _fitness = [i.fitness for i in self._pop]
        probability = [(i/(sum(_fitness))) for i in _fitness]
        probability = [(max(probability)/i) for i in probability]
        probability = [i/sum(probability) for i in probability]

        chosen=[]

        while len(chosen) < self.params.pop_size:
            chosen.append(np.random.choice(a=self._pop, p=probability))
        return chosen

    def reproduce(self, selected):
        """The method imitatess evolutionory reproduce process via apply
        `crossover` and `mutation` to given undividuals from population.
        Args:
            selected : the set of inviduals for reproducing
        Returns:
            reprodused individuals
        """
        children = []
        np.random.shuffle(selected)
        ####
        reproduced = []
        for _ in range(len(selected)):
            i1 = random.randint(0, len(selected)-1)#set random index
            i2 = random.randint(0, len(selected)-1)
            while i1!=i2 and i1 not in reproduced:
                i1 = random.randint(0, len(selected)-1)
                i2 = random.randint(0, len(selected)-1)
            reproduced.append(i1)
            p1 = selected[i1]
            p2 = selected[i2]
        ####
        # for pair_index in range(0, len(selected) - 1):
        #     p1 = selected[pair_index]
        #     p2 = selected[pair_index + 1]

            child_gen = self.crossover(s1=p1.genotype, s2=p2.genotype,
                                       domain=self.task_setup.domain,
                                       rate=self.params.crossover_rate)

            child_gen = self.mutation(structure=child_gen,
                                      domain=self.task_setup.domain,
                                      rate=self.params.mutation_rate)

            #if str(child_gen) != str(p1.genotype) and str(child_gen) != str(p2.genotype):#
            child = Individual(genotype=copy.deepcopy(child_gen))
            children.append(child)

        return children
