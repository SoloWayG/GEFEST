import timeit
import pickle
import numpy as np
from gefest.tools.estimators.simulators.sound_wave.sound_interface import SoundSimulator
from gefest.core.opt.gen_design_data_generator import design
from cases.main_conf import opt_params
from cases.sound_waves.sound_surr.configuration_exp import (
    sound_domain,
    sound_estimator,
    sound_optimizer,
    sound_sampler,
)
from gefest.tools.utils.count_files import count_files
from poly_from_point import poly_from_comsol_txt
from pathlib import Path
import os
import shutil
from cases.sound_waves.experements.microphone_points import Microphone


micro = Microphone().array()
point_cnt_mes = len(micro)

################################
new_path = f'Data_04_09'     #path to create new dir of experement iteration
###############################
if os.path.exists(new_path):#
    shutil.rmtree(new_path) #
os.makedirs(new_path)       #
# ------------
# GEFEST tools configuration
# ------------
root_path = Path(__file__).parent.parent.parent.parent
opt_params.is_closed = True
opt_params.pop_size = 1000
opt_params.n_steps = 20
opt_params.n_polys = 1
opt_params.n_points = 10
opt_params.m_rate = 0
opt_params.c_rate = 0
is_extra = True
LOSS = 'MSE'
micro = Microphone().array()
point_cnt_mes = len(micro)

def upload_file(path: str):
    with open(path, "rb") as f:
        file = pickle.load(f)
        f.close()
    return file
paths_for_plotting = ['cases/sound_waves/experements/1508_Random_7_stps_200/iter_0/bottom_square',
                      'cases/sound_waves/experements/1508_Random_6_stps_200/iter_0/bottom_square',
                      'cases/sound_waves/experements/1508_Random_5_stps_200/iter_0/bottom_square',
                      'cases/sound_waves/experements/1508_Random_8_stps_200/iter_0/bottom_square',
                      'cases/sound_waves/experements/1508_Random_4_stps_200/iter0/bottom_square_exp',
                      'cases/sound_waves/experements/1508_Random_3_stps_200/iter0/bottom_square_exp',
                      'cases/sound_waves/experements/1508_Random_2_steps_200/iter0/bottom_square_exp',
                      'cases/sound_waves/experements/1508_Random_1_stps_200/iter0/bottom_square_exp',
                     'cases/sound_waves/experements/1508_Random_8_stps_200/iter_0/bottom_triangle']

paths_for_plotting_evo = ['cases/sound_waves/experements/002_3107_roulette/iter_0/bottom_square',
                      'cases/sound_waves/experements/001_3107_roulette/iter_0/bottom_square',
                      'cases/sound_waves/experements/003_3107_roulette/iter_0/bottom_square',
                      'cases/sound_waves/experements/001_3107_tournament/iter_0/bottom_square',
                      'cases/sound_waves/experements/002_3107_tournament/iter_0/bottom_square',
                      'cases/sound_waves/experements/003_3107_tournament/iter_0/bottom_square',
                      'cases/sound_waves/experements/002_3107_roulette/iter_1/bottom_square',
                      'cases/sound_waves/experements/001_3107_roulette/iter_1/bottom_square',
                      'cases/sound_waves/experements/003_3107_roulette/iter_1/bottom_square',
                      'cases/sound_waves/experements/001_3107_tournament/iter_1/bottom_square',
                      'cases/sound_waves/experements/002_3107_tournament/iter_1/bottom_square',
                      'cases/sound_waves/experements/1_0908_roulette/iter0/bottom_square_exp'
                          ]

path_to_result = f'{root_path}/{paths_for_plotting_evo[2]}'


domain, _ = sound_domain.configurate_domain(
        poly_num=opt_params.n_polys,
        points_num=opt_params.n_points,
        is_closed=opt_params.is_closed,
    )
class SoundSimulator_(SoundSimulator):
    def __init__(self, domain):
        super().__init__(domain)
        self.duration = 400
        self.pressure_hist = np.zeros((self.duration, self.size_y, self.size_x))

    def estimate(self, structure):
        spl = super().estimate(structure)
        spl_matrix = np.nan_to_num(spl,nan=0,neginf=0,posinf=0)
        #spl_mask = np.where(spl_matrix!=0,1,spl_matrix)
        return spl_matrix

estimator = SoundSimulator_(domain)
lenght = count_files(path =f'{path_to_result}', like ='optimized_structure_')
archs = count_files(path =f'{path_to_result}/History_0', like ='performance_')
pwd = os.getcwd()
dir_name = os.path.basename(pwd)
best_samples =[]


def _save_res(spl, path,ind):
    """
    Saving results in pickle format
    :param performance: (List), performance of samples
    :param samples: (List), samples to save
    :return: None
    """
    with open(Path(path, f'matrix_spl_{ind}.pickle'), 'wb') as handle:
        pickle.dump(spl, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return


for a in range(lenght):
    pop_path_2 = ([f"{path_to_result}/History_{a}/population_{i}.pickle" for i in range(archs)])
    samples = ([upload_file(i)[0] for i in pop_path_2])
    path_to_save = f"{path_to_result}/History_{a}"
    #fitness = list(np.array(fitness)/np.max(np.array(fitness)))#Normed loss
    #best_samples.append(samples[-1][0])
    [_save_res(spl=estimator.estimate(s),path=path_to_save,ind=ind) for ind,s in enumerate(samples)]
#
# #--#
# ls = os.listdir(path=f'{path_to_result}')
# lenght = 0
# for i in ls:
#     if 'optimized_structure_' in i:
#         lenght+=1
# init_path = f"{path_to_result}/best_structure.pickle"
# optimized_paths = [f"{path_to_result}/optimized_structure_{i}.pickle" for i in range(lenght)]
#
#
#
#
#
# sampler = sound_sampler.configurate_sampler(domain=domain)
#
# # optimizer = sound_optimizer.configurate_optimizer(
# #     pop_size=opt_params.pop_size,
# #     crossover_rate=opt_params.c_rate,
# #     mutation_rate=opt_params.m_rate,
# #     task_setup=task_setup,
# #     evolutionary_operators=point_crossover
# # )
# optimizer =False
# # ------------
# # Generative design stage
# # ------------
#
# #start = timeit.default_timer()
# optimized_pop = design(
#     n_steps=opt_params.n_steps,
#     pop_size=opt_params.pop_size,
#     estimator=estimator,
#     sampler=sampler,
#     optimizer=optimizer,
#     extra=is_extra,
#     path=new_path+f'/History',
#     extra_break=opt_params.n_steps
# )
#
# # with open(new_path+f"/optimized_structure_{i}.pickle", "wb") as handle:
# #     pickle.dump(optimized_pop, handle, protocol=pickle.HIGHEST_PROTOCOL)


