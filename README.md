# Healthcare Synthetic File Lab

## Overview

Healthcare Synthetic File Lab is an end-to-end healthcare standards generation platform built on top of Synthea.

The project generates healthcare data in multiple healthcare standards including:

- FHIR
- HL7 v2
- C-CDA
- X12 EDI
- EOB
- Pharmacy Standards
- Imaging Standards
- Revenue Cycle Files
- Healthcare Interoperability Files

---

## Quick Start

### Clone Repository

```bash
git clone <repo-url>
cd healthcare-synthetic-file-lab


2. Create Python Environment
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
3. Clone Synthea

Synthea is not committed into this repo. Clone it locally inside the project folder.

git clone https://github.com/synthetichealth/synthea.git

Expected structure:

healthcare-synthetic-file-lab/
├── synthea/
├── src/
├── config/
├── docs/
└── README.md
4. Build and Test Synthea
cd synthea
./gradlew build check test
cd ..
5. Generate Base Synthetic Clinical Data
cd synthea
./run_synthea -p 10 Texas Dallas -c ../config/synthea.properties
cd ..

Expected output:

data/synthea_output/fhir
data/synthea_output/csv
data/synthea_output/ccda
6. Generate All Healthcare Standard Files
python src/generators/generate_all.py

Expected output:

data/generated/hl7
data/generated/x12
data/generated/eob
data/generated/pharmacy
data/generated/labs
data/generated/imaging
data/generated/rcm
data/generated/interoperability
7. Verify Generated Files
find data/generated -type f
8. Current Scope

This repo is focused only on generating synthetic healthcare standard files.

Included:

FHIR
C-CDA
HL7 v2
X12 EDI
EOB
Pharmacy
Labs
Imaging
RCM
Interoperability samples

Not included yet:

Snowflake loading
Databricks pipelines
dbt models
Warehouse modeling
Production validation
Real payer/provider certification