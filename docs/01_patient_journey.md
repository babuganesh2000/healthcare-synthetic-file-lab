```markdown
# End-to-End Healthcare Patient Journey

## Core Healthcare Entities

1. Patient
2. Coverage
3. Encounter
4. Clinical Activity
5. Claim
6. Payment

---

## Healthcare Lifecycle

Patient
↓
Coverage
↓
Appointment
↓
Registration
↓
Encounter
↓
Clinical Activity
↓
Claim
↓
Payment
↓
AR Aging
↓
Collections

---

## Standards Mapping

| Stage | Standard |
|---------|---------|
| Enrollment | 834 |
| Eligibility | 270 / 271 |
| Registration | HL7 ADT |
| Scheduling | HL7 SIU |
| Lab Order | HL7 ORM |
| Lab Result | HL7 ORU |
| Clinical API | FHIR |
| Clinical Document | C-CDA |
| Professional Claim | 837P |
| Institutional Claim | 837I |
| Remittance | 835 |
| Pharmacy | NCPDP |
| Imaging | DICOM |
| Denials | CARC / RARC |