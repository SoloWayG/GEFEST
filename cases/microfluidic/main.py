import timeit

from gefest.core.opt.gen_design_micro import design
from cases.microfluidic.configuration_standard import sd_domain, sd_sampler, sd_estimator,sd_optimizer
from cases.main_conf import opt_params

opt_params.is_closed = True
opt_params.pop_size = 35
opt_params.n_steps = 200
opt_params.n_polys = 4
opt_params.n_points = 10
opt_params.m_rate = 0.9
opt_params.c_rate = 0.6

# ------------
# GEFEST tools configuration
# ------------

domain, task_setup = sd_domain.configurate_domain(poly_num=opt_params.n_polys,
                                                  points_num=opt_params.n_points,
                                                  is_closed=opt_params.is_closed)

estimator = sd_estimator.configurate_estimator(domain=domain)
sampler = sd_sampler.configurate_sampler(domain=domain)
optimizer = sd_optimizer.configurate_optimizer(pop_size=opt_params.pop_size,
                                               crossover_rate=opt_params.c_rate,
                                               mutation_rate=opt_params.m_rate,
                                               task_setup=task_setup)

# ------------
# Generative design stage
# ------------

start = timeit.default_timer()
optimized_pop = design(n_steps=opt_params.n_steps,
                       pop_size=opt_params.pop_size,
                       estimator=estimator,
                       sampler=sampler,
                       optimizer=optimizer)
spend_time = timeit.default_timer() - start
print(f'spent time {spend_time} sec')
