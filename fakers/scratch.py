"""Faking data for OMOP

A factory function and a series of classes that can be called to generate fake
data
"""
import numpy as np
import datetime as dt


def fake_it(seed=42, n_subspells=1):
    """Factory function that builds up an instance of a spell

    An OMOP visit (equivalent to an NHS spell) is the fundamental unit necessary
    to write data into the OMOP CDM. This means creating
    - a patient (we need a patient identifier)
    - visit with a start and a stop timestamp
    - a critical care (sub)spell (for our purposes) (of which they're might be
      more than one)

    We can optionally override the default seed to generate different outputs

    Keyword Arguments:
        seed {number} -- [description] (default: {42})
        n_subspells {number} -- [description] (default: {1})
    """
    np.random.seed(seed)

    patient = Patient()
    spell = Spell(patient)
    subspells = (Subspell(spell, patient, i) for i in range(n_subspells))

    # - [ ] @TODO: (2018-10-26) enhanced data for OMOP plus
    # location (care_site) at ward level
    # bed (specific ward bed within care_site)
    # finished consultant episodes

    return Faker(patient, spell, subspells)


class Faker():
    def __init__(self, patient, spell, subspells):
        self.patient = patient
        self.spell = spell
        self.subspells = subspells
        pass


class Patient():
    """Group and define patient level attributes

    e.g.
    - name
    - date of birth
    - hospital number (modelled to look like UCLH)
    - NHS number
    These need to be defined before the spell since you can't be born during an
    admission!
    """

    def __init__(self):
        self.id_mrn = '4{:07}'.format((np.random.randint(10000000)))
        self.id_nhs = '{:03} {:04} {:04}'.format(
            np.random.randint(1000),
            np.random.randint(10000),
            np.random.randint(10000))
        # - [ ] @TODO: (2018-10-26) implement dob paying attention that age will
        #   affect spell dates since you can't be admitted before you are born
        #   or after you die!

    def __str__(self):
        # str is the pretty version / repr is the dev version
        return 'UCLH patient MRN {}'.format(self.id_mrn)


class Spell():
    """A period of care delivered by a single care provider

    This is equivalent to an OMOP visit

    Variables:
        pass {[type]} -- [description]
    """

    def __init__(self, patient):

        los_days = min(np.random.lognormal(1.5,1.), 365)
        self.los_hours = dt.timedelta(hours=los_days*24)
        self.start = dt.datetime.utcnow() - dt.timedelta(hours = np.random.uniform(0.0, 24*(365 - los_days))) - self.los_hours
        self.stop = self.start + self.los_hours


class Subspell(Spell):
    # imagine they're might be other subspells in the future
    period_type = 'criticalcare'
    pass


# - [ ] @TODO: (2018-10-26) implement tests for this class
# testing
mrjones = fake_it(seed=42, n_subspells=1)
print(mrjones)
print(mrjones.patient)
print(mrjones.patient.id_nhs)
print(mrjones.spell.start)
print(mrjones.spell.los_hours)
print(mrjones.spell.stop)

for i in range(10):
    # switch seed off for randomness
    mrsjones = fake_it(seed=None, n_subspells=1)
    print(mrsjones)
    print(mrsjones.patient)
    print(mrsjones.patient.id_nhs)
    print(mrsjones.spell.start)
    print(mrsjones.spell.los_hours)
    print(mrsjones.spell.stop)

