#!/usr/bin/env python3
"""
Create a sample dataset with numeric columns for EDA demonstration.
This creates a 'sample_health_metrics' table with realistic health data.
"""
from app.database import SessionLocal, engine
from app.models.eda_models import Dataset, DatasetColumn
from sqlalchemy import text

def create_sample_table():
    """Create a sample table with numeric health metrics."""
    
    # Create table with numeric columns
    create_table_sql = text("""
        CREATE TABLE IF NOT EXISTS public.sample_health_metrics (
            id SERIAL PRIMARY KEY,
            patient_age INTEGER,
            systolic_bp INTEGER,
            diastolic_bp INTEGER,
            heart_rate INTEGER,
            glucose_level DECIMAL(5,2),
            cholesterol DECIMAL(5,2),
            bmi DECIMAL(4,2),
            temperature DECIMAL(4,2),
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    with engine.connect() as conn:
        conn.execute(create_table_sql)
        conn.commit()
        print("✅ Created table: public.sample_health_metrics")
    
    # Insert sample data
    insert_data_sql = text("""
        INSERT INTO public.sample_health_metrics 
        (patient_age, systolic_bp, diastolic_bp, heart_rate, glucose_level, cholesterol, bmi, temperature)
        SELECT 
            (random() * 50 + 20)::INTEGER as patient_age,
            (random() * 40 + 100)::INTEGER as systolic_bp,
            (random() * 20 + 60)::INTEGER as diastolic_bp,
            (random() * 40 + 60)::INTEGER as heart_rate,
            (random() * 100 + 70)::DECIMAL(5,2) as glucose_level,
            (random() * 100 + 150)::DECIMAL(5,2) as cholesterol,
            (random() * 15 + 18)::DECIMAL(4,2) as bmi,
            (random() * 2 + 36.5)::DECIMAL(4,2) as temperature
        FROM generate_series(1, 100)
        ON CONFLICT DO NOTHING
    """)
    
    with engine.connect() as conn:
        result = conn.execute(insert_data_sql)
        conn.commit()
        print(f"✅ Inserted sample health metrics data")

def register_dataset():
    """Register the sample dataset in the datasets table."""
    db = SessionLocal()
    
    try:
        # Check if dataset already exists
        existing = db.query(Dataset).filter(Dataset.id == "sample-health-metrics").first()
        if existing:
            print("⚠️  Dataset 'sample-health-metrics' already exists")
            return
        
        # Create dataset entry
        dataset = Dataset(
            id="sample-health-metrics",
            name="Sample Health Metrics",
            schema_name="public",
            table_name="sample_health_metrics",
            consent_profile_id="demo-consent"
        )
        db.add(dataset)
        
        # Add column metadata
        columns = [
            ("id", "integer"),
            ("patient_age", "integer"),
            ("systolic_bp", "integer"),
            ("diastolic_bp", "integer"),
            ("heart_rate", "integer"),
            ("glucose_level", "numeric"),
            ("cholesterol", "numeric"),
            ("bmi", "numeric"),
            ("temperature", "numeric"),
            ("recorded_at", "timestamp")
        ]
        
        for col_name, col_type in columns:
            dataset_col = DatasetColumn(
                dataset_id="sample-health-metrics",
                column_name=col_name,
                data_type=col_type
            )
            db.add(dataset_col)
        
        db.commit()
        print("✅ Registered dataset: sample-health-metrics")
        print(f"   - Columns: {len(columns)}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating sample health metrics dataset...")
    create_sample_table()
    register_dataset()
    print("\n🎉 Sample dataset ready for EDA testing!")
    print("   Dataset ID: sample-health-metrics")
    print("   Numeric columns: patient_age, systolic_bp, diastolic_bp, heart_rate,")
    print("                    glucose_level, cholesterol, bmi, temperature")
