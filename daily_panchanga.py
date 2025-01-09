from datetime import datetime, timedelta
import argparse
from panchanga import PanchangaCalculator

try:
    from jdatetime import datetime as jdatetime
except ImportError:
    jdatetime = None

from utils import parse_timezone, parse_time


def main():
    parser = argparse.ArgumentParser(description='Calculate Panchanga with high precision')
    parser.add_argument('-d', '--date', required=True, help='Date in DD/MM/YYYY format')
    parser.add_argument('-t', '--time', required=True, help='Time in HH:MM 24-hour format')
    parser.add_argument('-z', '--zone', required=True, help='Zone with respect to GMT in [+/-]HH:MM format')
    parser.add_argument('--calendar', default='gregorian', choices=['gregorian', 'jalali'], help='Calendar type of the input date')

    args = parser.parse_args()

    try:
        dd, mm, yy = map(int, args.date.split('/'))
        hr = parse_time(args.time)
        z_hr = parse_timezone(args.zone)

        if args.calendar == 'jalali':
            if jdatetime is None:
                print("Error: jdatetime library is not installed. Install it using 'pip install jdatetime' to use Jalali dates.")
                exit(1)
            jalali_date = jdatetime(yy, mm, dd)
            gregorian_date = jalali_date.togregorian()
            date = datetime(gregorian_date.year, gregorian_date.month, gregorian_date.day, int(hr), int((hr % 1) * 60))
        else:
            date = datetime(yy, mm, dd, int(hr), int((hr % 1) * 60))

        local_time = date
        utc_time = local_time - timedelta(hours=z_hr)
        observer = PanchangaCalculator.setup_observer(utc_time)
        calculator = PanchangaCalculator()
        pdata = calculator.calculate_panchanga(observer.date)

        print(f"Tithi     : {pdata.tithi}, {pdata.paksha} Paksha")
        print(f"Nakshatra : {pdata.nakshatra}")
        print(f"Yoga      : {pdata.yoga}")
        print(f"Karana    : {pdata.karana}")
        print(f"Rashi     : {pdata.rashi}")

    except ValueError as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()