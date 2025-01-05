# Panchanga Calculator

A Python tool to calculate Panchanga (Hindu astrological almanac) elements for a given date and time with high precision.

## Table of Contents

- [Introduction](#introduction)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Astronomical Calculations](#astronomical-calculations)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This tool calculates the Panchanga elements such as Tithi, Nakshatra, Yoga, Karana, and Rashi for a specified date, time, and timezone. It uses the `ephem` library for astronomical computations.

## Dependencies

- `ephem`: For astronomical calculations.
- `datetime`: For date and time manipulations.
- `argparse`: For command-line argument parsing.

## Installation

Ensure you have Python 3.x installed. Install the required dependencies using pip:

```bash
pip install ephem
```

## Usage

Run the script from the command line with the required arguments:

```bash
python panchanga.py -d DD/MM/YYYY -t HH:MM -z [+/-]HH:MM
```

**Arguments:**

- `-d` or `--date`: Date in `DD/MM/YYYY` format.
- `-t` or `--time`: Time in `HH:MM` 24-hour format.
- `-z` or `--zone`: Timezone with respect to GMT in `[+/-]HH:MM` format.

**Example:**

```bash
python panchanga.py -d 25/12/2023 -t 12:00 -z +05:30
```

**Output:**

```
Tithi     : <Tithi Name>, <Shukla/Krishna> Paksha
Nakshatra : <Nakshatra Name>
Yoga      : <Yoga Name>
Karana    : <Karana Name>
Rashi     : <Rashi Name>
```

## Astronomical Calculations

### Tithi

Calculated based on the angular distance between the Moon and the Sun, divided by 12 degrees.

### Nakshatra

Determined by the Moon's ecliptic longitude, divided into 27 equal parts.

### Yoga

Calculated from the sum of the ecliptic longitudes of the Sun and the Moon, divided into 27 equal parts.

### Karana

Half of a Tithi, calculated based on the progress within the Tithi.

### Rashi

Determined by the Moon's ecliptic longitude, divided into 12 equal parts.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the GPL3 License.