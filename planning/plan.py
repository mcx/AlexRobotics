# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 13:41:26 2018

@author: Alexandre
"""
###############################################################################
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3

###############################################################################
from AlexRobotics.dynamic  import system
from AlexRobotics.analysis import simulation
from AlexRobotics.control  import controller
from AlexRobotics.signal   import timefiltering


###############################################################################
class OpenLoopController( controller.StaticController ) :
    """    """
    ############################
    def __init__(self, sys):
        """ """
        
        # Sys
        self.sys = sys
        
        # Dimensions
        self.k = 1   
        self.m = sys.m
        self.p = sys.p
        
        controller.StaticController.__init__(self, self.k, self.m, self.p)
        
        # Label
        self.name = 'Value Iteration Controller'
        
        # Intit
        self.solution = None
        
    
    ############################
    def t2u(self, t ):
        """ get u from solution """
        
        if self.solution == None:
            
            u = self.sys.ubar
        
        else:
            
            # Find time index
            times = self.solution[2]
            i = (np.abs(times - t)).argmin()
            
            # Find associated control input
            u = self.solution[1][:,i]
            
            # No action pass trajectory time
            if t > self.time_to_goal:
                u    = self.sys.ubar
            
        return u

    #############################
    def c( self , y , r , t  ):
        """  U depends only on time """
        
        u = self.t2u( t )
        
        return u
    
    ############################
    def load_solution(self, name = 'RRT_Solution.npy' ):
        
        RRT.load_solution( self , name )
        
        

###############################################################################
class Trajectory() :
    """    """
    ############################
    def __init__(self, x , u , t , dx = None , y = None):
        """ 
        x: array of dim = ( time-steps , sys.n )
        u: array of dim = ( time-steps , sys.m )
        t: array of dim = ( time-steps , 1 )
        """
                
        self.x_sol  = x
        self.u_sol  = u
        self.t_sol  = t
        self.dx_sol = dx
        self.y_sol  = y
        
        self.time_to_goal    = t.max()
        self.solution_length = t.size
        
    ############################
    def save(self, name = 'trajectory_solution.npy' ):
        
        arr = np.array( [ self.x_sol , 
                          self.u_sol , 
                          self.t_sol ,
                          self.dx_sol,
                          self.y_sol ] )
        
        np.save( name , arr )
        
        
    ############################
    def load(self, name = 'trajectory_solution.npy' ):
        
        data = np.load( name )
        
        self.x_sol  = data[0]
        self.u_sol  = data[1]
        self.t_sol  = data[2]
        self.dx_sol = data[3]
        self.y_sol  = data[4]
        
        self.time_to_goal    = self.t_sol.max()
        self.solution_length = self.t_sol.size
        
    
    ############################
    def lowpassfilter( self , fc = 3 ):
        
        # Assuming time-step is constant
        dt = self.t_sol[1] - self.t_sol[0]
        
        self.low_pass_filter = timefiltering.LowPassFilter( fc , dt )

        self.x_sol  = self.low_pass_filter.filter_array( self.x_sol  )
        self.u_sol  = self.low_pass_filter.filter_array( self.u_sol  )
        
        if not(self.dx_sol == None):
            self.dx_sol  = self.low_pass_filter.filter_array( self.dx_sol  )
            
        if not(self.y_sol == None):
            self.y_sol  = self.low_pass_filter.filter_array( self.y_sol  )
            
        
    ############################
    def t2u(self, t ):
        """ get u from time """
        
        # Find time index
        i = (np.abs(self.t_sol - t)).argmin()
        
        # Find associated control input
        u = self.u_sol[i,:]
            
        return u
    
    ############################
    def t2x(self, t ):
        """ get x from time """
        
        # Find time index
        i = (np.abs(self.t_sol - t)).argmin()
        
        # Find associated control input
        x = self.x_sol[i,:]
            
        return x
    
    ############################
    def plot_trajectory(self, sys , params = 'xu' ):
        """  """
        
        sim = simulation.Simulation( sys , 
                                     self.time_to_goal , 
                                     self.solution_length )

        sim.x_sol = self.x_sol
        sim.t     = self.t_sol
        sim.u_sol = self.u_sol
        
        sim.plot( params )
        
        sys.sim = sim



   
###############################################################################
def load_trajectory( name = 'trajectory_solution.npy' ):
    
        data = np.load( name )
        
        return Trajectory( data[0] , data[1], data[2] , data[3] , data[4] )
        
        
        
        
        
        
        
        
        
        