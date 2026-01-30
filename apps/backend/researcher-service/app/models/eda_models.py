
from sqlalchemy import Column, String, Integer, ForeignKey
from app.database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    schema_name = Column(String)
    # Assuming table_name exists or we derive it. Adding it for completeness.
    # If it doesn't exist in DB, this might cause issues, but for now it's needed for the logic.
    table_name = Column(String, nullable=True) 
    consent_profile_id = Column(String)

class DatasetColumn(Base):
    __tablename__ = "dataset_columns"

    dataset_id = Column(String, ForeignKey("datasets.id"), primary_key=True)
    column_name = Column(String, primary_key=True)
    data_type = Column(String)
