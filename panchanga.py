import ephem
import math
from datetime import datetime
import argparse
from typing import Dict, NamedTuple
from dataclasses import dataclass

# Constants
D2R = math.pi / 180.0
R2D = 180.0 / math.pi

@dataclass
class PanchangaData:
    tithi: str = ""
    paksha: str = ""
    nakshatra: str = ""
    yoga: str = ""
    karana: str = ""
    rashi: str = ""

class AstronomicalConstants:
    MONTHS = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    RASHI = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya", "Tula",
             "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"]

    TITHI = ["Prathame", "Dwithiya", "Thrithiya", "Chathurthi", "Panchami",
             "Shrashti", "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi",
             "Dwadashi", "Thrayodashi", "Chaturdashi", "Poornima", "Prathame",
             "Dwithiya", "Thrithiya", "Chathurthi", "Panchami", "Shrashti",
             "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi",
             "Thrayodashi", "Chaturdashi", "Amavasya"]

    KARAN = ["Bava", "Balava", "Kaulava", "Taitula", "Garija", "Vanija",
             "Visti", "Sakuni", "Chatuspada", "Naga", "Kimstughna"]

    YOGA = ["Vishkambha", "Prithi", "Ayushman", "Saubhagya", "Shobhana",
            "Atiganda", "Sukarman", "Dhrithi", "Shoola", "Ganda", "Vridhi",
            "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata",
            "Variyan", "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
            "Bramha", "Indra", "Vaidhruthi"]

    NAKSHATRA = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardhra",
                 "Punarvasu", "Pushya", "Ashlesa", "Magha", "Poorva Phalguni", "Uttara Phalguni",
                 "Hasta", "Chitra", "Swathi", "Vishaka", "Anuradha", "Jyeshta", "Mula",
                 "Poorva Ashada", "Uttara Ashada", "Sravana", "Dhanishta", "Shatabisha",
                 "Poorva Bhadra", "Uttara Bhadra", "Revathi"]

class PanchangaCalculator:
    @staticmethod
    def normalize_degrees(angle: float) -> float:
        """Normalize angle to range [0, 360)"""
        return angle - math.floor(angle / 360.0) * 360.0

    @staticmethod
    def calculate_ayanamsa(jd: float) -> float:
        """Calculate ayanamsa for given Julian date"""
        t = (jd - 2451545.0) / 36525
        return 23.452294 - 0.0130125 * t - 0.00000164 * t * t + 0.000000503 * t * t * t

    @staticmethod
    def setup_observer(date: datetime) -> ephem.Observer:
        """Setup observer with default parameters"""
        observer = ephem.Observer()
        observer.date = ephem.Date(date)
        observer.lat = '0'
        observer.lon = '0'
        observer.elevation = 0
        observer.pressure = 0
        observer.horizon = '-0:34'
        return observer

    def calculate_panchanga(self, date: datetime) -> PanchangaData:
        """Calculate all Panchanga elements for given date and time"""
        pdata = PanchangaData()
        
        # Initialize celestial objects and observer
        observer = self.setup_observer(date)
        sun = ephem.Sun()
        moon = ephem.Moon()
        
        # Compute positions
        sun.compute(observer)
        moon.compute(observer)
        
        # Calculate base values
        jd = ephem.julian_date(observer.date)
        ayanamsa = self.calculate_ayanamsa(jd)
        sun_long = math.degrees(sun.ra) * 15
        moon_long = math.degrees(moon.ra) * 15
        moon_phase = moon.phase
        
        # Calculate adjusted longitudes
        moon_long_adjusted = self.normalize_degrees(moon_long + ayanamsa)
        sun_long_adjusted = self.normalize_degrees(sun_long + ayanamsa)

        # Calculate all panchanga elements
        self._calculate_tithi(moon_phase, pdata)
        self._calculate_nakshatra(moon_long_adjusted, pdata)
        self._calculate_yoga(moon_long_adjusted, sun_long_adjusted, pdata)
        self._calculate_karana(moon_phase, pdata)
        self._calculate_rashi(moon_long_adjusted, pdata)
        
        return pdata

    def _calculate_tithi(self, moon_phase: float, pdata: PanchangaData) -> None:
        """Calculate Tithi from moon phase"""
        tithi_num = int(moon_phase / 12)
        pdata.tithi = AstronomicalConstants.TITHI[tithi_num]
        pdata.paksha = "Shukla" if moon_phase < 180 else "Krishna"

    def _calculate_nakshatra(self, moon_long_adjusted: float, pdata: PanchangaData) -> None:
        """Calculate Nakshatra from adjusted moon longitude"""
        nak_index = int(moon_long_adjusted * 27 / 360)
        pdata.nakshatra = AstronomicalConstants.NAKSHATRA[nak_index]

    def _calculate_yoga(self, moon_long_adjusted: float, sun_long_adjusted: float, 
                       pdata: PanchangaData) -> None:
        """Calculate Yoga from adjusted sun and moon longitudes"""
        yoga_angle = self.normalize_degrees(moon_long_adjusted + sun_long_adjusted)
        yoga_index = int(yoga_angle * 27 / 360)
        pdata.yoga = AstronomicalConstants.YOGA[yoga_index]

    def _calculate_karana(self, moon_phase: float, pdata: PanchangaData) -> None:
        """Calculate Karana from moon phase"""
        lunar_day_progress = moon_phase % 12
        karana_num = int(lunar_day_progress / 6)
        if karana_num == 0:
            karana_num = 10
        elif karana_num >= 57:
            karana_num -= 50
        pdata.karana = AstronomicalConstants.KARAN[karana_num % len(AstronomicalConstants.KARAN)]

    def _calculate_rashi(self, moon_long_adjusted: float, pdata: PanchangaData) -> None:
        """Calculate Rashi from adjusted moon longitude"""
        rashi_long = self.normalize_degrees(moon_long_adjusted)
        rashi_index = int(rashi_long / 30)
        pdata.rashi = AstronomicalConstants.RASHI[rashi_index]

def parse_time(time_str: str) -> float:
    """Parse time string into decimal hours"""
    try:
        hr_str, mn_str = time_str.split(':')
        return float(hr_str) + float(mn_str) / 60.0
    except ValueError:
        raise ValueError("Invalid time format. Use hh:mm.")

def parse_timezone(zone_str: str) -> float:
    """Parse timezone string into decimal hours"""
    try:
        z_hr_str, z_mn_str = zone_str.split(':')
        z_hr = float(z_hr_str) + float(z_mn_str) / 60.0
        return -z_hr if zone_str.startswith('-') else z_hr
    except ValueError:
        raise ValueError("Invalid timezone format. Use [+/-]hh:mm.")

def main():
    parser = argparse.ArgumentParser(description='Calculate Panchanga with high precision')
    parser.add_argument('-d', '--date', required=True, help='Date in dd/mm/yyyy format')
    parser.add_argument('-t', '--time', required=True, help='Time in hh:mm 24-hour format')
    parser.add_argument('-z', '--zone', required=True, help='Zone with respect to GMT in [+/-]hh:mm format')

    args = parser.parse_args()

    try:
        dd, mm, yy = map(int, args.date.split('/'))
        hr = parse_time(args.time)
        z_hr = parse_timezone(args.zone)

        date = datetime(yy, mm, dd, int(hr), int((hr % 1) * 60))
        calculator = PanchangaCalculator()
        pdata = calculator.calculate_panchanga(date)

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