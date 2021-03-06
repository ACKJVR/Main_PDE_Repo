## \file spatial_driver.py

## \package spatial_driver
#  These objects drive the solution of the spatial part of the
#  PDE problem.
#
#  The spatial part of the problem corresponds to the right
#  hand side of the differential equation
#  du/dt = f( u, d^(n)u/dx^(n), d^(n)u/dy^(n) )
#  
#  The SpatialDriver is called by the main driver class and
#  itself calls the problem class and the boundary handler
#  objects in order to return an approximation for the
#  values of the right hand side to the data logger object.


## The SpatialDriver class
class SpatialDriver():

    ## The constructor for the SpatialDriver class.
    #  
    #  Initializes the spatial driver with a PDE problem object,
    #  a boundary handler, and a data logger object.
    #  \param pde_problem The PDE problem object
    #  \param logger The data logger object
    def __init__(self, pde_problem, logger):
        
        ## A PDE problem object
        self.pde_problem = pde_problem

        ## A data logger object
        self.logger = logger

    ## Set the spatial boundaries to the appropriate values
    #  based on the boundary conditions.
    #  
    #  This method simply calls the set_bound_vals() method of
    #  the boundary handler object. Returns the updated grid with
    #  the correct boundary values.
    #  \param t The current time
    #  \param val_grid The spatial grid of function values
    #  \return Updated grid with correct boundary values
    def set_BCs(self, t, val_grid):
        return self.pde_problem.set_BCs(t, val_grid)

    ## Evaluate the right hand side of the given PDE
    #  
    #  This method simply calls the RHS() method of the
    #  problem object. Returns the spatial grid of approximate
    #  RHS values.
    #  \param val_grid The spatial grid of function values
    #  \return The spatial grid of approximate RHS values
    def eval_rhs(self, val_grid):
        return self.pde_problem.RHS(val_grid)

    ## Send a spatial grid of function values to the data
    #  logger object.
    #  
    #  This method simply calls the log() method of the data
    #  logger object.
    #  \param t The current time step
    #  \param val_grid The spatial grid of function values
    def log_data(self, t, val_grid):
        self.logger.log(t, val_grid)
        return

    ## Perform the full sequence of spatial problem steps.
    #  1. Set boundary values
    #  2. Log the current time step and function values
    #  3. Evaluate the approximate RHS values
    #  
    #  This method calls the other methods defined in this
    #  class. Returns the input grid with updated boundary
    #  values and the grid of RHS values that will be
    #  passed to the time stepper.
    #  \param t The current time step
    #  \param val_grid A spatial grid object
    #  \return The spatial grid with correct boundary values
    #  \return The grid object to pass to the time stepper
    def solve(self, t, val_grid):
        self.set_BCs(t, val_grid)
        self.log_data(t, val_grid)
        return val_grid, self.eval_rhs(val_grid)
