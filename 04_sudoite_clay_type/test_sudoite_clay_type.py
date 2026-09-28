#!/usr/bin/env python3
"""Test which PyGCC clay-mineral branch reproduces published Sudoite-Li logK.

Published sources:
  * Boschetti and Awolayo (2026), Section 3.1 calls Li-sudoite a Li-bearing
    chlorite; Table 1 gives the 14-A chlorite formula
    (Li0.3Mg1.7Al3.0)(Si3.3Al0.7)O10(OH)8.
  * Supplementary File 3, `thermo.250bars_copy.tdat`, labels Sudoite-Li
    `type=Chlorite` and supplies the EXPECTED_LOGK values below.
"""

import numpy as np
import pygcc
from pygcc import calcRxnlogK


TOLERANCE = 5.1e-4
T_C = np.array([0.01, 25.0, 60.0, 100.0, 150.0, 200.0, 250.0, 300.0])
EXPECTED_LOGK = np.array(
    [41.2998, 34.4312, 26.1356, 18.6918, 11.7154, 6.4733, 2.2912, -1.3737]
)
SUDOITE = ["Sudoite-Li", "3.3", "3.7", "0", "0", "1.7", "0", "0", "0", ".3", "0"]


def calculate(clay_mineral_type):
    return calcRxnlogK(
        T=T_C,
        P=np.full(T_C.size, 250.0),
        Specie="Clay",
        elem=SUDOITE,
        group="14A",
        ClayMintype=clay_mineral_type,
        Int_Mg_fract=0,
        Int_Li_fract=0,
        heatcap_approx="constant",
    )


print("PyGCC imported from:", pygcc.__file__)
print("Mineral: Sudoite-Li; group: 14A; T (C):", T_C, "; pressure: 250 bar")
smectite = calculate("Smectite")
chlorite = calculate("Chlorite")
smectite_error = np.max(np.abs(np.asarray(smectite.logK) - EXPECTED_LOGK))
chlorite_error = np.max(np.abs(np.asarray(chlorite.logK) - EXPECTED_LOGK))
print("Published type: Chlorite")
print("Published logK:          ", EXPECTED_LOGK)
print("Smectite-branch logK:    ", smectite.logK)
print("Chlorite-branch logK:    ", chlorite.logK)
print("Max error, Smectite:     ", smectite_error)
print("Max error, Chlorite:     ", chlorite_error)

assert smectite_error <= TOLERANCE, "Smectite-branch calculation does not match."
assert chlorite_error > TOLERANCE, "Chlorite-branch calculation unexpectedly matches."
print("ISSUE REPRODUCED: Sudoite-Li logK matches the Smectite, not Chlorite branch.")
