
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, AsyncMock
from app.main import app
from app.services.eda_service import EdaService
from app.schemas import eda_schema
from app.utils.auth import verify_jwt

# Mock Auth to bypass JWT validation
@pytest.fixture
def mock_auth():
    with patch("app.routers.eda_router.authenticate") as mock:
        mock.return_value = {"user_id": "test_user", "role": "researcher"}
        yield mock

@pytest.fixture
def mock_db():
    with patch("app.database.get_db") as mock:
        db_session = MagicMock()
        mock.return_value = db_session
        yield db_session

client = TestClient(app)

# Helper to mock endpoint service call if needed, but we want to test the full flow including service logic where possible.
# However, Service uses DB execution which requires active DB. We must mock the DB execution results.

@patch("app.routers.eda_router.authenticate")
@patch("app.services.eda_service.EdaService._get_table_ref")
@patch("app.services.eda_service.EdaService.get_summary_stats") # Mocking the service method directly for Integration Test of Router
def test_summary_stats(mock_method, mock_table_ref, mock_auth):
    mock_auth.return_value = {"user_id": "u1"}
    mock_table_ref.return_value = "public.data"
    
    # Mock return
    mock_method.return_value = [
        eda_schema.SummaryStatsOutput(
            column="age", min=20, max=80, mean=45.5, median=45, std_dev=10, valid_count=100
        )
    ]

    response = client.post("/eda/summary-stats", json={"dataset_id": "123", "columns": ["age"]})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["mean"] == 45.5

@patch("app.routers.eda_router.authenticate")
@patch("app.services.eda_service.EdaService.get_unique_values")
def test_unique_values(mock_method, mock_auth):
    mock_auth.return_value = {"user_id": "u1"}
    mock_method.return_value = eda_schema.UniqueValuesOutput(
        unique_count=5, 
        top_values=[{"value": "A", "count": 20}]
    )
    
    response = client.post("/eda/unique-values", json={"dataset_id": "123", "column": "category"})
    assert response.status_code == 200
    assert response.json()["unique_count"] == 5

@patch("app.routers.eda_router.authenticate")
@patch("app.services.eda_service.EdaService.get_histogram")
def test_histogram(mock_method, mock_auth):
    mock_auth.return_value = {"user_id": "u1"}
    mock_method.return_value = eda_schema.HistogramOutput(
        bins=[{"range": "0-10", "count": 50}],
        narrative="Test"
    )
    
    response = client.post("/eda/histogram", json={"dataset_id": "123", "column": "age", "bins": 5})
    assert response.status_code == 200
    assert response.json()["bins"][0]["count"] == 50

# --- SQL Generation Unit Tests (Service Layer) ---
# Testing that service generates correct SQL (mocking db.execute)

@patch("app.services.eda_service.Dataset")
def test_service_sql_generation():
    # Setup
    mock_db = MagicMock()
    service = EdaService(mock_db)
    
    # Mock Dataset lookup
    mock_dataset = MagicMock()
    mock_dataset.schema_name = "public"
    mock_dataset.table_name = "patients"
    mock_db.query.return_value.filter.return_value.first.return_value = mock_dataset
    
    # Mock DB execution for Unique Values
    mock_db.execute.return_value.fetchall.return_value = [MagicMock(val="A", cnt=15)]
    mock_db.execute.return_value.scalar.return_value = 10 # unique count
    
    # Run
    import asyncio
    req = eda_schema.UniqueValuesRequest(dataset_id="d1", column="diagnosis")
    res = asyncio.run(service.get_unique_values(req))
    
    # Verify basics
    assert res.top_values[0].value == "A"
    
    # Verify SQL calls
    # We can inspect mock_db.execute.call_args_list to see the SQL text
    args, _ = mock_db.execute.call_args_list[0]
    sql_text = str(args[0])
    assert "SELECT diagnosis as val, COUNT(*) as cnt" in sql_text
    assert "FROM public.patients" in sql_text

if __name__ == "__main__":
    # Allow running directly
    import sys
    from fastapi.testclient import TestClient
    sys.exit(pytest.main(["-v", __file__]))
