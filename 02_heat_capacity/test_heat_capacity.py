#!/usr/bin/env python3
"""Test which PyGCC heat-capacity option reproduces the published logK.

Published sources:
  * Boschetti and Awolayo (2026), Section 3.1 and Table 1, describe
    temperature-dependent "Mayer-Kelly" a, b, and c heat-capacity parameters.
  * Supplementary File 3, `thermo.250bars_copy.tdat`, supplies the Hectorite
    EXPECTED_LOGK values below.

PyGCC 1.4.0 spells the temperature-dependent API option `Maier-Kelley`.
"""

import numpy as np
import pygcc
from pygcc import calcRxnlogK


TOLERANCE = 5.1e-4
T_C = np.array([0.01, 25.0, 60.0, 100.0, 150.0, 200.0, 250.0, 300.0])
EXPECTED_LOGK = np.array(
    [24.1815, 22.1983, 19.3287, 16.6802, 14.3246, 12.7512, 11.6759, 10.8408]
)
HECTORITE = ["Hectorite", "4", "0", "0", "0", "2.7", "0", ".3", "0", ".3", "0"]


def calculate(heat_capacity_option):
    result = calcRxnlogK(
        T=T_C,
        P=np.full(T_C.size, 250.0),
        Specie="Clay",
        elem=HECTORITE,
        group="10A",
        ClayMintype="Smectite",
        Int_Mg_fract=0,
        Int_Li_fract=0,
        heatcap_approx=heat_capacity_option,
    )
    return np.asarray(result.logK)


print("PyGCC imported from:", pygcc.__file__)
print("Mineral: Hectorite; T (C):", T_C, "; pressure: 250 bar")
constant_logk = calculate("constant")
maier_kelley_logk = calculate("Maier-Kelley")
constant_error = np.max(np.abs(constant_logk - EXPECTED_LOGK))
maier_kelley_error = np.max(np.abs(maier_kelley_logk - EXPECTED_LOGK))
print("Published logK:              ", EXPECTED_LOGK)
print("PyGCC constant logK:         ", constant_logk)
print("PyGCC Maier-Kelley logK:     ", maier_kelley_logk)
print("Max error, constant:         ", constant_error)
print("Max error, Maier-Kelley:     ", maier_kelley_error)

assert constant_error <= TOLERANCE, "The constant-Cp calculation does not match."
assert maier_kelley_error > TOLERANCE, "Maier-Kelley unexpectedly matches."
print("ISSUE REPRODUCED: published logK matches constant Cp, not Maier-Kelley Cp.")
