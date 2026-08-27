#!/usr/bin/env python3
import copy,importlib.util,math
from pathlib import Path
spec=importlib.util.spec_from_file_location('cli',Path(__file__).with_name('r2_qualification_cli_v3_17.py')); cli=importlib.util.module_from_spec(spec); spec.loader.exec_module(cli)
rows=cli.load(Path(__file__).with_name('fixtures')/'r2_voc_intensity_qualification_v3_17_pass.csv')

def expect(name,mutator,gate):
    x=copy.deepcopy(rows); mutator(x); c=cli.assess(x)
    assert c['overall_status']=='FAIL',(name,c['overall_status'])
    assert gate in c['failed_gates'],(name,c['failed_gates'])
    print('PASS',name,gate)

def nonanchor(x): return [r for r in x if not cli.b(r['anchor_flag'])]
expect('point_noise',lambda x:[r.__setitem__('voc_u_V','0.001') for r in nonanchor(x)],'point_voc_sd')
expect('temperature',lambda x:[r.__setitem__('dut_temperature_K','301') for r in nonanchor(x)],'temperature_excursion')
def ref(x):
    a=[r for r in x if cli.b(r['anchor_flag'])]; a[-1]['reference_signal_raw']='101000'
expect('reference_drift',ref,'reference_anchor_drift')
def vocd(x):
    a=[r for r in x if cli.b(r['anchor_flag'])]; a[-1]['voc_V']='0.902'
expect('voc_drift',vocd,'voc_anchor_drift')
def hyst(x):
    for r in nonanchor(x):
        if r['sweep_direction']=='descending': r['voc_V']=str(float(r['voc_V'])+0.002)
expect('hysteresis',hyst,'sweep_median_voc_difference')
def spectral(x):
    for r in nonanchor(x): r['spectral_mismatch_factor']='1.03'
expect('spectral_mismatch',spectral,'spectral_mismatch')
def cal(x):
    rr=nonanchor(x); vals=sorted({float(r['target_suns']) for r in rr}); lo,hi=math.log(vals[0]),math.log(vals[-1]); mid=.5*(lo+hi); span=.5*(hi-lo)
    for r in rr:
        p=float(r['target_suns']); z=(math.log(p)-mid)/span; r['calibrated_suns']=str(p*math.exp(0.012*z*z))
expect('calibration_shape',cal,'calibration_residual')
# Independent analytic gain check: x_m=(1+a)x -> contrast measured=true/(1+a)
t=[.05*(2/.05)**(i/16) for i in range(17)]; a=.005; m=[p**(1+a) for p in t]
bias=cli.cal_bias(t,m); expected=cli.STRESS/(1+a)-cli.STRESS
assert abs(bias-expected)<1e-10,(bias,expected)
print('PASS analytic_log_gain_crosscheck',bias)
# Missing spectrum metadata must not silently pass.
x=copy.deepcopy(rows)
for r in nonanchor(x): r['source_spectrum_id']=''
c=cli.assess(x); assert c['overall_status']=='INCOMPLETE' and 'spectral_mismatch' in c['incomplete_gates']
print('PASS missing_spectrum_is_incomplete')
