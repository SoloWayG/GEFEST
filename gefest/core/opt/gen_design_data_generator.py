import os
import shutil
import pickle
from copy import deepcopy

from tqdm import tqdm
from pathlib import Path


def design(n_steps: int,
           pop_size: int,
           estimator,
           sampler,
           optimizer,
           extra=False,
           path = 'HistoryFiles',
           extra_break=250):
    """
    Generative design procedure
    :param n_steps: (Int) number of generative design steps
    :param pop_size: (Int) number of samples in population
    :param estimator: (Object) estimator with .estimate() method
    :param sampler: (Object) sampler with .sample() method
    :param optimizer: (Object) optimizer with .optimize() method
    :param extra: (Bool) flag for extra sampling
    :return: (List[Structure]) designed samples
    """

    def _save_res(spl_matrix, samples,spl_mask,path):
        """
        Saving results in pickle format
        :param performance: (List), performance of samples
        :param samples: (List), samples to save
        :return: None
        """


        with open(Path(path, f'spl_matrix_{i}.pickle'), 'wb') as handle:
            pickle.dump(spl_matrix, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(Path(path, f'population_{i}.pickle'), 'wb') as handle:
            pickle.dump(samples, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(Path(path, f'spl_mask_{i}.pickle'), 'wb') as handle:
            pickle.dump(spl_mask, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return

    def _remain_best(performance, samples, dice_metric):
        """
        From current population we remain best only
        :param performance: (List), performance of samples
        :param samples: (List), samples to save
        :return: (Tuple), performance and samples
        """
        # Combination of performance and samples
        perf_samples = list(zip(performance, samples, dice_metric))

        # Sorting with respect to performance
        sorted_pop = sorted(perf_samples, key=lambda x: x[0])[:pop_size]

        performance = [x[0] for x in sorted_pop]
        samples = [x[1] for x in sorted_pop]
        dice_metric = [x[2] for x in sorted_pop]

        return performance, samples, dice_metric

    path = path
    path_data = path+'/Data'

    if os.path.exists(path_data):
        shutil.rmtree(path_data)
    os.makedirs(path_data)

    samples = sampler.sample(n_samples=pop_size)


    for i in range(n_steps):
        spl_matrixs, spl_masks =[],[]
        for s in samples:
            spl_matrix, spl_mask = estimator.estimate(s)
            spl_matrixs.append(spl_matrix)
            spl_masks.append(spl_mask)
        #spl_matrix,spl_mask = [estimator.estimate(s) for s in samples]
        _save_res(spl_matrixs, samples,spl_masks ,path=path_data)
        # Choose best and save the results
        #performance, samples, dice_metric = _remain_best(performance, samples,dice_metric)
        #print(f'\nBest performance is {performance[0]},dice is {dice_metric[0]}')
        #best_individs = deepcopy(samples[:3])
        #_save_res(performance, samples, dice_metric,path=path)
        samples = sampler.sample(n_samples=pop_size)
    return samples
