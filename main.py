from pathlib import Path
import subprocess
import sys

import psycopg2

from src.database import get_connection


BASE_DIR = Path(__file__).resolve().parent


def run_python_script(script_name):
    print()
    print("=" * 60)
    print(f"RUNNING: {script_name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(BASE_DIR / "src" / script_name)],
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{script_name} failed with exit code "
            f"{result.returncode}"
        )


def execute_sql_file(file_name):
    print()
    print("=" * 60)
    print(f"EXECUTING SQL: {file_name}")
    print("=" * 60)

    sql_file = BASE_DIR / "sql" / file_name

    with open(sql_file, "r", encoding="utf-8") as file:
        sql = file.read()

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(sql)
        connection.commit()

        print(f"Successfully executed {file_name}")

    except Exception as error:
        connection.rollback()

        print("SQL execution failed:")
        print(error)

        raise

    finally:
        cursor.close()
        connection.close()

        print("Database connection closed.")


def run_pipeline():
    print()
    print("=" * 60)
    print("TELECONNECT DATA ENGINEERING PIPELINE")
    print("=" * 60)

    # Step 1: Validate and process source data
    run_python_script("process_all.py")

    # Step 2: Load valid data into staging
    run_python_script("load_processed_to_staging.py")

    # Step 3: Load staging data into data warehouse
    execute_sql_file("load_dw.sql")

    print()
    print("=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()