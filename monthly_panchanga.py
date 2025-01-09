#!/usr/bin/env python3

from datetime import datetime, timedelta
import argparse
from typing import List

from calendar import monthcalendar
import sys
from panchanga import PanchangaCalculator, PanchangaData, AstronomicalConstants
from utils import parse_timezone

class MonthlyPanchangaDisplay:
    def __init__(self, year: int, month: int, timezone: float):
        self.year = year
        self.month = month
        self.timezone = timezone
        self.calculator = PanchangaCalculator()

    def get_day_panchanga(self, day: int) -> PanchangaData:
        date = datetime(self.year, self.month, day, 0, 0)
        utc_time = date - timedelta(hours=self.timezone)
        return self.calculator.calculate_panchanga(utc_time)

    def display(self):
        # Header
        month_name = AstronomicalConstants.MONTHS[self.month - 1]
        header = f"{month_name} {self.year}"
        print("\n" + "=" * 80)
        print(header.center(80))
        print("=" * 80)

        # Weekday headers
        print("Sun         Mon         Tue         Wed         Thu         Fri         Sat")
        print("-" * 80)

        # Calendar content
        cal = monthcalendar(self.year, self.month)
        for week in cal:
            self.display_week(week)

    def display_week(self, week: List[int]):
        # Day and Tithi
        week_str = ""
        for day in week:
            if day == 0:
                week_str += "           "
            else:
                try:
                    pdata = self.get_day_panchanga(day)
                    day_info = f"{day:2d}-{pdata.tithi[:3]}"
                    week_str += f"{day_info:<11}"
                except:
                    week_str += "           "
        print(week_str)

        # Display additional information
        for info_type in ["Nakshatra", "Yoga", "Karana"]:
            week_str = ""
            for day in week:
                if day == 0:
                    week_str += "           "
                else:
                    try:
                        pdata = self.get_day_panchanga(day)
                        if info_type == "Nakshatra":
                            info = pdata.nakshatra[:3]
                        elif info_type == "Yoga":
                            info = pdata.yoga[:3]
                        else:
                            info = pdata.karana[:3]
                        week_str += f"{info:11}"
                    except:
                        week_str += "           "
            print(week_str)
        print("-" * 80)


def main():
    parser = argparse.ArgumentParser(description='Generate Monthly Panchanga Calendar')
    parser.add_argument('--month', type=int, help='Month number (1-12)')
    parser.add_argument('--year', type=int, help='Year')
    parser.add_argument('-z', '--zone', required=True, 
                        help='Timezone offset from UTC (e.g., +5:30 or +5.5)')

    args = parser.parse_args()

    try:
        # Use current month/year if not specified
        current_date = datetime.now()
        month = args.month if args.month else current_date.month
        year = args.year if args.year else current_date.year

        if not (1 <= month <= 12):
            raise ValueError("Month must be between 1 and 12")

        timezone = parse_timezone(args.zone)
        
        display = MonthlyPanchangaDisplay(year, month, timezone)
        display.display()

    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()