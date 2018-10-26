import numpy as np
import datetime as dt


class Patient():
    """Patient class

    Patient specific data model
    Should be the ancestor of visit (NHS 'spell')
    with respect to OMOP you then need a critical care 'spell'
    """

    def __init__(self):

        self.mrn = '{:06}'.format((np.random.randint(1, high=1000)))
        self.t0 = dt.datetime.utcnow()
        self.t_now = self.t0
        self.t_step = dt.timedelta(hours=1)  # time interval
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


class Spell(Patient):
    """NHS data dictionary secondary care provision

    - period of care provided by a secondary care provider not limited to a single
    - physical location would contain multiple finished consultant episodes
      aligns with the OMOP defintion of 'visit' provided at an organisational
      'care site'
    - anticipate that patients would move between different physical locations
      including ward to ward and distinct addresses during that period

    Extends:
        Patient
    """
    pass


class FinishedConsultantEpisode():
    pass

class CriticalCareSpell(Spell):
    """Time period within a spell during which a patient recieves critical care

    Corresponds to a critical care spell
    Might contain multiple different periods of care in different physical locations

    Extends:
        Spell
    """
    pass



# - [ ] @TODO: (2018-10-26) test class initiation
# - [ ] @TODO: (2018-10-26) implement a time invariant example PBC
# - [ ] @TODO: (2018-10-26) implement a time varying example (Lactate)

mrjones = Patient()
mrjones.t_step
mrjones.t0
mrjones.measure()
[mrjones[i] for i in range(3)]
mrjones[]
mrjones.t_now
mrjones.lactate
mrjones.measure()
mrjones.t_now
mrjones.lactate
