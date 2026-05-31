
### `docs/06_imaging_guide.md`

```markdown
# Imaging Guide

Imaging data covers radiology orders, imaging metadata, and radiology results.

## Standards

| Standard | Purpose |
|---|---|
| DICOM | Imaging metadata and image exchange |
| HL7 ORM | Radiology order |
| HL7 ORU | Radiology result |
| CPT | Billable imaging procedure |

## Generated Files

```text
data/generated/imaging/dicom_metadata.json
data/generated/imaging/radiology_order.hl7
data/generated/imaging/radiology_result.hl7
data/generated/imaging/xray_report.txt