/* YB-0018 core: metabolic features from a sampled power trace (t_i seconds, P_i milliwatts, sorted by t).
 * out[0] energy (joules, trapezoid rule), [1] mean power (W, time-weighted), [2] peak power (W),
 * [3] power RMSSD (W, successive-difference variability), [4] duration covered (s). Returns 0, or 1 if n < 2. */
#include <math.h>

int power_features(const double *t, const double *p_mw, int n, double *out) {
    if (n < 2) return 1;
    double E = 0, pk = p_mw[0], d2 = 0;
    for (int i = 1; i < n; i++) {
        E += 0.5 * (p_mw[i] + p_mw[i - 1]) * (t[i] - t[i - 1]);
        if (p_mw[i] > pk) pk = p_mw[i];
        d2 += (p_mw[i] - p_mw[i - 1]) * (p_mw[i] - p_mw[i - 1]);
    }
    double dur = t[n - 1] - t[0];
    out[0] = E / 1000.0; out[1] = dur > 0 ? E / dur / 1000.0 : p_mw[0] / 1000.0; out[2] = pk / 1000.0;
    out[3] = sqrt(d2 / (n - 1)) / 1000.0; out[4] = dur;
    return 0;
}
