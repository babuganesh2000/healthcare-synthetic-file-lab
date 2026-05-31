from pathlib import Path
import pandas as pd


PATIENT_FILE = "data/synthea_output/csv/patients.csv"
OUTPUT_DIR = "data/generated/hl7"


def create_adt_message(patient):

    patient_id = patient["Id"]

    first_name = patient["FIRST"]
    last_name = patient["LAST"]

    gender = patient["GENDER"]

    birth_date = str(patient["BIRTHDATE"]).replace("-", "")

    city = patient["CITY"]

    msg = f"""
MSH|^~\\&|SYNTHEA|HOSPITAL|LAB|DALLAS|20260530090000||ADT^A04|MSG00001|P|2.5
EVN|A04|20260530090000
PID|1||{patient_id}||{last_name}^{first_name}||{birth_date}|{gender}|||{city}
PV1|1|O
"""

    return msg.strip()

def create_orm_lab_order(patient):

    patient_id = patient["Id"]
    first_name = patient["FIRST"]
    last_name = patient["LAST"]
    birth_date = str(patient["BIRTHDATE"]).replace("-", "")
    gender = patient["GENDER"]

    msg = f"""
MSH|^~\\&|SYNTHEA|HOSPITAL|LAB|DALLAS|20260530091500||ORM^O01|MSG00002|P|2.5
PID|1||{patient_id}||{last_name}^{first_name}||{birth_date}|{gender}
ORC|NW|ORD00001
OBR|1|ORD00001|LAB00001|4548-4^Hemoglobin A1c^LOINC|||20260530091500
"""

    return msg.strip()

def create_oru_lab_result(patient):

    patient_id = patient["Id"]

    first_name = patient["FIRST"]
    last_name = patient["LAST"]

    birth_date = str(patient["BIRTHDATE"]).replace("-", "")

    gender = patient["GENDER"]

    msg = f"""
MSH|^~\\&|LAB|DALLAS|HOSPITAL|DALLAS|20260530100000||ORU^R01|MSG00003|P|2.5
PID|1||{patient_id}||{last_name}^{first_name}||{birth_date}|{gender}
OBR|1|ORD00001|LAB00001|4548-4^Hemoglobin A1c^LOINC
OBX|1|NM|4548-4^Hemoglobin A1c^LOINC||6.8|%|4.0-5.6|H
"""

    return msg.strip()

def create_siu_schedule(patient):

    patient_id = patient["Id"]
    first_name = patient["FIRST"]
    last_name = patient["LAST"]
    birth_date = str(patient["BIRTHDATE"]).replace("-", "")
    gender = patient["GENDER"]

    msg = f"""
MSH|^~\\&|SYNTHEA|SCHEDULING|HOSPITAL|DALLAS|20260530083000||SIU^S12|MSG00004|P|2.5
SCH|APT00001|APT00001|||||ROUTINE CHECKUP|30|MINUTES|||20260530090000
PID|1||{patient_id}||{last_name}^{first_name}||{birth_date}|{gender}
PV1|1|O
"""

    return msg.strip()

def create_dft_charge_transaction(patient):

    patient_id = patient["Id"]
    first_name = patient["FIRST"]
    last_name = patient["LAST"]
    birth_date = str(patient["BIRTHDATE"]).replace("-", "")
    gender = patient["GENDER"]

    msg = f"""
MSH|^~\\&|SYNTHEA|BILLING|HOSPITAL|DALLAS|20260530103000||DFT^P03|MSG00005|P|2.5
EVN|P03|20260530103000
PID|1||{patient_id}||{last_name}^{first_name}||{birth_date}|{gender}
FT1|1|20260530103000|20260530103000|CG|99213^Office Visit^CPT|1|125.00
DG1|1|ICD10|Z00.00^General adult medical examination without abnormal findings
"""

    return msg.strip()


def main():

    df = pd.read_csv(PATIENT_FILE)

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    patient = df.iloc[0]

    adt_message = create_adt_message(patient)
    orm_message = create_orm_lab_order(patient)
    oru_message = create_oru_lab_result(patient)
    siu_message = create_siu_schedule(patient)
    dft_message = create_dft_charge_transaction(patient)

    adt_file = Path(OUTPUT_DIR) / "ADT_A04.hl7"
    orm_file = Path(OUTPUT_DIR) / "ORM_O01_Lab_Order.hl7"
    oru_file = Path(OUTPUT_DIR) / "ORU_R01_Lab_Result.hl7"
    siu_file = Path(OUTPUT_DIR) / "SIU_S12_Appointment.hl7"
    dft_file = Path(OUTPUT_DIR) / "DFT_P03_Charge_Transaction.hl7"

    adt_file.write_text(adt_message + "\n")
    orm_file.write_text(orm_message + "\n")
    oru_file.write_text(oru_message + "\n")
    siu_file.write_text(siu_message + "\n")
    dft_file.write_text(dft_message + "\n")

    print(f"Created: {siu_file}")
    print(f"Created: {dft_file}")

    print(f"Created: {adt_file}")
    print(f"Created: {orm_file}")
    print(f"Created: {oru_file}")


if __name__ == "__main__":
    main()