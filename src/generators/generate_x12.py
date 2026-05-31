from pathlib import Path
import pandas as pd

PATIENT_FILE = "data/synthea_output/csv/patients.csv"
CLAIMS_FILE = "data/synthea_output/csv/claims.csv"
CLAIM_LINES_FILE = "data/synthea_output/csv/claims_transactions.csv"
OUTPUT_DIR = "data/generated/x12"


def clean(value, length=20):
    return str(value).replace("-", "").replace(" ", "").replace(",", "")[:length]


def create_270(patient):
    patient_id = clean(patient["Id"])
    first = patient["FIRST"]
    last = patient["LAST"]
    dob = str(patient["BIRTHDATE"]).replace("-", "")
    gender = patient["GENDER"]

    return f"""ISA*00*          *00*          *ZZ*SYNTHPROVIDER  *ZZ*SYNTHPAYER     *260530*0900*^*00501*000000001*0*T*:~
GS*HS*SYNTHPROVIDER*SYNTHPAYER*20260530*0900*1*X*005010X279A1~
ST*270*0001*005010X279A1~
BHT*0022*13*10001234*20260530*0900~
HL*1**20*1~
NM1*PR*2*SYNTHETIC PAYER*****PI*99999~
HL*2*1*21*1~
NM1*1P*2*SYNTHETIC PROVIDER*****XX*1234567893~
HL*3*2*22*0~
TRN*1*93175012547*9877281234~
NM1*IL*1*{last}*{first}****MI*{patient_id}~
DMG*D8*{dob}*{gender}~
DTP*291*D8*20260530~
EQ*30~
SE*13*0001~
GE*1*1~
IEA*1*000000001~"""


def create_271(patient):
    patient_id = clean(patient["Id"])
    first = patient["FIRST"]
    last = patient["LAST"]
    dob = str(patient["BIRTHDATE"]).replace("-", "")
    gender = patient["GENDER"]

    return f"""ISA*00*          *00*          *ZZ*SYNTHPAYER     *ZZ*SYNTHPROVIDER  *260530*0901*^*00501*000000002*0*T*:~
GS*HB*SYNTHPAYER*SYNTHPROVIDER*20260530*0901*2*X*005010X279A1~
ST*271*0002*005010X279A1~
BHT*0022*11*10001234*20260530*0901~
HL*1**20*1~
NM1*PR*2*SYNTHETIC PAYER*****PI*99999~
HL*2*1*21*1~
NM1*1P*2*SYNTHETIC PROVIDER*****XX*1234567893~
HL*3*2*22*0~
TRN*2*93175012547*9877281234~
NM1*IL*1*{last}*{first}****MI*{patient_id}~
DMG*D8*{dob}*{gender}~
EB*1**30**ACTIVE COVERAGE~
DTP*291*D8*20260530~
SE*13*0002~
GE*1*2~
IEA*1*000000002~"""


def create_837p(patient, claim, line):
    patient_id = clean(patient["Id"])
    claim_id = clean(claim["Id"])
    first = patient["FIRST"]
    last = patient["LAST"]
    dob = str(patient["BIRTHDATE"]).replace("-", "")
    gender = patient["GENDER"]
    charge = float(line["AMOUNT"])
    proc = str(line["PROCEDURECODE"])

    return f"""ISA*00*          *00*          *ZZ*SYNTHPROVIDER  *ZZ*SYNTHPAYER     *260530*0930*^*00501*000000003*0*T*:~
GS*HC*SYNTHPROVIDER*SYNTHPAYER*20260530*0930*3*X*005010X222A1~
ST*837*0003*005010X222A1~
BHT*0019*00*{claim_id}*20260530*0930*CH~
NM1*41*2*SYNTHETIC BILLING PROVIDER*****46*123456789~
PER*IC*SYNTH CONTACT*TE*9725551111~
NM1*40*2*SYNTHETIC PAYER*****46*99999~
HL*1**20*1~
NM1*85*2*SYNTHETIC CLINIC*****XX*1234567893~
N3*100 HEALTHCARE DR~
N4*DALLAS*TX*75201~
HL*2*1*22*0~
SBR*P*18*******CI~
NM1*IL*1*{last}*{first}****MI*{patient_id}~
DMG*D8*{dob}*{gender}~
CLM*{claim_id}*{charge:.2f}***11:B:1*Y*A*Y*I~
HI*ABK:Z0000~
LX*1~
SV1*HC:99213*{charge:.2f}*UN*1***1~
DTP*472*D8*20260530~
SE*24*0003~
GE*1*3~
IEA*1*000000003~"""


def create_835(patient, claim, line):
    claim_id = clean(claim["Id"])
    patient_name = f"{patient['LAST']} {patient['FIRST']}"
    charge = float(line["AMOUNT"])
    allowed = round(charge * 0.80, 2)
    paid = round(allowed * 0.75, 2)
    patient_resp = round(allowed - paid, 2)
    adjustment = round(charge - allowed, 2)

    return f"""ISA*00*          *00*          *ZZ*SYNTHPAYER     *ZZ*SYNTHPROVIDER  *260530*1000*^*00501*000000004*0*T*:~
GS*HP*SYNTHPAYER*SYNTHPROVIDER*20260530*1000*4*X*005010X221A1~
ST*835*0004~
BPR*I*{paid:.2f}*C*ACH*CCP*01*999999999*DA*123456789*1512345678**01*111111111*DA*987654321*20260530~
TRN*1*83500001*9999999999~
REF*EV*PROVIDER123~
DTM*405*20260530~
N1*PR*SYNTHETIC PAYER~
N1*PE*SYNTHETIC CLINIC*XX*1234567893~
CLP*{claim_id}*1*{charge:.2f}*{paid:.2f}*{patient_resp:.2f}*12*CTRL123*11*1~
NM1*QC*1*{patient_name}~
CAS*CO*45*{adjustment:.2f}~
CAS*PR*1*{patient_resp:.2f}~
SVC*HC:99213*{charge:.2f}*{paid:.2f}~
DTM*472*20260530~
SE*18*0004~
GE*1*4~
IEA*1*000000004~"""


def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    patients = pd.read_csv(PATIENT_FILE)
    claims = pd.read_csv(CLAIMS_FILE)
    lines = pd.read_csv(CLAIM_LINES_FILE)

    patient = patients.iloc[0]
    claim = claims.iloc[0]
    line = lines.iloc[0]

    files = {
        "270_Eligibility_Request.edi": create_270(patient),
        "271_Eligibility_Response.edi": create_271(patient),
        "837P_Professional_Claim.edi": create_837p(patient, claim, line),
        "835_Remittance_Advice.edi": create_835(patient, claim, line),
    }

    for name, content in files.items():
        path = Path(OUTPUT_DIR) / name
        path.write_text(content + "\n")
        print(f"Created: {path}")


if __name__ == "__main__":
    main()