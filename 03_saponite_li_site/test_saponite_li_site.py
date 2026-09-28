#!/usr/bin/env python3
"""Test which Li-site assignment reproduces published Saponite-Li-int logK.

Published sources:
  * Boschetti and Awolayo (2026), Table 1, gives Saponite-Li-int as
    (Li0.33)(Mg3)(Si3.67Al0.33)O10(OH)2: Li is in the first, interlayer site.
  * Supplementary File 3, `thermo.250bars_copy.tdat`, supplies the
    Saponite-Li^int EXPECTED_LOGK values below.

In PyGCC 1.4.0, `Int_Li_fract` is the fraction of total Li assigned to the
interlayer: 1 means all interlayer and 0 means all octahedral.
"""

import numpy as np
import pygcc
from pygcc import calcRxnlogK


TOLERANCE = 5.1e-4
T_C = np.array([0.01, 25.0, 60.0, 100.0, 150.0, 200.0, 250.0, 300.0])
EXPECTED_LOGK = np.array(
    [34.7999, 31.3519, 26.8560, 22.7437, 18.9420, 16.1997, 14.1352, 12.4230]
)
SAPONITE = ["Saponite-Li^int", "3.67", ".33", "0", "0", "3", "0", "0", "0", ".33", "0"]


def calculate(interlayer_li_fraction):
    return calcRxnlogK(
        T=T_C,
        P=np.full(T_C.size, 250.0),
        Specie="Clay",
        elem=SAPONITE,
        group="10A",
        ClayMintype="Smectite",
        Int_Mg_fract=0,
        Int_Li_fract=interlayer_li_fraction,
        heatcap_approx="constant",
    )


print("PyGCC imported from:", pygcc.__file__)
print("Mineral: Saponite-Li^int; T (C):", T_C, "; pressure: 250 bar")
octahedral = calculate(0)
interlayer = calculate(1)
octahedral_error = np.max(np.abs(np.asarray(octahedral.logK) - EXPECTED_LOGK))
interlayer_error = np.max(np.abs(np.asarray(interlayer.logK) - EXPECTED_LOGK))
print("Published Table 1 formula:       (Li0.33)(Mg3)(Si3.67Al0.33)O10(OH)2")
print("PyGCC formula, Int_Li_fract=0: ", octahedral.Rxn["struct_formula"])
print("PyGCC formula, Int_Li_fract=1: ", interlayer.Rxn["struct_formula"])
print("Published logK:                 ", EXPECTED_LOGK)
print("Octahedral-Li logK:             ", octahedral.logK)
print("Interlayer-Li logK:             ", interlayer.logK)
print("Max error, octahedral Li:       ", octahedral_error)
print("Max error, interlayer Li:       ", interlayer_error)

assert octahedral_error <= TOLERANCE, "Octahedral-Li calculation does not match."
assert interlayer_error > TOLERANCE, "Interlayer-Li calculation unexpectedly matches."
print("ISSUE REPRODUCED: Saponite-Li-int logK matches octahedral, not interlayer Li.")
