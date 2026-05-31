from pathlib import Path
import json
import pandas as pd

MED_FILE = "data/synthea_output/csv/medications.csv"
PATIENT_FILE = "data/synthea_output/csv/patients.csv"
OUTPUT_DIR = "data/generated/pharmacy"


def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    patients = pd.read_csv(PATIENT_FILE)
    meds = pd.read_csv(MED_FILE)

    patient = patients.iloc[0]
    med = meds.iloc[0] if len(meds) > 0 else None

    ndc_ref = pd.DataFrame([
        {"ndc": "00054-0450-25", "drug_name": "Synthetic Insulin", "labeler": "Synthetic Pharma", "package": "10ML"},
        {"ndc": "00093-7424-56", "drug_name": "Synthetic Atorvastatin", "labeler": "Synthetic Pharma", "package": "30 TABLETS"},
    ])

    rxnorm_ref = pd.DataFrame([
        {"rxnorm": "860975", "drug_name": "Metformin 500 MG Oral Tablet"},
        {"rxnorm": "617314", "drug_name": "Atorvastatin 20 MG Oral Tablet"},
    ])

    pharmacy_claim = {
        "transaction_type": "NCPDP-like Pharmacy Claim",
        "patient_id": patient["Id"],
        "patient_name": f"{patient['FIRST']} {patient['LAST']}",
        "ndc": "00054-0450-25",
        "rxnorm": "860975",
        "drug_name": str(med["DESCRIPTION"]) if med is not None and "DESCRIPTION" in meds.columns else "Synthetic Medication",
        "days_supply": 30,
        "quantity": 30,
        "ingredient_cost": 42.50,
        "dispensing_fee": 2.00,
        "patient_pay": 10.00,
    }

    new_rx = {
        "transaction_type": "NCPDP SCRIPT NewRx-like",
        "patient_id": patient["Id"],
        "prescriber_npi": "1234567893",
        "pharmacy_npi": "1987654321",
        "medication": pharmacy_claim["drug_name"],
        "sig": "Take one tablet by mouth daily",
        "quantity": 30,
        "refills": 2,
    }

    ndc_ref.to_csv(Path(OUTPUT_DIR) / "ndc_reference.csv", index=False)
    rxnorm_ref.to_csv(Path(OUTPUT_DIR) / "rxnorm_reference.csv", index=False)

    Path(OUTPUT_DIR, "ncpdp_pharmacy_claim.json").write_text(json.dumps(pharmacy_claim, indent=2))
    Path(OUTPUT_DIR, "ncpdp_script_new_rx.json").write_text(json.dumps(new_rx, indent=2))

    print(f"Created pharmacy files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()