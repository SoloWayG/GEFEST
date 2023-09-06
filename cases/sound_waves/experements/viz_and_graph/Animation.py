import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.image as mpimg
from cases.main_conf import opt_params
from cases.sound_waves.configuration import sound_domain
from gefest.tools.estimators.simulators.sound_wave.sound_interface import SoundSimulator
from cases.sound_waves.experements.microphone_points import Microphone
import numpy as np
from gefest.tools.utils.count_files import count_files
import os
from pathlib import Path
from matplotlib.animation import FuncAnimation
root_path = Path(__file__).parent.parent.parent.parent.parent
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


lenght = count_files(path =f'{path_to_result}', like ='optimized_structure_')
archs = count_files(path =f'{path_to_result}/History_0', like ='performance_')
pwd = os.getcwd()
dir_name = os.path.basename(pwd)
best_fit =[]
ls = os.listdir(path=f'{path_to_result}')
lenght = 0
for i in ls:
    if 'optimized_structure_' in i:
        lenght+=1
init_path = f"{path_to_result}/best_structure.pickle"
optimized_paths = [f"{path_to_result}/optimized_structure_{i}.pickle" for i in range(lenght)]

domain, _ = sound_domain.configurate_domain(
    poly_num=opt_params.n_polys,
    points_num=opt_params.n_points,
    is_closed=opt_params.is_closed,
)

init_structure = upload_file(init_path)
optimized_structures = [upload_file(i)[0] for i in optimized_paths]


class SoundSimulator_(SoundSimulator):
    def __init__(self, domain):
        super().__init__(domain)
        self.duration = 4
        self.pressure_hist = np.zeros((self.duration, self.size_y, self.size_x))


sound = SoundSimulator_(domain)

spl_matrix = upload_file(f"{path_to_result}/History_0/matrix_spl_90.pickle")
spl_matrix = np.where(spl_matrix==0,np.inf,spl_matrix)
spl_0 = sound.estimate(init_structure)

receivers = [9,64,240,'Full field']
micro = Microphone().array()
micro_p = Microphone.coords['points']
frames = count_files(path =f'{path_to_result}/History_0', like ='matrix_spl_')




fig = plt.figure(figsize=(6,18))
img = mpimg.imread(f'{root_path}/docs/img/gefest_logo.png')

ax1 = plt.subplot2grid((3,2), (0,0), colspan=1)
ax6 = plt.subplot2grid((3,2), (0,1), colspan=1)
ax2= plt.subplot2grid((3,2), (1,0), colspan=1)
ax3= plt.subplot2grid((3,2), (1,1), colspan=1)
ax4= plt.subplot2grid((3,2), (2,0), colspan=1)
ax5= plt.subplot2grid((3,2), (2,1), colspan=1)

ax6.imshow(img, aspect='equal')
ax6.axis('off')
im = ax1.pcolormesh(spl_0,cmap="coolwarm")
ax1.set_title('Reference object')
plt.colorbar(im, ax=ax1, label='dB', location='bottom', orientation='horizontal')


ax2.set_title('9 receivers')
im1 = ax2.pcolormesh(spl_0, cmap="coolwarm")
ax3.set_title('64 receivers')
im2 = ax3.pcolormesh(spl_0, cmap="coolwarm")
ax4.set_title('240 receivers')
im3 = ax4.pcolormesh(spl_0, cmap="coolwarm")
ax5.set_title('Full matrix')
im4 = ax5.pcolormesh(spl_0, cmap="coolwarm")
plt.colorbar(im1, ax=ax2, label='dB', location='bottom', orientation='horizontal')
plt.colorbar(im2, ax=ax3, label='dB', location='bottom', orientation='horizontal')
plt.colorbar(im3, ax=ax4, label='dB', location='bottom', orientation='horizontal')
plt.colorbar(im4, ax=ax5, label='dB', location='bottom', orientation='horizontal')


def spl_matrix_(iter,history):
    spl_matrix = upload_file(f"{path_to_result}/History_{history}/matrix_spl_{iter}.pickle")
    spl_matrix = np.where(spl_matrix == 0, np.inf, spl_matrix)
    return spl_matrix
def animate(iter):
    im1.set_array(spl_matrix_(iter,0))
    im2.set_array(spl_matrix_(iter, 1))
    im3.set_array(spl_matrix_(iter, 2))
    im4.set_array(spl_matrix_(iter, 3))

ani = FuncAnimation(fig, animate, frames=frames,repeat=False)
plt.show()