from pathlib import Path
import json
import pandas as pd

PATIENT_FILE = "data/synthea_output/csv/patients.csv"
OUTPUT_DIR = "data/generated/interoperability"


def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    patient = pd.read_csv(PATIENT_FILE).iloc[0]

    consent = {
        "resourceType": "Consent",
        "status": "active",
        "patient": {"reference": f"Patient/{patient['Id']}"},
        "scope": {
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/consentscope", "code": "patient-privacy"}]
        },
        "category": [{"text": "Patient consent for data exchange"}],
    }

    carin_eob = {
        "resourceType": "ExplanationOfBenefit",
        "id": "synthetic-carin-eob-001",
        "status": "active",
        "type": {"text": "Professional Claim"},
        "patient": {"reference": f"Patient/{patient['Id']}"},
        "use": "claim",
        "outcome": "complete",
        "insurer": {"display": "Synthetic Payer"},
        "provider": {"display": "Synthetic Provider"},
    }

    da_vinci_prior_auth = {
        "standard": "Da Vinci Prior Authorization-like request",
        "patient_id": patient["Id"],
        "requested_service": "MRI Lumbar Spine",
        "cpt": "72148",
        "diagnosis_icd10": "M54.50",
        "status": "submitted",
    }

    tefca_audit = {
        "exchange_framework": "TEFCA-like",
        "event": "patient_data_query",
        "requesting_organization": "Synthetic QHIN Participant",
        "responding_organization": "Synthetic Hospital",
        "patient_id": patient["Id"],
        "timestamp": "2026-05-30T10:00:00Z",
        "purpose_of_use": "Treatment",
    }

    Path(OUTPUT_DIR, "consent_record.json").write_text(json.dumps(consent, indent=2))
    Path(OUTPUT_DIR, "carin_blue_button_eob.json").write_text(json.dumps(carin_eob, indent=2))
    Path(OUTPUT_DIR, "da_vinci_prior_auth_request.json").write_text(json.dumps(da_vinci_prior_auth, indent=2))
    Path(OUTPUT_DIR, "tefca_exchange_audit.json").write_text(json.dumps(tefca_audit, indent=2))

    print(f"Created interoperability files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()