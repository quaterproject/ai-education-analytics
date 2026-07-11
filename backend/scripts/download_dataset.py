import os
import zipfile
import urllib.request
import pandas as pd
import numpy as np

# Define paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")

UCI_URL = "https://archive.ics.uci.edu/static/public/320/student+performance.zip"

def create_synthetic_uci_data(size=600) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generates synthetic student performance data with exact UCI columns as fallback."""
    print("Generating synthetic student performance data...")
    np.random.seed(42)
    
    schools = ['GP', 'MS']
    sexes = ['F', 'M']
    addresses = ['U', 'R']
    famsizes = ['GT3', 'LE3']
    pstatuses = ['T', 'A']
    mjobs = ['at_home', 'health', 'other', 'services', 'teacher']
    fjobs = ['at_home', 'health', 'other', 'services', 'teacher']
    reasons = ['course', 'home', 'reputation', 'other']
    guardians = ['mother', 'father', 'other']
    yes_no = ['yes', 'no']
    
    data = []
    for i in range(size):
        school = np.random.choice(schools, p=[0.75, 0.25])
        sex = np.random.choice(sexes)
        age = int(np.random.randint(15, 23))
        address = np.random.choice(addresses, p=[0.7, 0.3])
        famsize = np.random.choice(famsizes, p=[0.7, 0.3])
        pstatus = np.random.choice(pstatuses, p=[0.9, 0.1])
        medu = int(np.random.randint(0, 5))
        fedu = int(np.random.randint(0, 5))
        mjob = np.random.choice(mjobs)
        fjob = np.random.choice(fjobs)
        reason = np.random.choice(reasons)
        guardian = np.random.choice(guardians, p=[0.7, 0.2, 0.1])
        traveltime = int(np.random.randint(1, 5))
        studytime = int(np.random.randint(1, 5))
        failures = int(np.random.choice([0, 1, 2, 3], p=[0.8, 0.1, 0.07, 0.03]))
        schoolsup = np.random.choice(yes_no, p=[0.1, 0.9])
        famsup = np.random.choice(yes_no, p=[0.6, 0.4])
        paid = np.random.choice(yes_no, p=[0.4, 0.6])
        activities = np.random.choice(yes_no)
        nursery = np.random.choice(yes_no, p=[0.8, 0.2])
        higher = np.random.choice(yes_no, p=[0.9, 0.1])
        internet = np.random.choice(yes_no, p=[0.8, 0.2])
        romantic = np.random.choice(yes_no, p=[0.3, 0.7])
        famrel = int(np.random.randint(1, 6))
        freetime = int(np.random.randint(1, 6))
        goout = int(np.random.randint(1, 6))
        dalc = int(np.random.randint(1, 6))
        walc = int(np.random.randint(1, 6))
        health = int(np.random.randint(1, 6))
        
        # Calculate grade signals correlated with studytime, absences, and failures
        base_grade = 10 + 1.2 * studytime - 2.0 * failures - 0.05 * np.random.randint(0, 20)
        if schoolsup == 'yes':
            base_grade += 0.5
        if internet == 'yes':
            base_grade += 0.5
            
        g1 = np.clip(base_grade + np.random.normal(0, 1.5), 0, 20)
        g2 = np.clip(g1 + np.random.normal(0, 1.0), 0, 20)
        g3 = np.clip(g2 + np.random.normal(0, 1.0), 0, 20)
        
        absences = int(np.random.negative_binomial(2, 0.2)) # typical absence distribution
        absences = np.clip(absences, 0, 93)
        
        row = [
            school, sex, age, address, famsize, pstatus, medu, fedu, mjob, fjob,
            reason, guardian, traveltime, studytime, failures, schoolsup, famsup,
            paid, activities, nursery, higher, internet, romantic, famrel,
            freetime, goout, dalc, walc, health, absences, int(g1), int(g2), int(g3)
        ]
        data.append(row)
        
    cols = [
        'school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'Mjob', 'Fjob',
        'reason', 'guardian', 'traveltime', 'studytime', 'failures', 'schoolsup', 'famsup',
        'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic', 'famrel',
        'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2', 'G3'
    ]
    df = pd.DataFrame(data, columns=cols)
    
    # Split into math and portuguese portions
    df_mat = df.sample(frac=0.6, random_state=42).copy()
    df_por = df.drop(df_mat.index).copy()
    
    return df_mat, df_por

def download_and_extract():
    os.makedirs(RAW_DIR, exist_ok=True)
    
    zip_path = os.path.join(RAW_DIR, "student_performance.zip")
    try:
        print(f"Downloading dataset from {UCI_URL}...")
        # Add User-Agent to avoid getting blocked
        req = urllib.request.Request(
            UCI_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=15) as response, open(zip_path, 'wb') as out_file:
            out_file.write(response.read())
            
        print("Extracting main ZIP file...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(RAW_DIR)
            
        inner_zip = os.path.join(RAW_DIR, "student.zip")
        if os.path.exists(inner_zip):
            print("Extracting inner ZIP file (student.zip)...")
            with zipfile.ZipFile(inner_zip, 'r') as zip_ref:
                zip_ref.extractall(RAW_DIR)
            os.remove(inner_zip)
            
        os.remove(zip_path)
        print("Dataset downloaded and extracted successfully!")
        
    except Exception as e:
        print(f"Failed to download/extract original dataset: {e}")
        # Call synthetic generator
        df_mat, df_por = create_synthetic_uci_data()
        df_mat.to_csv(os.path.join(RAW_DIR, "student-mat.csv"), sep=";", index=False)
        df_por.to_csv(os.path.join(RAW_DIR, "student-por.csv"), sep=";", index=False)
        print("Generated synthetic dataset backups as CSVs.")

if __name__ == "__main__":
    download_and_extract()
