# Failure Analyzer for FDM

A Python-based tool for analyzing the effects of mechanical loading on 3D-printed models.

---

## Table of Contents
- [Failure Analyzer for FDM](#failure-analyzer-for-fdm)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Features](#features)
  - [How to Use](#how-to-use)
  - [License](#license)
  - [Limitations](#limitations)

---

## About

This project is a Python-based tool designed to analyze the stiffness and strength of 3D-printed parts. It allows users to define a beam with multiple sections and evaluate whether the structure meets design requirements under various loading conditions.

---

## Features

- User-defined multi-sectional beam
- Supports four types of loading: transverse force, tensile force, bending moment, and torsion
- Easily modifiable for parameter iteration and design exploration

---

## How to Use

1. Download or clone the repository.
2. Run `main.py` using Python 3:
   ```bash
   python main.py
3. Follow the instructions displayed in the terminal.

## License
This project is licensed under the GNU License – see the LICENSE file for details.

## Limitations

This tool is intended as a guideline for estimating the upper boundary of structural behavior within the elastic regime.


It is best suited for cases where bending moment and transverse force are dominant. The effects of elongation due to tension and compression are neglected in the displacement analysis.