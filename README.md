# PyGCC 1.4.0 reproduction tests for Boschetti and Awolayo (2026)

These four small, independent scripts reproduce discrepancies found while
rebuilding the Li-clay thermodynamic data reported by:

> Boschetti, T. and Awolayo, A.N. (2026), *Constraining lithium-clay
> equilibria in sedimentary environments using a new thermodynamic dataset*,
> Journal of Geochemical Exploration 280, 107920.

The tests use the downloaded PyGCC 1.4.0 source tree, the version named in
Section 3.1 of the article. Each script states the article or supplementary
source of every published value that it compares. The numerical reference is
Supplementary File 3, archive `thermo.250bars_copy.tdat`.

## Run

Run each script separately from any directory:

```bash
PYTHONPATH=$PYGCC/pygcc-1.4.0/src \
  python 01_temperature_grid/test_temperature_grid.py
```

Other test paths:

- `02_heat_capacity/test_heat_capacity.py`
- `03_saponite_li_site/test_saponite_li_site.py`
- `04_sudoite_clay_type/test_sudoite_clay_type.py`

Each script prints the imported `pygcc` path, all calculation choices, the
published and calculated logK arrays, and maximum absolute differences. A
successful run ends with `ISSUE REPRODUCED`, which means that the
script reproduced the reported discrepancy. It does not mean that the
publication and stated calculation agree.

The comparison tolerance is `5.1e-4` logK units. This is slightly larger than
half the last reported decimal place in the four-decimal supplementary data.

## Tests

1. **Temperature grid:** the Supplementary File 3 header labels the fifth and
   sixth points as 120 and 150 degrees C, but the logK values reported match
   PyGCC calculations at 150 and 200 degrees C.
2. **Heat-capacity treatment:** Section 3.1 and Table 1 discuss the
   temperature-dependent Maier-Kelley coefficients, whereas the supplementary
   logK values match those obtained with PyGCC's `constant` option, not its
   `Maier-Kelley` option. 
3. **Saponite Li site:** Table 1 places Li in the interlayer of
   Saponite-Li<sup>int</sup>, but its logK values match those from the
   octahedral-Li calculation (`Int_Li_fract=0`), not the interlayer calculation
   (`Int_Li_fract=1`).
5. **Sudoite mineral type:** Section 3.1 and Table 1 identify Sudoite-Li as a
   chlorite, but its supplementary logK values match PyGCC's `Smectite`
   calculation branch, not its `Chlorite` option.