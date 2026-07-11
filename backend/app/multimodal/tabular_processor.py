from typing import Dict, Any
from app.core.exceptions import InvalidAcademicDataException

class TabularProcessor:
    @staticmethod
    def validate_and_format_record(record_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate student tabular attributes (grades, study time, absences, support indicators).
        Ensures columns fall into valid bounds matching the UCI schema.
        """
        # Validate ranges
        try:
            study_time = int(record_data.get("study_time", 2))
            if not (1 <= study_time <= 4):
                raise ValueError("study_time must be between 1 and 4")
                
            failures = int(record_data.get("failures", 0))
            if not (0 <= failures <= 4):
                raise ValueError("failures must be between 0 and 4")
                
            absences = int(record_data.get("absences", 0))
            if not (0 <= absences <= 93):
                raise ValueError("absences must be between 0 and 93")
                
            g1 = float(record_data.get("g1", 10.0))
            if not (0.0 <= g1 <= 20.0):
                raise ValueError("g1 must be between 0 and 20")
                
            g2 = float(record_data.get("g2", 10.0))
            if not (0.0 <= g2 <= 20.0):
                raise ValueError("g2 must be between 0 and 20")
                
            health = int(record_data.get("health", 3))
            if not (1 <= health <= 5):
                raise ValueError("health must be between 1 and 5")
                
            # Support flags
            family_support = str(record_data.get("family_support", "no")).lower()
            if family_support not in ["yes", "no"]:
                raise ValueError("family_support must be 'yes' or 'no'")
                
            school_support = str(record_data.get("school_support", "no")).lower()
            if school_support not in ["yes", "no"]:
                raise ValueError("school_support must be 'yes' or 'no'")
                
            internet_access = str(record_data.get("internet_access", "yes")).lower()
            if internet_access not in ["yes", "no"]:
                raise ValueError("internet_access must be 'yes' or 'no'")

            return {
                "study_time": study_time,
                "failures": failures,
                "absences": absences,
                "family_support": family_support,
                "school_support": school_support,
                "internet_access": internet_access,
                "health": health,
                "g1": g1,
                "g2": g2
            }
        except Exception as e:
            raise InvalidAcademicDataException(f"Invalid tabular record: {str(e)}")
        
    @staticmethod
    def map_student_and_record_to_features(student_obj: Any, record_obj: Any) -> Dict[str, Any]:
        """
        Produce a unified 30-feature dictionary representing the raw row format for preprocessor mapping.
        """
        return {
            'school': student_obj.school,
            'sex': student_obj.gender,
            'age': student_obj.age,
            'address': 'U',
            'famsize': 'GT3',
            'Pstatus': 'T',
            'Medu': 3,
            'Fedu': 3,
            'Mjob': 'other',
            'Fjob': 'other',
            'reason': 'course',
            'guardian': 'mother',
            'traveltime': 1,
            'studytime': record_obj.study_time,
            'failures': record_obj.failures,
            'schoolsup': record_obj.school_support,
            'famsup': record_obj.family_support,
            'paid': 'no',
            'activities': 'no',
            'nursery': 'yes',
            'higher': 'yes',
            'internet': record_obj.internet_access,
            'romantic': 'no',
            'famrel': 4,
            'freetime': 3,
            'goout': 3,
            'Dalc': 1,
            'Walc': 1,
            'health': record_obj.health,
            'absences': record_obj.absences,
            'G1': record_obj.g1,
            'G2': record_obj.g2
        }
