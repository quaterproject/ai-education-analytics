import pandas as pd

def engineer_features(df: pd.DataFrame, model_type: str = "LATE_STAGE") -> pd.DataFrame:
    """
    Engineer features from the raw student dataset.
    Handles both pandas DataFrame and dictionary/JSON-like inputs.
    """
    df = df.copy()
    
    # 1. Total Alcohol Consumption
    # Dalc (workday alcohol) and Walc (weekend alcohol) are 1 (very low) to 5 (very high)
    if 'Dalc' in df.columns and 'Walc' in df.columns:
        df['alc_consumption'] = df['Dalc'].astype(float) + df['Walc'].astype(float)
    else:
        df['alc_consumption'] = 2.0  # default
        
    # 2. Parental Education Level Sum
    # Medu and Fedu are 0 (none) to 4 (higher education)
    if 'Medu' in df.columns and 'Fedu' in df.columns:
        df['parent_edu_sum'] = df['Medu'].astype(float) + df['Fedu'].astype(float)
    else:
        df['parent_edu_sum'] = 4.0  # default
        
    # 3. Combined Support Score
    # schoolsup and famsup are yes/no
    school_sup_val = 0.0
    fam_sup_val = 0.0
    if 'schoolsup' in df.columns:
        school_sup_val = df['schoolsup'].map({'yes': 1.0, 'no': 0.0}).fillna(0.0)
    if 'famsup' in df.columns:
        fam_sup_val = df['famsup'].map({'yes': 1.0, 'no': 0.0}).fillna(0.0)
    df['academic_support_score'] = school_sup_val + fam_sup_val

    # 4. Study to Free Time Ratio
    # studytime (1-4) and freetime (1-5)
    if 'studytime' in df.columns and 'freetime' in df.columns:
        df['study_to_free_ratio'] = df['studytime'].astype(float) / (df['freetime'].astype(float) + 0.1)
    else:
        df['study_to_free_ratio'] = 0.5  # default

    # 5. Grade Trend (G2 - G1) - Only for LATE_STAGE model
    if model_type == "LATE_STAGE" and 'G1' in df.columns and 'G2' in df.columns:
        df['grade_trend'] = df['G2'].astype(float) - df['G1'].astype(float)
    else:
        df['grade_trend'] = 0.0  # default or placeholder

    return df
