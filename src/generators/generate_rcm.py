from pathlib import Path
import pandas as pd

PATIENT_FILE = "data/synthea_output/csv/patients.csv"
CLAIMS_FILE = "data/synthea_output/csv/claims.csv"
CLAIM_LINES_FILE = "data/synthea_output/csv/claims_transactions.csv"
OUTPUT_DIR = "data/generated/rcm"


def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    patient = pd.read_csv(PATIENT_FILE).iloc[0]
    claim = pd.read_csv(CLAIMS_FILE).iloc[0]
    line = pd.read_csv(CLAIM_LINES_FILE).iloc[0]

    charge = float(line["AMOUNT"])
    allowed = round(charge * 0.80, 2)
    paid = round(allowed * 0.50, 2)
    patient_balance = round(allowed - paid, 2)

    patient_statement = pd.DataFrame([{
        "patient_id": patient["Id"],
        "patient_name": f"{patient['FIRST']} {patient['LAST']}",
        "claim_id": claim["Id"],
        "statement_date": "2026-05-30",
        "balance_due": patient_balance,
        "due_date": "2026-06-30",
    }])

    ar_aging = pd.DataFrame([{
        "claim_id": claim["Id"],
        "patient_id": patient["Id"],
        "payer": "Synthetic Payer",
        "balance": patient_balance,
        "aging_bucket": "91-120",
        "status": "Delinquent",
    }])

    denial_workqueue = pd.DataFrame([{
        "claim_id": claim["Id"],
        "denial_code": "CARC 45",
        "remark_code": "RARC N130",
        "denial_reason": "Charge exceeds fee schedule",
        "workqueue_status": "Open",
    }])

    collections = pd.DataFrame([{
        "patient_id": patient["Id"],
        "claim_id": claim["Id"],
        "placement_date": "2026-09-30",
        "collection_agency": "Synthetic Collections Agency",
        "placed_amount": patient_balance,
        "status": "New Placement",
    }])

    writeoff = pd.DataFrame([{
        "claim_id": claim["Id"],
        "writeoff_date": "2026-12-31",
        "writeoff_type": "Bad Debt",
        "amount": patient_balance,
    }])

    patient_statement.to_csv(Path(OUTPUT_DIR) / "patient_statement.csv", index=False)
    ar_aging.to_csv(Path(OUTPUT_DIR) / "ar_aging.csv", index=False)
    denial_workqueue.to_csv(Path(OUTPUT_DIR) / "denial_workqueue.csv", index=False)
    collections.to_csv(Path(OUTPUT_DIR) / "collections_placement.csv", index=False)
    writeoff.to_csv(Path(OUTPUT_DIR) / "bad_debt_writeoff.csv", index=False)

    print(f"Created RCM files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()