
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
