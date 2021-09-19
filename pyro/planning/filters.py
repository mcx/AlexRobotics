# -*- coding: utf-8 -*-"""Created on Sun Mar  6 15:09:12 2016@author: alex"""###############################################################################import scipy.signal as signal                       ###############################################################################class TrajectoryFilter:    """ Low pass filter function for discrete data array """        ############################    def __init__(self, fc = 5 , dt = 0.01 ):        """        Low Pass filter                fc : cutoff   freq [Hz]        fs : sampling fred [Hz]        dt : sampling period [sec]                ------------------        use:                filtered_data = low_pass.filter_array( data )                """                self.fc    = fc        self.fs    = 1.0 / dt        self.order = 2                self.setup()            ############################    def setup(self):        """ compute intermediate parametes """                wn = 2 * self.fc / self.fs                self.b , self.a  = signal.butter( self.order, wn, btype = 'low' )                    ############################    def set_freq_to(self, fc = 10 , dt = 0.01 ):        """ Recomputed filter given a new cutoff fred """                self.fc    = fc        self.fs    = 1.0 / dt        self.setup()                    ############################    def low_pass_filter_traj(self, traj ):                filtered_traj = traj.copy()                filtered_traj.x  = signal.filtfilt( self.b, self.a, traj.x.T ).T        filtered_traj.dx = signal.filtfilt( self.b, self.a, traj.dx.T ).T        filtered_traj.y  = signal.filtfilt( self.b, self.a, traj.y.T ).T        filtered_traj.u  = signal.filtfilt( self.b, self.a, traj.u.T ).T                return filtered_traj        