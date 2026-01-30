#!/usr/bin/env python3
"""
Seed sample datasets for EDA testing.
This creates dataset entries that point to existing health data tables.
"""
from app.database import SessionLocal
from app.models.eda_models import Dataset, DatasetColumn
from sqlalchemy import text

def get_table_columns(db, schema_name, table_name):
    """Get column names and types for a table."""
    query = text("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = :schema AND table_name = :table
        ORDER BY ordinal_position
    """)
    
    result = db.execute(query, {"schema": schema_name, "table": table_name})
    return [(row[0], row[1]) for row in result.fetchall()]

def seed_datasets():
    """Create sample datasets for testing."""
    db = SessionLocal()
    
    try:
        # Check if datasets already exist
        existing = db.query(Dataset).filter(Dataset.id == "patients-dataset").first()
        if existing:
            print("⚠️  Datasets already exist. Skipping seed.")
            return
        
        # Define datasets to create
        datasets_to_create = [
            {
                "id": "patients-dataset",
                "name": "Patient Demographics",
                "schema": "public",
                "table": "patients",
                "consent_profile": "patient-demographics-consent"
            },
            {
                "id": "observations-dataset",
                "name": "Clinical Observations",
                "schema": "public",
                "table": "observations",
                "consent_profile": "clinical-data-consent"
            },
            {
                "id": "medications-dataset",
                "name": "Medication Records",
                "schema": "public",
                "table": "medications",
                "consent_profile": "medication-consent"
            }
        ]
        
        for ds_info in datasets_to_create:
            # Create dataset
            dataset = Dataset(
                id=ds_info["id"],
                name=ds_info["name"],
                schema_name=ds_info["schema"],
                table_name=ds_info["table"],
                consent_profile_id=ds_info["consent_profile"]
            )
            db.add(dataset)
            
            # Get columns from the actual table
            columns = get_table_columns(db, ds_info["schema"], ds_info["table"])
            
            # Create dataset column metadata
            for col_name, col_type in columns:
                dataset_col = DatasetColumn(
                    dataset_id=ds_info["id"],
                    column_name=col_name,
                    data_type=col_type
                )
                db.add(dataset_col)
            
            print(f"✅ Created dataset: {ds_info['name']}")
            print(f"   - ID: {ds_info['id']}")
            print(f"   - Table: {ds_info['schema']}.{ds_info['table']}")
            print(f"   - Columns: {len(columns)}")
        
        db.commit()
        print("\n🎉 All datasets created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding datasets: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_datasets()
