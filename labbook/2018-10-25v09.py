import numpy as np
import datetime as dt

class Patient():

    def  __init__(self):

        self.mrn = '{:06}'.format((np.random.randint(1,high=1000)))
        self.t0 = dt.datetime.utcnow()
        self.t_now = self.t0
        self.t_step = dt.timedelta(hours=1) # time interval
        self.lactate = 1


    def measure(self):
        while True:
            yield self.t_now, self.lactate
            self.t_now += self.t_step
            self.lactate = np.random.lognormal()

    def __getitem__(self, index):
        t = self.t0 + index * self.t_step
        lactate = np.random.lognormal()
        return (t, lactate)



    def __repr__(self):
        return 'Patient MRN {}'.format(self.mrn)

mrjones = Patient()
mrjones.t_step
mrjones.t0
mrjones.measure()
[mrjones[i] for i in range(3) ]
mrjones[]
mrjones.t_now
mrjones.lactate
mrjones.measure()
mrjones.t_now
mrjones.lactate
