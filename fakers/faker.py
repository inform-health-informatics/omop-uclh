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
    """Creates fake patient data to enter into OMOP

    Once provided with patient and spell information then makes available
    functions to generate fake 1d and 2d data
    """

    def __init__(self, patient, spell, subspells):
        self.patient = patient
        self.spell = spell
        self.subspells = subspells

    def fake_these(self, conc, DSN=None):
        # - [ ] @TODO: (2018-10-26) fake a list of different variables
        pass

    def fake_this(self, concept, DSN=None):
        """Returns fake OneD or TwoD data

        Looks in the associated class definitions for the function to implement
        the fake data; throws warning if not found (method not implemented)

        Arguments:
            concept {[type]} -- [description]
            patient {[type]} -- [description]
            spell {[type]} -- [description]
        """

        # 1. Find a class corresponding to the type of variable that needs to be faked
        # - [ ] @TODO: (2018-10-26) expects string representing class name; permit reference by concept ID too

        # 2. Calls the simulate_data method from that class

        # 3. Returns the simulated data either as
        # 3.1 pandas dataframe or scalar
        # 3.2 writes the data to the database specified by DSN and return a success statement
        return 'foobar'


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

    # - [ ] @TODO: (2018-10-26) you need patient passed through to for birth/death checks against spell; not yet implemented
    def __init__(self, patient, los_mean=7, los_sd=3, los_max=365):
        """Set up spell

        Derive start and stop of spell using a lognormal distribution

        Arguments:
            patient {Patient object} -- Patient object needed to manage birth/death checks

        Keyword Arguments:
            los_mean {number} -- mean length of stay in days (default: {7})
            los_sd {number} -- sd length of stay in days (default: {3})
        """

        _los_days = self._gen_los_days(los_mean, los_sd, los_max)
        self.los_hours = dt.timedelta(hours=_los_days * 24)
        self.start = (dt.datetime.utcnow()
                      - dt.timedelta(hours=np.random.uniform(0.0,
                                                             24 * (365 - _los_days)))
                      - self.los_hours)
        self.stop = self.start + self.los_hours

    def __str__(self):
        return 'Spell: {:.2} days from {} to {}'.format(
            self.los_hours.total_seconds()/(24*60*60), self.start, self.stop)

    @staticmethod
    def _gen_los_days(los_mean, los_sd, los_max):
        # Convert length of stay parameters to those needed for lognormal
        # see https://www.mathworks.com/help/stats/lognpdf.html
        # max capped at 365 days

        # - [ ] @TODO: (2018-10-26) convert to docstring to test @later
        # np.random.seed(seed=None)
        # np.std([_gen_los_days(7, 3) for i in range(100000)])

        _los_mu = np.log(los_mean**2 / ((los_sd**2 + los_mean**2)**0.5))
        _los_sd = (np.log((los_sd**2 / los_mean**2) + 1))**0.5
        return min(np.random.lognormal(_los_mu, _los_sd), los_max)

    def gen_time_series(self, cadence=None):
        # return times by natural cadence
        # - daily bloods
        # - regular ward obs
        # - close monitoring in critical care
        # - [ ] @TODO: (2018-10-26) implement missingness
        # - [ ] @ENHANCEMENT: (2018-10-26) implemnent jitter so times don't line up

        # default cadence
        if cadence is None:
            cadence = '1D'

        ts = pd.date_range(self.start, self.stop, freq=cadence)

        return ts


# - [ ] @TODO: (2018-10-26) not yet implemented
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
print(mrjones.spell.gen_time_series())

for i in range(10):
    # switch seed off for randomness
    mrsjones = fake_it(seed=None, n_subspells=1)
    print(mrsjones)
    print(mrsjones.patient)
    print(mrsjones.patient.id_nhs)
    print(mrsjones.spell.start)
    print(mrsjones.spell.los_hours)
    print(mrsjones.spell.stop)
