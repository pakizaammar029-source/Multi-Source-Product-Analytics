import logging

from src.extract.api_client import (
    fetch_dummyjson,
    fetch_openbeautyfacts
)

from src.transform.clean_data import main as clean_pipeline
from src.validation.validate_data import validate_products
from src.load.load_data import load_data

from src.analysis.product_analytics import run_analytics
from src.analysis.data_quality import analyze_data_quality
from src.analysis.advanced_analysis import run_advanced_analysis
from src.analysis.visualize_data import visualize_data
from src.analysis.advanced_visualizations import create_advanced_visualizations
from src.analysis.submission_audit import run_submission_audit


# Configure logging
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


def main():

    print("\n" + "=" * 65)
    print("MULTI-SOURCE E-COMMERCE PRODUCT ANALYTICS")
    print("COMPLETE ETL AND ANALYTICS PIPELINE")
    print("=" * 65)

    steps = [
        ("Extract DummyJSON Data", fetch_dummyjson),
        ("Extract Open Beauty Facts Data", fetch_openbeautyfacts),
        ("Clean and Transform Data", clean_pipeline),
        ("Validate Data with Pydantic", validate_products),
        ("Load Data into SQLite Database", load_data),
        ("Basic Product Analytics", run_analytics),
        ("Data Quality Analysis", analyze_data_quality),
        ("Advanced Data Analysis", run_advanced_analysis),
        ("Basic Data Visualizations", visualize_data),
        ("Advanced Data Visualizations", create_advanced_visualizations),
        ("Final Submission Audit", run_submission_audit)
    ]

    total_steps = len(steps)

    for index, (name, function) in enumerate(steps, start=1):

        print(f"\n\nSTEP {index}/{total_steps}: {name}")
        print("-" * 65)

        logging.info("STARTED: %s", name)

        try:
            function()

            logging.info("SUCCESS: %s", name)
            print(f"\nSUCCESS: {name}")

        except Exception:
            logging.exception("FAILED: %s", name)

            print(f"\nFAILED: {name}")
            print("Check pipeline.log for error details.")

            raise

    print("\n" + "=" * 65)
    print("ALL PIPELINE STAGES COMPLETED SUCCESSFULLY!")
    print("ETL, VALIDATION, DATABASE, ANALYTICS AND AUDIT COMPLETED.")
    print("=" * 65)

    logging.info("COMPLETE PIPELINE EXECUTED SUCCESSFULLY")


if __name__ == "__main__":
    main()