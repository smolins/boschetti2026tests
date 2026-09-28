#!/usr/bin/env python3
"""Reproduce the temperature-header/logK mismatch in Supplementary File 3.

Published source:
  Boschetti and Awolayo (2026), Supplementary File 3,
  `thermo.250bars_copy.tdat`. Its header gives temperatures
  0.01, 25, 60, 100, 120, 150, 250, and 300 C at 250 bar. The Hectorite
  mineral record supplies the EXPECTED_LOGK values below.

The article body, Section 3.3, says logK was calculated with PyGCC over
0--300 C at a fixed pressure of 250 bar.
"""

import numpy as np
import pygcc
from pygcc import calcRxnlogK


TOLERANCE = 5.1e-4
HEADER_T_C = np.array([0.01, 25.0, 60.0, 100.0, 120.0, 150.0, 250.0, 300.0])
EFFECTIVE_T_C = np.array([0.01, 25.0, 60.0, 100.0, 150.0, 200.0, 250.0, 300.0])
EXPECTED_LOGK = np.array(
    [24.1815, 22.1983, 19.3287, 16.6802, 14.3246, 12.7512, 11.6759, 10.8408]
)
HECTORITE = ["Hectorite", "4", "0", "0", "0", "2.7", "0", ".3", "0", ".3", "0"]


def calculate(temperatures):
    result = calcRxnlogK(
        T=temperatures,
        P=np.full(temperatures.size, 250.0),
        Specie="Clay",
        elem=HECTORITE,
        group="10A",
        ClayMintype="Smectite",
        Int_Mg_fract=0,
        Int_Li_fract=0,
        heatcap_approx="constant",
    )
    return np.asarray(result.logK)


print("PyGCC imported from:", pygcc.__file__)
print("Mineral: Hectorite; pressure: 250 bar; heatcap_approx: constant")
header_logk = calculate(HEADER_T_C)
effective_logk = calculate(EFFECTIVE_T_C)
header_error = np.max(np.abs(header_logk - EXPECTED_LOGK))
effective_error = np.max(np.abs(effective_logk - EXPECTED_LOGK))
print("Supplement header T (C):", HEADER_T_C)
print("Candidate effective T (C):", EFFECTIVE_T_C)
print("Published logK:           ", EXPECTED_LOGK)
print("Calculated on header:     ", header_logk)
print("Calculated on effective:  ", effective_logk)
print("Max error, header grid:   ", header_error)
print("Max error, effective grid:", effective_error)

assert header_error > TOLERANCE, "Header grid unexpectedly matches the published values."
assert effective_error <= TOLERANCE, "Effective 150/200 C grid does not match."
print("ISSUE REPRODUCED: values labeled 120/150 C match calculations at 150/200 C.")
