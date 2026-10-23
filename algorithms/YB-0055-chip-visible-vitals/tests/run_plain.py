'''Runs every test_* function in tests/test_*.py with plain python3, so CI needs no pytest (the CI image installs
numpy, scikit-learn and requests only). Fails if a test fails or if no test was found, so it can never pass empty.'''
import glob, importlib.util, os, sys, traceback
here = os.path.dirname(os.path.abspath(__file__))
ran, bad = 0, 0
for path in sorted(glob.glob(os.path.join(here, 'test_*.py'))):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    for name in sorted(n for n in dir(mod) if n.startswith('test_') and callable(getattr(mod, n))):
        ran += 1
        try:
            getattr(mod, name)(); print('PASS', name)
        except Exception:
            bad += 1; print('FAIL', name); traceback.print_exc()
print('%d/%d tests passed' % (ran - bad, ran))
sys.exit(1 if bad or not ran else 0)
