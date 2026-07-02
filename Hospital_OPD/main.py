from db_setup import create_tables
from seed_data import insert_sample_data
from views import (
    create_opd_analytics_view,
    create_department_daily_revenue_view
)
from queries import run_queries


def main():

    print("=" * 60)
    print("Hospital OPD Appointment and Billing Analytics")
    print("=" * 60)

    print("\nCreating Tables...")
    create_tables()

    print("\nInserting Sample Data...")
    insert_sample_data()

    print("\nCreating Views...")
    create_opd_analytics_view()
    create_department_daily_revenue_view()

    print("\nRunning Queries...")
    run_queries()

    print("\nProject Executed Successfully!")


if __name__ == "__main__":
    main()