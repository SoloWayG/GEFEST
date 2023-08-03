from copy import deepcopy

from gefest.tools.optimizers.GA.base_GA import BaseGA


class GA(BaseGA):
    """The class uses genetic algorithm during optimization process.
    Args:
        BaseGA (Callable): parent abstract class with main optimization methods
    """

    def step(self, population, performance, verbose=True, **kwargs):
        self.init_populations(population)
        self.init_fitness(performance)
        selected = self.roulette_selection()
        best_individs = deepcopy(population[:5])
        #selected =self.tournament_selection()
        self._pop = sorted(selected, key=lambda x: x.fitness)

        un_pop = set()
        self._pop = \
            [un_pop.add(str(ind.genotype)) or ind for ind in self._pop
             if str(ind.genotype) not in un_pop]

        self._pop.extend(self.reproduce(self._pop))
        pop_reproduced = self.reproduce(self._pop)
        population += best_individs
        population = [ind.genotype for ind in pop_reproduced]

        return population
