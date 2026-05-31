from pathlib import Path
import json
import pandas as pd

PATIENT_FILE = "data/synthea_output/csv/patients.csv"
CLAIMS_FILE = "data/synthea_output/csv/claims.csv"
CLAIM_LINES_FILE = "data/synthea_output/csv/claims_transactions.csv"
OUTPUT_DIR = "data/generated/eob"


def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    patient = pd.read_csv(PATIENT_FILE).iloc[0]
    claim = pd.read_csv(CLAIMS_FILE).iloc[0]
    line = pd.read_csv(CLAIM_LINES_FILE).iloc[0]

    charge = float(line["AMOUNT"])
    allowed = round(charge * 0.80, 2)
    paid = round(allowed * 0.75, 2)
    patient_resp = round(allowed - paid, 2)
    adjustment = round(charge - allowed, 2)

    eob = {
        "document_type": "Explanation of Benefits",
        "patient": f"{patient['FIRST']} {patient['LAST']}",
        "claim_id": claim["Id"],
        "service_date": claim["SERVICEDATE"],
        "procedure": str(line["NOTES"]),
        "charged_amount": charge,
        "allowed_amount": allowed,
        "insurance_paid": paid,
        "patient_responsibility": patient_resp,
        "adjustment": adjustment,
        "adjustment_reason": "CARC 45 - Charge exceeds fee schedule",
        "remark_code": "RARC N130 - Consult plan benefits",
    }

    json_path = Path(OUTPUT_DIR) / "eob_patient_explanation.json"
    txt_path = Path(OUTPUT_DIR) / "eob_patient_explanation.txt"
    csv_path = Path(OUTPUT_DIR) / "eob_patient_explanation.csv"

    json_path.write_text(json.dumps(eob, indent=2))
    pd.DataFrame([eob]).to_csv(csv_path, index=False)

    txt_path.write_text(
        f"""EXPLANATION OF BENEFITS

Patient: {eob['patient']}
Claim ID: {eob['claim_id']}
Service Date: {eob['service_date']}
Procedure: {eob['procedure']}

Charged Amount: ${charge:.2f}
Allowed Amount: ${allowed:.2f}
Insurance Paid: ${paid:.2f}
Patient Responsibility: ${patient_resp:.2f}
Adjustment: ${adjustment:.2f}

Reason:
{eob['adjustment_reason']}
{eob['remark_code']}
"""
    )

    print(f"Created: {json_path}")
    print(f"Created: {txt_path}")
    print(f"Created: {csv_path}")


if __name__ == "__main__":
    main()