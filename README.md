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
  - [Daily Panchanga](#daily-panchanga)
  - [Monthly Panchanga](#monthly-panchanga) 
  - [Muhurtha Finder](#muhurtha-finder)
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

The tool has three modes of operation:

### Daily Panchanga

Calculate Panchanga elements for a specific day:

```bash
python daily_panchanga.py -d DD/MM/YYYY -t HH:MM -z [+/-]HH:MM [--calendar gregorian|jalali]
```

Example output:
```bash
python3 daily_panchanga.py -d 23/09/1402 -t 12:00 -z +03:30 --calendar jalali

Tithi     : Prathame, Shukla Paksha
Nakshatra : Dhanishta
Yoga      : Sadhya
Karana    : Kimstughna
Rashi     : Makara
```

```bash
python monthly_panchanga.py -z +3:30                         

================================================================================
                                  January 2025                                  
================================================================================
Sun         Mon         Tue         Wed         Thu         Fri         Sat
--------------------------------------------------------------------------------
                       1-Pra      2-Pra      3-Pra      4-Dwi      5-Thr     
                      Ash        Poo        Has        Ash        Swa        
                      Ayu        Shi        Gan        Ind        Vaj        
                      Kim        Kim        Bal        Kim        Kim        
--------------------------------------------------------------------------------
 6-Cha      7-Pan      8-Pan      9-Shr     10-Sap     11-Ash     12-Ash     
Bha        Vis        Roh        Mul        Ash        Utt        Anu        
Ayu        Var        Suk        Shu        Vaj        Ati        Bra        
Kim        Kim        Bal        Bal        Bal        Kim        Bal        
--------------------------------------------------------------------------------
13-Nav     14-Nav     15-Nav     16-Ash     17-Ash     18-Ash     19-Sap     
Pus        Poo        Chi        Bha        Swa        Ash        Has        
Vya        Sho        Ind        Vaj        Ayu        Sid        Ayu        
Kim        Kim        Kim        Bal        Bal        Kim        Kim        
--------------------------------------------------------------------------------
20-Shr     21-Pan     22-Pan     23-Cha     24-Thr     25-Dwi     26-Dwi     
Poo        Mag        Sra        Pus        Utt        Ash        Sha        
Sid        Pri        Vaj        Pri        Vya        Sho        Sad        
Bal        Bal        Kim        Kim        Bal        Bal        Kim        
--------------------------------------------------------------------------------
27-Pra     28-Pra     29-Pra     30-Pra     31-Pra                           
Has        Kri        Mul        Pus        Dha                              
Dhr        Ayu        Shi        Gan        Vai                              
Bal        Kim        Kim        Kim        Kim                              
--------------------------------------------------------------------------------
```

```bash
python muhurtha_finder.py

Suitable period:
Start: 2025-01-10 04:33
End: 2025-01-10 06:33
Duration: 2 hours
Quality: Good

Astrological Factors:
This is a good time for meeting because:
- It falls on Friday, which is an auspicious day for meeting
- The Nakshatra (lunar mansion) is Chitra, which is favorable for meeting
- The Tithi (lunar day) is Saptami, which is not in the avoided tithis
- The Paksha (lunar phase) is Shukla
- This combination supports clear communication and successful outcomes
--------------------------------------------------
```