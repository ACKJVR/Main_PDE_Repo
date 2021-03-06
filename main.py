import numpy as np
from src import grid
from src import gridoperator
from src import static_bcs
from src import dirichlet_hand
from src import logger
from src import forward_euler
from src import conduct_heat_eqn
from src import spatial_driver
from src import driver
from src import vis_gif_2d
from src import plot_end
import initializer

gspec = grid.CartesianGridSpec(initializer.coords)
grid_u = grid.GridScalar(gspec,initializer.u)  # initial grid of temperature values

laplace_op = gridoperator.GridOperator(gspec, initializer.laplace_scheme)
ops_dict = {'laplacian': laplace_op}

#set each of the boundaries (using all dirichlet zero for now)
BCs = []
# BCs.append(static_bcs.Dirichlet(0,'l',np.array([1])))
# BCs.append(static_bcs.Dirichlet(0,'r',np.array([0])))
BCs.append(static_bcs.Dirichlet(0,'l',np.zeros(grid_u.shape[0])))
BCs.append(static_bcs.Dirichlet(0,'r',np.zeros(grid_u.shape[0])))
BCs.append(static_bcs.Dirichlet(1,'l',np.zeros(grid_u.shape[0])))
BCs.append(static_bcs.Dirichlet(1,'r',np.zeros(grid_u.shape[0])))

bound_handlr = dirichlet_hand.DirichletHand(BCs)

data_logger = logger.Logger()

time_stpr = forward_euler.ForwardEuler()

prblm = conduct_heat_eqn.ConductHeatEqn(bound_handlr, alpha=0.05)

prblm.set_ops(ops_dict)

space_drive = spatial_driver.SpatialDriver(prblm, data_logger)

drive = driver.Driver(space_drive, time_stpr)

drive.full_solve(initializer.t_start, initializer.t_end, initializer.dt, grid_u)

visualizer = plot_end.PlotEnd(initializer.out_loc)

visualizer.plot2d(data_logger,name=initializer.out_name)

# visualizer = vis_gif_2d.VisGif2d(initializer.out_loc)
# visualizer.make_2d_movie(data_logger,name = initializer.out_name)
