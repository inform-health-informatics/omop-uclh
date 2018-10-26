# testing fakers
mrjones = fake_it(seed=42, n_subspells=1)
print(mrjones.spell)
print(mrjones.spell.los_hours.total_seconds()/24/3600)
'{:.1}'.format(mrjones.spell.los_hours)
mrjones.fake_this('lactate')

twod = TwoD(mrjones.spell)
twod.gen_time_series()
lactates = Lactate(mrjones.spell).simulate(cadence='4H')

[np.random.lognormal() for i in twod.ts]

import pandas as pd
pd.date_range(mrjones.spell.start, mrjones.spell.stop, freq='6H')
