import mysql.connector
from mysql.connector import Error

# Replace with your MySQL database connection details
# IMPORTANT: For creating a database, 'user' needs sufficient privileges (e.g., 'root' or a user with CREATE DATABASE).
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', # User with CREATE DATABASE privilege (e.g., 'root')
    'password': 'Pavani@3534',
    'database': 'hospital_data' # The name of the database you want to create/use
}

# The SQL CREATE TABLE statements with IF NOT EXISTS
SQL_CREATE_TABLES = """
-- Table for File 1: Population Projection Data
-- This table stores population counts based on different projection variants, gender, age, and specific dates.
CREATE TABLE IF NOT EXISTS PopulationProjections (
    id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each row
    ProjectionVariant VARCHAR(255),    -- Description of the population projection variant
    Gender VARCHAR(50),                -- Gender (e.g., 'Männlich', 'Weiblich', 'Insgesamt')
    AgeGroup VARCHAR(50),              -- Age or age group (e.g., '0', '1', '90+', 'Insgesamt')
    Population_2022_12_31 INT,         -- Population count for 2022-12-31
    Population_2023_12_31 INT,         -- Population count for 2023-12-31
    Population_2024_12_31 INT,         -- Population count for 2024-12-31
    Population_2025_12_31 INT,         -- Population count for 2025-12-31
    Population_2026_12_31 INT,         -- Population count for 2026-12-31
    Population_2027_12_31 INT,         -- Population count for 2027-12-31
    Population_2028_12_31 INT,         -- Population count for 2028-12-31
    Population_2029_12_31 INT,         -- Population count for 2029-12-31
    Population_2030_12_31 INT,         -- Population count for 2030-12-31
    Population_2031_12_31 INT,         -- Population count for 2031-12-31
    Population_2032_12_31 INT,         -- Population count for 2032-12-31
    Population_2033_12_31 INT,         -- Population count for 2033-12-31
    Population_2034_12_31 INT,         -- Population count for 2034-12-31
    Population_2035_12_31 INT,         -- Population count for 2035-12-31
    Population_2036_12_31 INT,         -- Population count for 2036-12-31
    Population_2037_12_31 INT,         -- Population count for 2037-12-31
    Population_2038_12_31 INT,         -- Population count for 2038-12-31
    Population_2039_12_31 INT,         -- Population count for 2039-12-31
    Population_2040_12_31 INT,         -- Population count for 2040-12-31
    Population_2041_12_31 INT,         -- Population count for 2041-12-31
    Population_2042_12_31 INT,         -- Population count for 2042-12-31
    Population_2043_12_31 INT,         -- Population count for 2043-12-31
    Population_2044_12_31 INT,         -- Population count for 2044-12-31
    Population_2045_12_31 INT,         -- Population count for 2045-12-31
    Population_2046_12_31 INT,         -- Population count for 2046-12-31
    Population_2047_12_31 INT,         -- Population count for 2047-12-31
    Population_2048_12_31 INT,         -- Population count for 2048-12-31
    Population_2049_12_31 INT,         -- Population count for 2049-12-31
    Population_2050_12_31 INT,         -- Population count for 2050-12-31
    Population_2051_12_31 INT,         -- Population count for 2051-12-31
    Population_2052_12_31 INT,         -- Population count for 2052-12-31
    Population_2053_12_31 INT,         -- Population count for 2053-12-31
    Population_2054_12_31 INT,         -- Population count for 2054-12-31
    Population_2055_12_31 INT,         -- Population count for 2055-12-31
    Population_2056_12_31 INT,         -- Population count for 2056-12-31
    Population_2057_12_31 INT,         -- Population count for 2057-12-31
    Population_2058_12_31 INT,         -- Population count for 2058-12-31
    Population_2059_12_31 INT,         -- Population count for 2059-12-31
    Population_2060_12_31 INT,         -- Population count for 2060-12-31
    Population_2061_12_31 INT,         -- Population count for 2061-12-31
    Population_2062_12_31 INT,         -- Population count for 2062-12-31
    Population_2063_12_31 INT,         -- Population count for 2063-12-31
    Population_2064_12_31 INT,         -- Population count for 2064-12-31
    Population_2065_12_31 INT,         -- Population count for 2065-12-31
    Population_2066_12_31 INT,         -- Population count for 2066-12-31
    Population_2067_12_31 INT,         -- Population count for 2067-12-31
    Population_2068_12_31 INT,         -- Population count for 2068-12-31
    Population_2069_12_31 INT,         -- Population count for 2069-12-31
    Population_2070_12_31 INT          -- Population count for 2070-12-31
);

-- Table for File 2: Hospital Bed Information (Detailed)
-- This table serves as a lookup for detailed hospital department codes and their descriptions.
CREATE TABLE IF NOT EXISTS HospitalBedDetails (
    id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each row
    FieldName VARCHAR(255) UNIQUE,     -- The field name or code (e.g., 'Kreis', '0100', 'INSG')
    Content TEXT                       -- The description or content associated with the field name
);

-- Table for File 3: Hospital Facility Data (Comprehensive)
-- This table stores comprehensive information about hospital facilities, including location, contact,
-- ownership, type, emergency care levels, and detailed bed counts by department.
CREATE TABLE IF NOT EXISTS HospitalFacilitiesComprehensive (
    id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each hospital entry
    Land VARCHAR(100),                 -- State or federal state in Germany
    Kreis VARCHAR(100),                -- District/County (with first digit potentially indicating administrative region)
    Gemeinde VARCHAR(100),             -- Municipality
    HospitalName VARCHAR(255),         -- Name of the hospital
    SiteName VARCHAR(255),             -- Name of the hospital site/location
    SiteStreet VARCHAR(255),           -- Street name of the hospital site
    SiteHouseNumber VARCHAR(50),       -- House number of the hospital site
    SitePostalCode VARCHAR(20),        -- Postal code of the hospital site
    SiteCity VARCHAR(100),             -- City/Town of the hospital site
    PhoneNumber VARCHAR(50),           -- Full telephone number (area code and number)
    EmailAddress VARCHAR(255),         -- Email address of the hospital
    InternetAddress VARCHAR(255),      -- Website address of the hospital
    OwnerType INT,                     -- Type of ownership (1=public, 2=non-profit, 3=private)
    OwnerName VARCHAR(255),            -- Name of the owner/operator
    InstitutionType INT,               -- Type of institution (e.g., 1=university clinic, 2=planned hospital, etc.)
    GeneralEmergencyCare INT,          -- Level of general stationary emergency care (0=none, 1=basic, 2=extended, 3=comprehensive)
    -- Note: Assuming these are distinct columns for special emergency care modules.
    -- If they are meant to be a single column with multiple values, consider a separate linking table or JSON/TEXT field.
    SpecialEmergencyCare_Modul1 VARCHAR(255), -- Special stationary emergency care module 1
    SpecialEmergencyCare_Modul2 VARCHAR(255), -- Special stationary emergency care module 2
    SpecialEmergencyCare_Modul3 VARCHAR(255), -- Special stationary emergency care module 3
    SpecialEmergencyCare_Modul4 VARCHAR(255), -- Special stationary emergency care module 4
    SpecialEmergencyCare_Modul5 VARCHAR(255), -- Special stationary emergency care module 5
    TotalBeds INT,                     -- Total number of established beds (INSG)

    -- Detailed Bed Counts by Department (based on File 2's descriptions)
    Beds_100_118 INT,                  -- Internal Medicine
    Beds_102 INT,                      -- Internal Medicine/Geriatrics
    Beds_103 INT,                      -- Internal Medicine/Cardiology
    Beds_104 INT,                      -- Internal Medicine/Nephrology
    Beds_105 INT,                      -- Internal Medicine/Hematology and Internal Oncology
    Beds_106 INT,                      -- Internal Medicine/Endocrinology
    Beds_107 INT,                      -- Internal Medicine/Gastroenterology
    Beds_108 INT,                      -- Internal Medicine/Pneumology
    Beds_109 INT,                      -- Internal Medicine/Rheumatology
    Beds_114 INT,                      -- Internal Medicine/Pulmonary and Bronchial Medicine
    Beds_152 INT,                      -- Internal Medicine/Infectious Diseases
    Beds_153 INT,                      -- Internal Medicine/Diabetes
    Beds_154 INT,                      -- Internal Medicine/Naturopathy
    Beds_156 INT,                      -- Internal Medicine/Stroke units
    Beds_200 INT,                      -- Geriatrics
    Beds_300 INT,                      -- Cardiology
    Beds_400 INT,                      -- Nephrology
    Beds_500 INT,                      -- Hematology and Internal Oncology
    Beds_510 INT,                      -- Hematology and Internal Oncology/Pediatrics
    Beds_533 INT,                      -- Hematology and Internal Oncology/Radiotherapy
    Beds_600 INT,                      -- Endocrinology
    Beds_700 INT,                      -- Gastroenterology
    Beds_800 INT,                      -- Pneumology
    Beds_900 INT,                      -- Rheumatology
    Beds_1000_34 INT,                  -- Pediatrics
    Beds_1004 INT,                     -- Pediatrics/Nephrology
    Beds_1005 INT,                     -- Pediatrics/Hematology and Internal Oncology
    Beds_1007 INT,                     -- Pediatrics/Gastroenterology
    Beds_1009 INT,                     -- Pediatrics/Rheumatology
    Beds_1011 INT,                     -- Pediatrics/Pediatric Cardiology
    Beds_1012 INT,                     -- Pediatrics/Neonatology
    Beds_1014 INT,                     -- Pediatrics/Pulmonary and Bronchial Medicine
    Beds_1028 INT,                     -- Pediatrics/Pediatric Neurology
    Beds_1051 INT,                     -- Long-term care for children
    Beds_1100 INT,                     -- Pediatric Cardiology
    Beds_1200 INT,                     -- Neonatology
    Beds_1300 INT,                     -- Pediatric Surgery
    Beds_1400 INT,                     -- Pulmonary and Bronchial Medicine
    Beds_1500 INT,                     -- General Surgery
    Beds_1513 INT,                     -- General Surgery/Pediatric Surgery
    Beds_1516 INT,                     -- General Surgery/Trauma Surgery
    Beds_1518 INT,                     -- General Surgery/Vascular Surgery
    Beds_1519 INT,                     -- General Surgery/Plastic Surgery
    Beds_1520 INT,                     -- General Surgery/Thoracic Surgery
    Beds_1523 INT,                     -- Surgery/Orthopedics
    Beds_1536 INT,                     -- General Surgery/Intensive Care Medicine
    Beds_1550 INT,                     -- General Surgery/Abdominal and Vascular Surgery
    Beds_1551 INT,                     -- General Surgery/Hand Surgery
    Beds_1600_59 INT,                  -- Trauma Surgery
    Beds_1700_35 INT,                  -- Neurosurgery
    Beds_1800_28 INT,                  -- Vascular Surgery
    Beds_1900 INT,                     -- Plastic Surgery
    Beds_2000 INT,                     -- Thoracic Surgery
    Beds_2021 INT,                     -- Thoracic Surgery/Cardiac Surgery
    Beds_2100 INT,                     -- Cardiac Surgery
    Beds_2118 INT,                     -- Cardiac Surgery/Vascular Surgery
    Beds_2120 INT,                     -- Cardiac Surgery/Thoracic Surgery
    Beds_2136 INT,                     -- Cardiac Surgery/Intensive Care Medicine
    Beds_2200_39 INT,                  -- Urology
    Beds_2300 INT,                     -- Orthopedics
    Beds_2309 INT,                     -- Orthopedics/Rheumatology
    Beds_2315 INT,                     -- Orthopedics/Surgery
    Beds_2316 INT,                     -- Orthopedics and Trauma Surgery
    Beds_2400_41 INT,                  -- Gynecology and Obstetrics
    Beds_2405 INT,                     -- Gynecology/Hematology and Internal Oncology
    Beds_2406 INT,                     -- Gynecology/Endocrinology
    Beds_2425 INT,                     -- Gynecology
    Beds_2500 INT,                     -- Obstetrics
    Beds_2600 INT,                     -- Otorhinolaryngology (ENT)
    Beds_2700 INT,                     -- Ophthalmology
    Beds_2800_46 INT,                  -- Neurology
    Beds_2810 INT,                     -- Neurology/Pediatrics
    Beds_2851 INT,                     -- Neurology/Gerontology
    Beds_2852 INT,                     -- Neurology/Neurological Early Rehabilitation
    Beds_2856 INT,                     -- Neurology/Stroke Patients
    Beds_2900 INT,                     -- General Psychiatry
    Beds_2930 INT,                     -- General Psychiatry/Child and Adolescent Psychiatry
    Beds_2931 INT,                     -- General Psychiatry/Psychosomatics/Psychotherapy
    Beds_2950 INT,                     -- General Psychiatry/Addiction Treatment
    Beds_2951 INT,                     -- General Psychiatry/Gerontopsychiatry
    Beds_3000 INT,                     -- Child and Adolescent Psychiatry
    Beds_3100 INT,                     -- Psychosomatics/Psychotherapy
    Beds_3110 INT,                     -- Psychosomatics/Psychotherapy/Child and Adolescent Psychosomatics
    Beds_3200 INT,                     -- Nuclear Medicine
    Beds_3233 INT,                     -- Nuclear Medicine/Radiotherapy
    Beds_3300 INT,                     -- Radiotherapy
    Beds_3350 INT,                     -- Radiotherapy/Radiology
    Beds_3400 INT,                     -- Dermatology
    Beds_3500 INT,                     -- Dentistry and Oral and Maxillofacial Surgery
    Beds_3600 INT,                     -- Intensive Care Medicine
    Beds_3601 INT,                     -- Intensive Care Medicine/Internal Medicine
    Beds_3603 INT,                     -- Intensive Care Medicine/Cardiology
    Beds_3610 INT,                     -- Intensive Care Medicine/Pediatrics
    Beds_3617 INT,                     -- Intensive Care Medicine/Neurosurgery
    Beds_3618 INT,                     -- Intensive Care Medicine/Surgery
    Beds_3621 INT,                     -- Intensive Care Medicine/Cardiac Surgery
    Beds_3622 INT,                     -- Intensive Care Medicine/Urology
    Beds_3624 INT,                     -- Intensive Care Medicine/Gynecology and Obstetrics
    Beds_3626 INT,                     -- Intensive Care Medicine/Otorhinolaryngology (ENT)
    Beds_3628 INT,                     -- Intensive Care Medicine/Neurology
    Beds_3650 INT,                     -- Operative Intensive Care Medicine/Surgery
    Beds_3651 INT,                     -- Intensive Care Medicine/Thoracic-Cardiac Surgery
    Beds_3700 INT,                     -- Other Special Department
    Beds_3750 INT,                     -- Angiology
    Beds_3751 INT,                     -- Radiology
    Beds_3752 INT,                     -- Palliative Medicine
    Beds_3753 INT,                     -- Pain Therapy
    Beds_3754 INT,                     -- Curative Therapy Department
    Beds_3755 INT,                     -- Spinal Surgery
    Beds_3756 INT,                     -- Addiction Medicine
    Beds_3757 INT                      -- Visceral Surgery
);

-- Table for File 4: Hospital Facility Data (Summarized)
-- This table provides a summarized view of hospital facilities with broader bed count categories.
CREATE TABLE IF NOT EXISTS HospitalFacilitiesSummarized (
    id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each hospital entry
    Land VARCHAR(100),                 -- State or federal state in Germany
    Kreis VARCHAR(100),                -- District/County
    Gemeinde VARCHAR(100),             -- Municipality
    HospitalName VARCHAR(255),         -- Name of the hospital
    Street VARCHAR(255),               -- Street name
    HouseNumber VARCHAR(50),           -- House number
    PostalCode VARCHAR(20),            -- Postal code
    City VARCHAR(100),                 -- City/Town
    PhoneNumber VARCHAR(50),           -- Full telephone number (area code and number)
    EmailAddress VARCHAR(255),         -- Email address of the hospital
    InternetAddress VARCHAR(255),      -- Website address of the hospital
    OwnerType INT,                     -- Type of ownership (1=public, 2=non-profit, 3=private)
    OwnerName VARCHAR(255),            -- Name of the owner/operator
    InstitutionType INT,               -- Type of institution (e.g., 1=university clinic, 2=planned hospital, etc.)
    TotalBeds INT,                     -- Total number of established beds (INSG)

    -- Summarized Bed Counts by Major Department
    Beds_0 INT,                        -- Unknown/Unspecified beds (if this represents a general category)
    Beds_100 INT,                      -- Internal Medicine (main category)
    Beds_200 INT,                      -- Geriatrics (main category)
    Beds_300 INT,                      -- Cardiology (main category)
    Beds_400 INT,                      -- Nephrology (main category)
    Beds_500 INT,                      -- Hematology and Internal Oncology (main category)
    Beds_600 INT,                      -- Endocrinology (main category)
    Beds_700 INT,                      -- Gastroenterology (main category)
    Beds_800 INT,                      -- Pneumology (main category)
    Beds_900 INT,                      -- Rheumatology (main category)
    Beds_1000 INT,                     -- Pediatrics (main category)
    Beds_1400 INT,                     -- Pulmonary and Bronchial Medicine (main category)
    Beds_1500 INT,                     -- General Surgery (main category)
    Beds_1600 INT,                     -- Trauma Surgery (main category)
    Beds_1800 INT,                     -- Vascular Surgery (main category)
    Beds_2100 INT,                     -- Cardiac Surgery (main category)
    Beds_2200 INT,                     -- Urology (main category)
    Beds_2300 INT,                     -- Orthopedics (main category)
    Beds_2400 INT,                     -- Gynecology and Obstetrics (main category)
    Beds_2600 INT,                     -- Otorhinolaryngology (ENT) (main category)
    Beds_2700 INT,                     -- Ophthalmology (main category)
    Beds_2800 INT,                     -- Neurology (main category)
    Beds_2900 INT,                     -- General Psychiatry (main category)
    Beds_3000 INT,                     -- Child and Adolescent Psychiatry (main category)
    Beds_3100 INT,                     -- Psychosomatics/Psychotherapy (main category)
    Beds_3400 INT,                     -- Dermatology (main category)
    Beds_3700 INT,                     -- Other Special Department (main category)
    Beds_8200 INT,                     -- Unknown/Other department category
    Beds_8500_86 INT,                  -- Unknown/Other department category (range seems odd, consider renaming if possible)
    Beds_8600 INT,                     -- Unknown/Other department category
    Beds_8800 INT,                     -- Unknown/Other department category
    Beds_9000 INT                      -- Unknown/Other department category
);
"""

def create_database_if_not_exists(config):
    """
    Connects to MySQL (without specifying a database) and creates the specified database if it doesn't exist.
    """
    db_name = config['database']
    temp_config = {k: v for k, v in config.items() if k != 'database'} # Connect without specific database
    connection = None
    try:
        connection = mysql.connector.connect(**temp_config)
        cursor = connection.cursor()
        print(f"Attempting to create database '{db_name}' if it doesn't exist...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        connection.commit()
        print(f"Database '{db_name}' ensured to exist.")
        return True
    except Error as e:
        print(f"Error creating database '{db_name}': {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def create_tables(config, sql_statements):
    """
    Connects to the specified database and executes the CREATE TABLE statements.
    Each table creation uses IF NOT EXISTS to prevent errors if the table already exists.
    """
    connection = None
    try:
        connection = mysql.connector.connect(**config) # Connect to the specific database
        cursor = connection.cursor()

        # Split SQL statements by semicolon and execute each
        statements = [s.strip() for s in sql_statements.split(';') if s.strip()]

        for statement in statements:
            try:
                # Add IF NOT EXISTS to each CREATE TABLE statement if it's not already there
                if statement.upper().startswith("CREATE TABLE") and "IF NOT EXISTS" not in statement.upper():
                    statement = statement.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS", 1)

                print(f"Executing: {statement[:100]}...") # Print first 100 chars
                cursor.execute(statement)
                print("OK")
            except Error as err:
                # With IF NOT EXISTS, this error check is less critical for table existence,
                # but good for other potential DDL errors.
                print(f"Error executing statement: {err}")
                connection.rollback() # Rollback on error
                return False # Indicate failure
        connection.commit() # Commit all changes if no errors
        print("All tables created successfully (or already existed).")
        return True
    except Error as e:
        print(f"Error connecting to MySQL or during table creation: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    # Step 1: Ensure the database exists
    if create_database_if_not_exists(DB_CONFIG):
        # Step 2: Create the tables within that database
        if create_tables(DB_CONFIG, SQL_CREATE_TABLES):
            print("\nDatabase and tables setup complete.")
        else:
            print("\nTable creation failed.")
    else:
        print("\nDatabase creation failed, aborting table setup.")
