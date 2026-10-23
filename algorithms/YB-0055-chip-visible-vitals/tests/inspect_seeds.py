'''Descriptive look at the recordings before pre-registration: no model, no score, no threshold. It prints
wrong-answer counts and available fields for whatever seeds are passed, which may include the test seeds;
that is a descriptive peek at the labels, not a score and not a pre-registered number. The design
(PREREGISTRATION.md) does not depend on these counts; it states only that the single primary seed is
underpowered and the pooled secondary is the informative check.'''
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from recordings import load_seed
for s in [int(a) for a in sys.argv[1:]]:
    L = load_seed(s); a = [r for r in L if r['answered']]
    print(s, len(L), sorted(L[0].keys()) if s == int(sys.argv[1]) else '')
    print(' answered', len(a), 'wrong', sum(not r['correct'] for r in a), 'power nonnull', sum(r.get('power') is not None for r in L),
          'final_start>48', sum(r['final_start'] > 48 for r in a), 'cats', sorted(set(r['cat'] for r in L)))
    p = [r['power'] for r in L if r.get('power') is not None]
    if p: print(' power sample', str(p[0])[:200])
