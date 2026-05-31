from pathlib import Path
import json
import pandas as pd

PATIENT_FILE = "data/synthea_output/csv/patients.csv"
OUTPUT_DIR = "data/generated/labs"


def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    patient = pd.read_csv(PATIENT_FILE).iloc[0]

    lab_rows = [
        {"loinc": "4548-4", "test": "Hemoglobin A1c", "value": 6.8, "unit": "%", "range": "4.0-5.6", "flag": "H"},
        {"loinc": "718-7", "test": "Hemoglobin", "value": 13.5, "unit": "g/dL", "range": "12.0-16.0", "flag": "N"},
        {"loinc": "2093-3", "test": "Total Cholesterol", "value": 220, "unit": "mg/dL", "range": "<200", "flag": "H"},
    ]

    pd.DataFrame(lab_rows).to_csv(Path(OUTPUT_DIR) / "loinc_lab_results.csv", index=False)

    fhir_observation = {
        "resourceType": "Observation",
        "status": "final",
        "subject": {"reference": f"Patient/{patient['Id']}"},
        "code": {
            "coding": [{"system": "http://loinc.org", "code": "4548-4", "display": "Hemoglobin A1c"}]
        },
        "valueQuantity": {"value": 6.8, "unit": "%"},
        "interpretation": [{"coding": [{"code": "H", "display": "High"}]}],
    }

    Path(OUTPUT_DIR, "fhir_observation_bloodwork.json").write_text(json.dumps(fhir_observation, indent=2))

    hl7 = f"""MSH|^~\\&|LAB|DALLAS|HOSPITAL|DALLAS|20260530100000||ORU^R01|LABMSG001|P|2.5
PID|1||{patient['Id']}||{patient['LAST']}^{patient['FIRST']}||{str(patient['BIRTHDATE']).replace("-", "")}|{patient['GENDER']}
OBR|1|ORD00001|LAB00001|24323-8^Basic Metabolic Panel^LOINC
OBX|1|NM|4548-4^Hemoglobin A1c^LOINC||6.8|%|4.0-5.6|H
OBX|2|NM|718-7^Hemoglobin^LOINC||13.5|g/dL|12.0-16.0|N
OBX|3|NM|2093-3^Total Cholesterol^LOINC||220|mg/dL|<200|H
"""
    Path(OUTPUT_DIR, "hl7_oru_bloodwork.hl7").write_text(hl7)

    print(f"Created lab files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()