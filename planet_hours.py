from datetime import datetime, timedelta
import ephem
import argparse
from typing import List, Tuple
import pytz
import re
from zoneinfo import ZoneInfo

class VedicPlanetaryHours:
    # Chaldean order of planets based on their speed through zodiac
    CHALDEAN_ORDER = [
        "Saturn",  # Slowest
        "Jupiter", 
        "Mars",
        "Sun",
        "Venus",
        "Mercury",
        "Moon"     # Fastest
    ]

    # Day rulers according to Vedic system
    DAY_RULERS = {
        0: "Sun",     # Sunday (Ravivara)
        1: "Moon",    # Monday (Somavara)
        2: "Mars",    # Tuesday (Mangalavara)
        3: "Mercury", # Wednesday (Budhavara)
        4: "Jupiter", # Thursday (Guruvara)
        5: "Venus",   # Friday (Shukravara)
        6: "Saturn"   # Saturday (Shanivara)
    }

    # Sanskrit names and symbols
    PLANET_INFO = {
        "Sun": {"sanskrit": "Surya", "symbol": "☉"},
        "Moon": {"sanskrit": "Chandra", "symbol": "☽"},
        "Mars": {"sanskrit": "Mangal", "symbol": "♂"},
        "Mercury": {"sanskrit": "Budha", "symbol": "☿"},
        "Jupiter": {"sanskrit": "Guru", "symbol": "♃"},
        "Venus": {"sanskrit": "Shukra", "symbol": "♀"},
        "Saturn": {"sanskrit": "Shani", "symbol": "♄"}
    }

    def __init__(self, date: datetime, latitude: float, longitude: float, timezone: str):
        self.latitude = latitude
        self.longitude = longitude
        self.original_timezone = timezone  # Store the original timezone string
        
        # Handle both timezone formats: "Asia/Tehran" or "+03:30"
        if re.match(r'^[+-]\d{2}:?\d{2}$', timezone):
            # Convert "+03:30" format to hours offset
            sign = 1 if timezone[0] == '+' else -1
            hours = int(timezone[1:3])
            minutes = int(timezone[-2:])
            self.tz_offset = timedelta(hours=sign * hours, minutes=minutes)
            self.timezone = f"UTC{timezone}"
            self.is_offset = True
        else:
            self.timezone = timezone
            self.is_offset = False
            tz = ZoneInfo(timezone)
            # Get the offset for the specific date
            sample_dt = date.replace(tzinfo=tz)
            self.tz_offset = sample_dt.utcoffset()

        # Convert input date to timezone-aware datetime
        if isinstance(date, datetime):
            if date.tzinfo is None:
                self.date = date + self.tz_offset
            else:
                self.date = date
        else:
            self.date = datetime.combine(date, datetime.min.time()) + self.tz_offset
            
        # Calculate local mean time adjustment
        self.lmt_adjustment = self._calculate_lmt_adjustment()


    def get_current_time(self) -> datetime:
        """Get current time in the proper timezone"""
        now = datetime.utcnow()
        if self.is_offset:
            return now + self.tz_offset
        else:
            return now.replace(tzinfo=pytz.UTC).astimezone(ZoneInfo(self.timezone))


    def _calculate_sunrise_sunset(self) -> Tuple[datetime, datetime]:
        """Calculate sunrise and sunset times"""
        observer = ephem.Observer()
        observer.lat = str(self.latitude)
        observer.lon = str(self.longitude)
        observer.date = self.date.strftime('%Y/%m/%d')
        observer.horizon = '-0:34'
        
        observer.epoch = '2000'
        ephem.Delta_T = 0
        ephem.ayanamsa_name = 'Lahiri'
        
        sun = ephem.Sun()
        
        # Get UTC sunrise/sunset
        sunrise_utc = observer.next_rising(sun).datetime()
        sunset_utc = observer.next_setting(sun).datetime()
        
        # Apply timezone offset
        sunrise = sunrise_utc + self.tz_offset + timedelta(hours=self.lmt_adjustment)
        sunset = sunset_utc + self.tz_offset + timedelta(hours=self.lmt_adjustment)
        
        return sunrise, sunset
    
    def _calculate_lmt_adjustment(self) -> float:
        """Calculate adjustment for Local Mean Time based on longitude"""
        standard_meridian = round(self.longitude / 15) * 15
        time_adjustment = 4 * (self.longitude - standard_meridian) / 60  # in hours
        return time_adjustment


    def _get_hora_sequence(self, weekday: int) -> List[str]:
        """Generate the sequence of planetary rulers based on weekday and Chaldean order"""
        # Base Chaldean sequence
        chaldean = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]
        
        # Adjust sequence based on weekday
        weekday_name = self.date.strftime('%a')
        if weekday_name == "Mon":
            chaldean = ["Moon", "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury"]
        elif weekday_name == "Tue":
            chaldean = ["Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter"]
        elif weekday_name == "Wed":
            chaldean = ["Mercury", "Moon", "Saturn", "Jupiter", "Mars", "Sun", "Venus"]
        elif weekday_name == "Thu":
            chaldean = ["Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn"]
        elif weekday_name == "Fri":
            chaldean = ["Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars", "Sun"]
        elif weekday_name == "Sat":
            chaldean = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]
        elif weekday_name == "Sun":
            chaldean = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
        
        # Create a 24-hour sequence by repeating the pattern
        extended_sequence = []
        current_idx = 0
        for _ in range(24):
            extended_sequence.append(chaldean[current_idx])
            current_idx = (current_idx + 1) % 7
            
        return extended_sequence



    def calculate_horas(self) -> List[dict]:
        """Calculate Vedic planetary hours (horas) for the day"""
        sunrise, sunset = self._calculate_sunrise_sunset()
        
        # Convert times to minutes since midnight
        sunrise_minutes = sunrise.hour * 60 + sunrise.minute
        sunset_minutes = sunset.hour * 60 + sunset.minute
        
        # Calculate length of daylight in minutes
        day_length = sunset_minutes - sunrise_minutes
        
        # Calculate night length (until next sunrise)
        next_sunrise = sunrise + timedelta(days=1)
        night_minutes = ((24 * 60) - sunset_minutes) + (next_sunrise.hour * 60 + next_sunrise.minute)
        
        # Length of each planetary hour
        day_hora_length = day_length / 12
        night_hora_length = night_minutes / 12
        
        # Get hora sequence for this weekday
        weekday = self.date.weekday()
        hora_sequence = self._get_hora_sequence(weekday)
        
        planetary_hours = []
        
        # Calculate daytime hours
        current_time = sunrise
        for i in range(12):
            end_time = current_time + timedelta(minutes=day_hora_length)
            planet = hora_sequence[i]
            planetary_hours.append({
                'start': current_time,
                'end': end_time,
                'planet': planet,
                'sanskrit': self.PLANET_INFO[planet]["sanskrit"],
                'symbol': self.PLANET_INFO[planet]["symbol"],
                'period': 'Day'
            })
            current_time = end_time

        # Calculate nighttime hours
        current_time = sunset
        for i in range(12):
            end_time = current_time + timedelta(minutes=night_hora_length)
            planet = hora_sequence[i + 12]
            planetary_hours.append({
                'start': current_time,
                'end': end_time,
                'planet': planet,
                'sanskrit': self.PLANET_INFO[planet]["sanskrit"],
                'symbol': self.PLANET_INFO[planet]["symbol"],
                'period': 'Night'
            })
            current_time = end_time

        return planetary_hours



    def display_horas(self):
        """Display Vedic planetary hours in a formatted way"""
        horas = self.calculate_horas()
        
        # Get current time using the appropriate method
        now = self.get_current_time()
        
        print(f"\nVedic Planetary Hours (Hora) for {self.date.strftime('%A, %B %d, %Y')}")
        print(f"Timezone: {self.original_timezone}")
        print(f"Location: {self.latitude}°N, {self.longitude}°E")
        print("-" * 100)
        print(f"{'Time Period':<20} {'Planet':<10} {'Sanskrit':<10} {'Symbol':<8} {'Period':<8} {'Current':<8}")
        print("-" * 100)
        
        for hora in horas:
            time_str = f"{hora['start'].strftime('%H:%M')} - {hora['end'].strftime('%H:%M')}"
            is_current = hora['start'] <= now <= hora['end']
            current_indicator = "→ NOW ←" if is_current else ""
            
            print(f"{time_str:<20} {hora['planet']:<10} {hora['sanskrit']:<10} "
                  f"{hora['symbol']:<8} {hora['period']:<8} {current_indicator}")



def get_available_timezones():
    """Get list of available timezones and add UTC offset format examples"""
    timezones = pytz.all_timezones
    # Add example UTC offset formats
    utc_examples = [
        "+00:00", "+01:00", "+02:00", "+03:00", "+03:30", "+04:00", "+04:30",
        "+05:00", "+05:30", "+05:45", "+06:00", "+06:30", "+07:00", "+08:00",
        "+09:00", "+09:30", "+10:00", "+11:00", "+12:00", "+13:00",
        "-01:00", "-02:00", "-03:00", "-03:30", "-04:00", "-05:00", "-06:00",
        "-07:00", "-08:00", "-09:00", "-10:00", "-11:00"
    ]
    return sorted(list(timezones) + utc_examples)

def validate_timezone(tz: str) -> bool:
    """Validate timezone string format"""
    if tz in pytz.all_timezones:
        return True
    # Check for UTC offset format (+/-HH:MM)
    if re.match(r'^[+-]\d{2}:?\d{2}$', tz):
        try:
            # Extract hours and minutes
            sign = 1 if tz[0] == '+' else -1
            hours = int(tz[1:3])
            minutes = int(tz[-2:])
            # Validate hours and minutes
            if hours <= 14 and minutes < 60:
                return True
        except ValueError:
            pass
    return False

def main():
    parser = argparse.ArgumentParser(description='Calculate Vedic Planetary Hours (Hora)')
    parser.add_argument('--date', help='Date in YYYY-MM-DD format (default: today)',
                      default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument('--lat', type=float, required=True,
                      help='Latitude in decimal degrees')
    parser.add_argument('--lon', type=float, required=True,
                      help='Longitude in decimal degrees')
    parser.add_argument('--tz', required=True,
                      help='Timezone name (e.g., "Asia/Tehran") or offset (e.g., "+03:30")')
    parser.add_argument('--list-timezones', action='store_true',
                      help='List all available timezone names and offset formats')

    args = parser.parse_args()

    if args.list_timezones:
        print("\nAvailable timezones and offset formats:")
        for tz in get_available_timezones():
            print(tz)
        return

    try:
        if not validate_timezone(args.tz):
            raise ValueError(f"Invalid timezone: {args.tz}. Use --list-timezones to see valid options.")
            
        date = datetime.strptime(args.date, '%Y-%m-%d')
        calculator = VedicPlanetaryHours(date, args.lat, args.lon, args.tz)
        calculator.display_horas()
        
    except ValueError as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()