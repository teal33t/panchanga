from datetime import datetime, timedelta
from typing import List
from dataclasses import dataclass
from panchanga import PanchangaData, PanchangaCalculator


@dataclass
class MuhurthaTimeRange:
    start_time: datetime
    end_time: datetime
    quality: str
    explanation: str



class MuhurthaFinder:
    def __init__(self):
        self.panchanga = PanchangaCalculator()
        
        # Expand action rules with meeting-specific criteria
        self.action_rules = {
            "marriage": {
                "good_nakshatras": ["Rohini", "Magha", "Uttara Phalguni", "Hasta"],
                "avoid_tithis": ["Amavasya", "Chaturthi"],
                "good_weekdays": [0, 3, 4]  # Monday, Thursday, Friday
            },
            "house_warming": {
                "good_nakshatras": ["Rohini", "Uttara Phalguni", "Uttara Ashadha"],
                "avoid_tithis": ["Amavasya"],
                "good_weekdays": [0, 3, 5]  # Monday, Thursday, Saturday
            },
            "meeting": {
                "good_nakshatras": ["Ashwini", "Pushya", "Chitra", "Swathi"],
                "avoid_tithis": ["Ashtami", "Navami"],
                "good_weekdays": [1, 2, 4]  # Tuesday, Wednesday, Friday
            }
            # Add more action types and their rules as needed
        }


    def _get_weekday_name(self, dt: datetime) -> str:
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return weekdays[dt.weekday()]

    def _generate_explanation(self, dt: datetime, pdata: PanchangaData, action_type: str) -> str:
        """Generate an explanation for why this time is suitable"""
        rules = self.action_rules[action_type]
        
        explanations = [
            f"This is a good time for {action_type} because:",
            f"- It falls on {self._get_weekday_name(dt)}, which is an auspicious day for {action_type}",
            f"- The Nakshatra (lunar mansion) is {pdata.nakshatra}, which is favorable for {action_type}",
            f"- The Tithi (lunar day) is {pdata.tithi}, which is not in the avoided tithis",
            f"- The Paksha (lunar phase) is {pdata.paksha}"
        ]
        
        # Add action-specific explanations
        if action_type == "meeting":
            explanations.append("- This combination supports clear communication and successful outcomes")
        elif action_type == "marriage":
            explanations.append("- This combination supports harmony and long-lasting relationships")
        elif action_type == "house_warming":
            explanations.append("- This combination supports prosperity and positive energy in the new home")
        
        return "\n".join(explanations)

    def find_muhurtha(self,
                      start_date: datetime,
                      end_date: datetime,
                      action_type: str,
                      check_interval_hours: float = 1.0) -> List[MuhurthaTimeRange]:
        if action_type not in self.action_rules:
            raise ValueError(f"Unknown action type: {action_type}")

        suitable_ranges = []
        current_time = start_date
        range_start = None
        current_quality = None
        current_explanation = None

        while current_time <= end_date:
            pdata = self.panchanga.calculate_panchanga(current_time)
            is_suitable = self._is_time_suitable(current_time, pdata, action_type)
            quality = self._evaluate_quality(current_time, pdata, action_type)

            if is_suitable:
                if range_start is None:
                    range_start = current_time
                    current_quality = quality
                    current_explanation = self._generate_explanation(current_time, pdata, action_type)
            else:
                if range_start is not None:
                    suitable_ranges.append(
                        MuhurthaTimeRange(
                            start_time=range_start,
                            end_time=current_time,
                            quality=current_quality,
                            explanation=current_explanation
                        )
                    )
                    range_start = None
                    current_quality = None
                    current_explanation = None

            current_time += timedelta(hours=check_interval_hours)

        if range_start is not None:
            suitable_ranges.append(
                MuhurthaTimeRange(
                    start_time=range_start,
                    end_time=current_time,
                    quality=current_quality,
                    explanation=current_explanation
                )
            )

        return suitable_ranges

    def format_duration(self, duration_hours: float) -> str:
        """Convert duration from hours to hours and minutes format"""
        total_minutes = int(duration_hours * 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        if hours == 0:
            return f"{minutes} minutes"
        elif minutes == 0:
            return f"{hours} hours"
        else:
            return f"{hours} hours {minutes} minutes"


    def _is_time_suitable(self,
                          dt: datetime,
                          pdata: PanchangaData,
                          action_type: str) -> bool:
        rules = self.action_rules[action_type]
        
        if (pdata.nakshatra in rules["good_nakshatras"] and
            pdata.tithi not in rules["avoid_tithis"] and
            dt.weekday() in rules["good_weekdays"]):
            return True
            
        return False

    def _evaluate_quality(self,
                          dt: datetime,
                          pdata: PanchangaData,
                          action_type: str) -> str:
        # A more sophisticated evaluation can be implemented here.
        return "Good" if self._is_time_suitable(dt, pdata, action_type) else "Neutral"

if __name__ == "__main__":
    finder = MuhurthaFinder()
    start = datetime.now()
    end = start + timedelta(days=7) # change days for your range
    
    results = finder.find_muhurtha(
        start_date=start,
        end_date=end,
        action_type="meeting",
        check_interval_hours=0.1
    )
    
    for result in results:
        duration = (result.end_time - result.start_time).total_seconds() / 3600
        duration_str = finder.format_duration(duration)
        
        print(f"Suitable period:")
        print(f"Start: {result.start_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"End: {result.end_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"Duration: {duration_str}")
        print(f"Quality: {result.quality}")
        print("\nAstrological Factors:")
        print(result.explanation)
        print("-" * 50)
        print()