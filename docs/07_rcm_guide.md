
### `docs/07_rcm_guide.md`

```markdown
# Revenue Cycle Management Guide

Revenue Cycle Management tracks healthcare money from claim submission to payment, denial, patient balance, collections, and write-off.

## Core Concepts

| Concept | Meaning |
|---|---|
| Claim | Bill submitted to payer |
| Remittance | Payer payment response |
| EOB | Human-readable explanation of benefits |
| AR Aging | Outstanding balance by age |
| Denial | Rejected or underpaid claim |
| Collections | Delinquent balance recovery |
| Bad Debt | Written-off uncollectible amount |

## Generated Files

```text
data/generated/rcm/patient_statement.csv
data/generated/rcm/ar_aging.csv
data/generated/rcm/denial_workqueue.csv
data/generated/rcm/collections_placement.csv
data/generated/rcm/bad_debt_writeoff.csv