# محاسبه‌گر پانچانگا

ابزاری به زبان پایتون برای محاسبه عناصر پانچانگا (تقویم ودیک آسترولوژی) برای تاریخ و زمان مشخص با دقت بالا.

## فهرست مطالب

- [مقدمه](#مقدمه)
- [وابستگی‌ها](#وابستگیها)
- [نصب](#نصب) 
- [نحوه استفاده](#نحوه-استفاده)
  - [پانچانگا روزانه](#پانچانگا-روزانه)
  - [پانچانگا ماهانه](#پانچانگا-ماهانه)
  - [جستجوی موهورتا](#جستجوی-موهورتا)
- [محاسبات نجومی](#محاسبات-نجومی)
- [مشارکت](#مشارکت)
- [مجوز](#مجوز)

## مقدمه

این ابزار عناصر پانچانگا مانند تیتی، ناکشاترا، یوگا، کارانا و راشی را برای تاریخ، زمان و منطقه زمانی مشخص محاسبه می‌کند. از کتابخانه `ephem` برای محاسبات نجومی استفاده می‌شود.

## وابستگی‌ها

- `ephem`: برای محاسبات نجومی
- `datetime`: برای دستکاری تاریخ و زمان 
- `argparse`: برای تجزیه آرگومان‌های خط فرمان
- `jdatetime`: برای تبدیل تاریخ جلالی (اختیاری)

## نصب

اطمینان حاصل کنید که پایتون ۳.x نصب شده است. وابستگی‌های مورد نیاز را با pip نصب کنید:

```bash
pip install ephem jdatetime
```

## نحوه استفاده

ابزار سه حالت کار دارد:

### پانچانگا روزانه

محاسبه عناصر پانچانگا برای یک روز مشخص:

```bash
python daily_panchanga.py -d DD/MM/YYYY -t HH:MM -z [+/-]HH:MM [--calendar gregorian|jalali]
```

### پانچانگا ماهانه 

نمایش تقویم پانچانگا برای یک ماه کامل:

```bash
python monthly_panchanga.py --month MM --year YYYY -z [+/-]HH:MM
```

### جستجوی موهورتا

یافتن زمان‌های مناسب برای فعالیت‌های مختلف:

```bash  
python muhurtha_finder.py --action <نوع-فعالیت> --start DD/MM/YYYY --end DD/MM/YYYY -z [+/-]HH:MM
```

انواع فعالیت‌های قابل جستجو:
- marriage (ازدواج)
- house_warming (خانه تکانی)
- meeting (جلسه)

## محاسبات نجومی 

محاسبه عناصر پانچانگا بر اساس فرمول‌های نجومی دقیق انجام می‌شود:

- **تیتی**: فاز ماه، تقسیم به ۳۰ روز قمری
- **ناکشاترا**: موقعیت ماه در منازل قمری 
- **یوگا**: ترکیب موقعیت خورشید و ماه
- **کارانا**: نیمه تیتی
- **راشی**: صورت فلکی ماه

## مشارکت

از مشارکت‌های شما استقبال می‌کنیم! لطفاً یک Issue باز کنید یا Pull Request ارسال نمایید.

## ارتباط با ما
[Telegram](https://t.me/samanesmaeil)


# Panchanga Calculator

A Python tool to calculate Panchanga (Vedic astrological almanac) elements for a given date and time with high precision.

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
- `jdatetime`: For Jalali date conversion (optional).

## Installation

Ensure you have Python 3.x installed. Install the required dependencies using pip:

```bash
pip install ephem jdatetime
```

## Usage

Run the script from the command line with the required arguments:

```bash
python panchanga.py -d DD/MM/YYYY -t HH:MM -z [+/-]HH:MM [--calendar gregorian|jalali]
```

**Arguments:**

- `-d` or `--date`: Date in `DD/MM/YYYY` format.
- `-t` or `--time`: Time in `HH:MM` 24-hour format.
- `-z` or `--zone`: Timezone with respect to GMT in `[+/-]HH:MM` format.
- `--calendar`: Specifies the calendar type of the input date (default: `gregorian`).

**Examples:**

- For Gregorian date:
  ```bash
  python panchanga.py -d 25/12/2023 -t 12:00 -z +05:30
  ```

- For Jalali date:
  ```bash
  python panchanga.py -d 23/09/1402 -t 12:00 -z +03:30 --calendar jalali
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
