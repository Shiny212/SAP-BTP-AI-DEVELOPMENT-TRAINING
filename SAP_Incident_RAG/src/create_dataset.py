from pathlib import Path
from datetime import datetime, timedelta
import random

import pandas as pd
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_ROOT / "data"

DATA_FOLDER.mkdir(exist_ok=True)

OUTPUT_FILE = DATA_FOLDER / "sap_incidents.xlsx"
random.seed(42)
official_incidents = [
    {
        "incident_id": "INC-1001",
        "incident_date": "2025-01-05",
        "sap_module": "SAP MM",
        "category": "Invoice Management",
        "priority": "P2",
        "issue_summary": "Supplier invoice blocked because of price variance",
        "issue_description": "Supplier invoice could not be posted because the invoice amount exceeded the allowed purchase order price variance.",
        "root_cause": "Incorrect purchase-order condition record",
        "resolution": "Corrected condition record and reprocessed invoice",
        "owner_team": "Procure-to-Pay Support",
        "resolution_time_hours": 3.5,
        "status": "Closed"
    },
    {
        "incident_id": "INC-1002",
        "incident_date": "2025-01-08",
        "sap_module": "SAP HANA",
        "category": "Database Availability",
        "priority": "P1",
        "issue_summary": "HANA database became unavailable",
        "issue_description": "Production SAP HANA database stopped responding during peak business hours.",
        "root_cause": "Severe memory exhaustion",
        "resolution": "Released memory, restarted service and adjusted allocation limits",
        "owner_team": "Database Platform Team",
        "resolution_time_hours": 5.0,
        "status": "Closed"
    },
    {
        "incident_id": "INC-1003",
        "incident_date": "2025-01-11",
        "sap_module": "SAP SD",
        "category": "Pricing",
        "priority": "P3",
        "issue_summary": "Incorrect discount in sales order",
        "issue_description": "Sales orders applied an incorrect customer discount during order creation.",
        "root_cause": "Incorrect pricing procedure sequence",
        "resolution": "Corrected condition sequence and repriced order",
        "owner_team": "Order-to-Cash Support",
        "resolution_time_hours": 1.2,
        "status": "Closed"
    },
    {
        "incident_id": "INC-1004",
        "incident_date": "2025-01-14",
        "sap_module": "SAP BTP",
        "category": "Connectivity",
        "priority": "P1",
        "issue_summary": "Application could not connect to backend system",
        "issue_description": "BTP application failed to establish a connection with the SAP backend.",
        "root_cause": "Expired destination credentials",
        "resolution": "Renewed credentials and corrected destination properties",
        "owner_team": "BTP Platform Team",
        "resolution_time_hours": 7.5,
        "status": "Closed"
    },
    {
        "incident_id": "INC-1005",
        "incident_date": "2025-01-18",
        "sap_module": "SAP SuccessFactors",
        "category": "Integration",
        "priority": "P2",
        "issue_summary": "Employee replication was delayed",
        "issue_description": "Employee master data replication from SuccessFactors was delayed.",
        "root_cause": "Mapping error in integration flow",
        "resolution": "Corrected mapping and reran integration job",
        "owner_team": "HR Integration Team",
        "resolution_time_hours": 4.0,
        "status": "Closed"
    },
    {
        "incident_id": "INC-1006",
        "incident_date": "2025-01-22",
        "sap_module": "SAP HANA",
        "category": "Performance",
        "priority": "P1",
        "issue_summary": "Critical transactions became slow",
        "issue_description": "Users experienced severe performance degradation during transaction processing.",
        "root_cause": "Long-running savepoint and storage pressure",
        "resolution": "Corrected storage pressure and optimized workload",
        "owner_team": "Database Platform Team",
        "resolution_time_hours": 9.0,
        "status": "Closed"
    },
    {
        "incident_id": "INC-1007",
        "incident_date": "2025-01-26",
        "sap_module": "SAP MM",
        "category": "Purchase Order",
        "priority": "P3",
        "issue_summary": "Purchase order release was not triggered",
        "issue_description": "Purchase order approval workflow was not triggered after submission.",
        "root_cause": "Incorrect release strategy configuration",
        "resolution": "Corrected release strategy and regenerated classification",
        "owner_team": "Procure-to-Pay Support",
        "resolution_time_hours": 2.5,
        "status": "Closed"
    },
    {
        "incident_id": "INC-1008",
        "incident_date": "2025-01-29",
        "sap_module": "SAP BTP",
        "category": "Authorization",
        "priority": "P2",
        "issue_summary": "User could not access deployed application",
        "issue_description": "User received authorization errors while accessing the deployed application.",
        "root_cause": "Missing role collection assignment",
        "resolution": "Assigned required role collection",
        "owner_team": "BTP Platform Team",
        "resolution_time_hours": 1.8,
        "status": "Closed"
    }
]
sap_modules = [
    "SAP MM",
    "SAP SD",
    "SAP FI",
    "SAP CO",
    "SAP PP",
    "SAP QM",
    "SAP PM",
    "SAP HCM",
    "SAP SuccessFactors",
    "SAP BTP",
    "SAP HANA",
    "SAP BW",
    "SAP Fiori"
]
priorities = [
    "P1",
    "P2",
    "P3",
    "P4"
]
categories = [
    "Authorization",
    "Performance",
    "Pricing",
    "Integration",
    "Database",
    "Connectivity",
    "Purchase Order",
    "Invoice Management",
    "Workflow",
    "Master Data",
    "Replication",
    "Reporting",
    "Background Job",
    "User Management",
    "Transport",
    "Security",
    "Batch Processing"
]
owner_teams = [
    "Procure-to-Pay Support",
    "Order-to-Cash Support",
    "Finance Support",
    "Production Planning Team",
    "Basis Team",
    "SAP Security Team",
    "Database Platform Team",
    "BTP Platform Team",
    "HR Integration Team",
    "Analytics Team"
]
module_templates = {

    "SAP MM": [
        {
            "category": "Purchase Order",
            "summary": "Purchase order release workflow failed",
            "description": "Approval workflow was not triggered after purchase order creation.",
            "cause": "Incorrect release strategy configuration",
            "resolution": "Corrected release strategy configuration."
        },
        {
            "category": "Invoice Management",
            "summary": "Supplier invoice blocked",
            "description": "Invoice posting failed because of price variance.",
            "cause": "Incorrect pricing condition",
            "resolution": "Updated pricing condition and reposted invoice."
        }
    ],

    "SAP SD": [
        {
            "category": "Pricing",
            "summary": "Incorrect customer discount",
            "description": "Sales order pricing calculation was incorrect.",
            "cause": "Pricing procedure configuration",
            "resolution": "Updated pricing procedure."
        },
        {
            "category": "Sales Order",
            "summary": "Sales order could not be created",
            "description": "Customer order creation failed.",
            "cause": "Missing master data",
            "resolution": "Maintained customer master records."
        }
    ],

    "SAP HANA": [
        {
            "category": "Database",
            "summary": "Database memory utilization exceeded threshold",
            "description": "Memory utilization exceeded safe operating limits.",
            "cause": "Memory exhaustion",
            "resolution": "Released memory and optimized workload."
        },
        {
            "category": "Performance",
            "summary": "Critical transactions became slow",
            "description": "Database performance degraded significantly.",
            "cause": "Long-running savepoint",
            "resolution": "Optimized SQL execution."
        }
    ],

    "SAP BTP": [
        {
            "category": "Connectivity",
            "summary": "Application could not connect to backend",
            "description": "Destination configuration failed.",
            "cause": "Expired destination credentials",
            "resolution": "Updated destination configuration."
        },
        {
            "category": "Authorization",
            "summary": "User authorization failed",
            "description": "User could not access deployed application.",
            "cause": "Missing role collection",
            "resolution": "Assigned role collection."
        }
    ],

    "SAP SuccessFactors": [
        {
            "category": "Integration",
            "summary": "Employee replication delayed",
            "description": "Employee synchronization failed.",
            "cause": "Integration mapping issue",
            "resolution": "Corrected mapping and restarted replication."
        }
    ]
}
status_list = [
    "Closed",
    "Resolved",
    "Completed"
]
base_date = datetime(2025, 2, 1)
generated_incidents = []

for incident_number in range(1009, 1251):

    module = random.choice(sap_modules)

if module in module_templates:
    template = random.choice(module_templates[module])
else:
    template = {
        "category": random.choice(categories),
        "summary": "General SAP issue",
        "description": "General enterprise application issue.",
        "cause": "Configuration mismatch",
        "resolution": "Configuration updated."
    }

    generated_incidents.append(
        {
            "incident_id": f"INC-{incident_number}",

            "incident_date": (
                base_date +
                timedelta(days=random.randint(0, 330))
            ).strftime("%Y-%m-%d"),

            "sap_module": module,

            "category": template["category"],

            "priority": random.choice(priorities),

            "issue_summary": template["summary"],

            "issue_description": template["description"],

            "root_cause": template["cause"],

            "resolution": template["resolution"],

            "owner_team": random.choice(owner_teams),

            "resolution_time_hours": round(
                random.uniform(0.5, 12.0),
                1
            ),

            "status": random.choice(status_list)
        }
    )
all_incidents = official_incidents + generated_incidents

df = pd.DataFrame(all_incidents)

df = df.sort_values(
    by="incident_id"
).reset_index(drop=True)

df.to_excel(
    OUTPUT_FILE,
    index=False
)

print("=" * 70)
print("SAP INCIDENT DATASET CREATED SUCCESSFULLY")
print("=" * 70)
print(f"Total Records : {len(df)}")
print(f"Columns       : {len(df.columns)}")
print(f"Output File   : {OUTPUT_FILE}")
print("=" * 70)
print(f"Total Records : {len(df)}")

print(f"Columns       : {len(df.columns)}")

print(f"Output File   : {OUTPUT_FILE}")

print("=" * 70)