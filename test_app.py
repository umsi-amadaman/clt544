from pathlib import Path
import numpy as np
from scipy.integrate import trapezoid
from clt_core import simulate,density
from streamlit.testing.v1 import AppTest
r=simulate(n=25,repetitions=5000,seed=544)
s=r['summary'].set_index('Population')
assert np.isclose(s.loc['Bimodal','Population SD'],3.9)
assert np.isclose(s.loc['Bimodal','Expected SE'],.78)
assert np.all(np.abs(s['Observed SD of means']/s['Expected SE']-1)<.04)
assert all(np.array_equal(r['samples'][k],simulate(n=25,repetitions=5000,seed=544)['samples'][k]) for k in r['samples'])
x=np.linspace(0,140,100000)
for name in r['samples']:assert abs(trapezoid(density(name,x,r),x)-1)<.002
one=simulate(n=1,repetitions=3000,seed=1)
assert np.array_equal(one['samples']['Bimodal'].mean(axis=1),one['samples']['Bimodal'].ravel())
app=AppTest.from_file(str(Path(__file__).with_name('streamlit_app.py')),default_timeout=45).run()
assert not app.exception,app.exception
app.slider[0].set_value(100).run();assert not app.exception
app.radio[0].set_value('Full original panel').run();assert not app.exception
app.slider[1].set_value(0.).run();assert not app.exception
app.select_slider[0].set_value(20).run();assert not app.exception
print('PASS: analytic moments, normalized densities, reproducibility, n=1, Streamlit controls, full-panel view.')
