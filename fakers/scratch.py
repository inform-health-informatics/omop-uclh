"""Faking data for OMOP

A factory function and a series of classes that can be called to generate fake
data
"""


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

    patient = Patient()
    spell = Spell()
    subspells = (Subspell(i) for i in range(n_subspells))

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
    pass


class Spell():
    pass


class Subspell(Spell):
    # imagine they're might be other subspells in the future
    period_type = 'criticalcare'
    pass


mrjones = fake_it(seed=42, n_subspells=1)
print(mrjones)
