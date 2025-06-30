import src.create_table as create_table
import src.ingest_data as ingest
import src.transform as transform
import src.validation as validation
import src.visualization as visualization


def main():
    print("Step 1: Creating tables...")
    create_table.main()
    print("✅ Tables created.\n")

    print("Step 2: Ingesting data from Google Sheets...")
    ingest.main()
    print("✅ Data ingested.\n")

    print("Step 3: Running transformations...")
    transform.main()
    print("✅ Transformation done.\n")

    print("Step 4: Running validations...")
    validation.main()
    print("✅ Validations complete.\n")

    print("Step 5: Generating visualizations...")
    visualization.main()
    print("✅ Visualizations complete.\n")

if __name__ == "__main__":
    main()
