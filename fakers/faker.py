"""Faking data for OMOP

A factory function and a series of classes that can be called to generate fake
data
"""
import datetime as dt
import numpy as np
import pandas as pd
from collections import namedtuple
import inspect
import fakers.TwoD
import fakers.OneD

ConceptKeys = namedtuple('ConceptKeys', [
    'concept_id',   # OMOP CDM concept ID
    'shortName',    # something you can type when writing code
    'FSN'           # fully specified name (as per SNOMED approach)
])


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

    # tuple rather than list since avoiding mutables as class variables
    # fakers1D = dict()
    fakers2D = dict()

    def __init__(self, patient, spell, subspells):
        self.patient = patient
        self.spell = spell
        self.subspells = subspells
        # generate the list of classes that can fake data
        # if not len(fakers.OneD):
        #     Faker.fakers1D = _multikey_dict_of_classes(fakers.OneD)
        if not len(Faker.fakers2D):
            Faker.fakers2D = self._multikey_dict_of_classes(fakers.TwoD)

    @staticmethod
    def _multikey_dict_of_classes(mod):
        """Returns a class object from the TwoD or OneD list if presented with either a concept code or a shortname

        [description]

        Arguments:
            mod {module} -- python module containing class definitions
        """
        _dict = dict()
        clsmembers = inspect.getmembers(mod, inspect.isclass)
        for string, cls in clsmembers:
            try:
                # - [ ] @FIXME: (2018-10-30) needs to work for 1d where there is
                #   no positional argument
                instance = cls(None)
                labels = instance.conceptkeys
                _dict.update(_dict.fromkeys(list(labels), cls))
            except (TypeError, AttributeError) as e:
                continue
        return _dict

    def fake_these(self, concepts, DSN=None):
        # - [ ] @TODO: (2018-10-26) fake a list of different variables
        for i, concept in enumerate(concepts):
            if i == 0:
                df = self.fake_this(concept, DSN)
            else:
                _df = self.fake_this(concept, DSN)
                _name, _vals = _df.iloc[:, 1].name, _df.iloc[:, 1].values
                df = df.assign(_tmp=_vals)
                df.rename(columns={'_tmp': _name}, inplace=True)
        return df

    def fake_this(self, concept, DSN=None):
        """Returns fake OneD or TwoD data

        Looks in the associated class definitions for the function to implement
        the fake data; throws warning if not found (method not implemented)

        Arguments:
            concept {[type]} -- [description]
            patient {[type]} -- [description]
            spell {[type]} -- [description]
        """

        # 2. Calls the simulate_data method from that class
        # match the object to the provided concept name
        # and instantiate with appropriate time series
        try:
            fake_ = Faker.fakers2D[concept](self.spell.ts)
        except KeyError as e:
            raise NotImplementedError(
                '{}: Simulation method not implemented'.format(concept))

        # 3. Returns the simulated data either as
        if DSN is None:
            # 3.1 pandas dataframe or scalar
            return fake_.simulate()
        else:
            # - [ ] @TODO: (2018-10-30) insert to the database specified by DSN and return a success statement
            raise NotImplementedError()


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
        # - [ ] @TODO: (2018-10-31) define a default value for each mandatory
        #   column of the person table

        # person_id                   INTEGER     NOT NULL ,
        self.person_id = np.random.randint(2147483647) #int4 max
        # gender_concept_id           INTEGER     NOT NULL ,
        int(pd.Series( dict(Male=8507, Female=8532)).sample())
        self.gender_concept_id = int(pd.Series(
            dict(Male=8507, Female=8532)).sample())
        # year_of_birth               INTEGER     NOT NULL ,
        self.year_of_birth = np.random.randint(low=1918, high=2018)
        # month_of_birth              INTEGER     NULL,
        # day_of_birth                INTEGER     NULL,
        # birth_datetime              TIMESTAMP   NULL,
        # race_concept_id             INTEGER     NOT NULL,
        race_concepts = [8515, 8516, 8522, 8527, 8552, 8557, 8657, 9178,
                         38003572, 38003573, 38003574, 38003575, 38003576, 38003577, 38003578,
                         38003579, 38003580, 38003581, 38003582, 38003583, 38003584, 38003585,
                         38003586, 38003587, 38003588, 38003589, 38003590, 38003591, 38003592,
                         38003593, 38003594, 38003595, 38003596, 38003597, 38003598, 38003599,
                         38003600, 38003601, 38003602, 38003603, 38003604, 38003605, 38003606,
                         38003607, 38003608, 38003609, 38003610, 38003611, 38003612, 38003613,
                         38003614, 38003615, 38003616]
        self.race_concept_id = int(pd.Series(race_concepts).sample())
        # ethnicity_concept_id        INTEGER     NOT NULL,
        self.ethnicity_concept_id = int(pd.Series(
            dict(HispanicOrLatino=38003563,
                 NotHispanicorLatino=38003564)).sample())
        # location_id                 INTEGER     NULL,
        # provider_id                 INTEGER     NULL,
        # care_site_id                INTEGER     NULL,
        # person_source_value         VARCHAR(50) NULL,
        # gender_source_value         VARCHAR(50) NULL,
        # gender_source_concept_id    INTEGER     NULL,
        # race_source_value           VARCHAR(50) NULL,
        # race_source_concept_id      INTEGER     NULL,
        # ethnicity_source_value      VARCHAR(50) NULL,
        # ethnicity_source_concept_id INTEGER     NULL

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
    def __init__(self, patient, los_mean=7, los_sd=3, los_max=365, cadence='6H'):
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
        self.cadence = cadence
        self.ts = self.gen_time_series(cadence=self.cadence)

    def __str__(self):
        return 'Spell: {:.2} days from {} to {}'.format(
            self.los_hours.total_seconds() / (24 * 60 * 60), self.start, self.stop)

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
# mrjones = fake_it(seed=42, n_subspells=1)
# print(mrjones)
# print(mrjones.patient)
# print(mrjones.patient.id_nhs)
# print(mrjones.spell.start)
# print(mrjones.spell.los_hours)
# print(mrjones.spell.stop)
# print(mrjones.spell.gen_time_series())

# for i in range(10):
#     # switch seed off for randomness
#     mrsjones = fake_it(seed=None, n_subspells=1)
#     print(mrsjones)
#     print(mrsjones.patient)
#     print(mrsjones.patient.id_nhs)
#     print(mrsjones.spell.start)
#     print(mrsjones.spell.los_hours)
#     print(mrsjones.spell.stop)
