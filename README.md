# Lotto Tool MU

<div align="center">

[![Latest Version](https://img.shields.io/badge/Lotto%20Tool%20MU-0.1.0-blue)](https://github.com/MrTanoshii/Lotto-tool-mu)
[![CC0-1.0 License](https://img.shields.io/badge/License-GPL--3.0-blue)](https://github.com/MrTanoshii/Lotto-tool-mu/blob/main/LICENSE)
[![Python Check](https://github.com/MrTanoshii/Lotto-tool-mu/actions/workflows/python_check.yml/badge.svg)](https://github.com/MrTanoshii/Lotto-tool-mu/actions/workflows/python_check.yml)

</div>

## Usage

### Setup

Input your lotto tickets info in `./data/lotto_entries.txt`

The format is as follows:
`START_DATE, END_DATE, #1, #2, #3, #4, #5, #6`

Where the dates are in `YYYY-MM-DD` format.

#### Example `lotto_entries.txt`

```plaintext
2022-10-05, 2022-10-19, 02, 03, 23, 33, 37, 39
2022-10-19, 2022-10-19, 15, 20, 25, 30, 34, 39
```

### Running

```bash
# Windows
python -m src

#Linux
python3 -m src
```
