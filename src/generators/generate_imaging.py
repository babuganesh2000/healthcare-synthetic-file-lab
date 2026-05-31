from pathlib import Path
import json
import pandas as pd

PATIENT_FILE = "data/synthea_output/csv/patients.csv"
OUTPUT_DIR = "data/generated/imaging"


def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    patient = pd.read_csv(PATIENT_FILE).iloc[0]

    dicom_metadata = {
        "standard": "DICOM metadata only",
        "patient_id": patient["Id"],
        "study_instance_uid": "1.2.840.113619.2.55.3.604688654.123.20260530.1",
        "modality": "DX",
        "body_part_examined": "CHEST",
        "study_description": "Chest X-Ray",
        "series_description": "PA and Lateral Chest",
        "accession_number": "RAD000001",
    }

    report = """RADIOLOGY REPORT

Exam: Chest X-Ray
Findings: No acute cardiopulmonary abnormality.
Impression: Normal chest radiograph.
"""

    hl7_order = f"""MSH|^~\\&|HOSPITAL|DALLAS|RAD|DALLAS|20260530110000||ORM^O01|RADMSG001|P|2.5
PID|1||{patient['Id']}||{patient['LAST']}^{patient['FIRST']}
ORC|NW|RADORD0001
OBR|1|RADORD0001|RAD000001|71046^Chest X-Ray 2 Views^CPT
"""

    hl7_result = f"""MSH|^~\\&|RAD|DALLAS|HOSPITAL|DALLAS|20260530120000||ORU^R01|RADMSG002|P|2.5
PID|1||{patient['Id']}||{patient['LAST']}^{patient['FIRST']}
OBR|1|RADORD0001|RAD000001|71046^Chest X-Ray 2 Views^CPT
OBX|1|TX|RADIMP^Radiology Impression||Normal chest radiograph.
"""

    Path(OUTPUT_DIR, "dicom_metadata.json").write_text(json.dumps(dicom_metadata, indent=2))
    Path(OUTPUT_DIR, "xray_report.txt").write_text(report)
    Path(OUTPUT_DIR, "radiology_order.hl7").write_text(hl7_order)
    Path(OUTPUT_DIR, "radiology_result.hl7").write_text(hl7_result)

    print(f"Created imaging files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()