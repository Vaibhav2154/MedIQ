
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Any, Dict, Union

# --- Common Inputs ---

class BaseEdaRequest(BaseModel):
    dataset_id: str

class SummaryStatsRequest(BaseEdaRequest):
    columns: List[str]

class UniqueValuesRequest(BaseEdaRequest):
    column: str

class MissingAnalysisRequest(BaseEdaRequest):
    columns: List[str]

class HistogramRequest(BaseEdaRequest):
    column: str
    bins: int = 10

class BoxPlotRequest(BaseEdaRequest):
    column: str

class PercentilesRequest(BaseEdaRequest):
    column: str
    percentiles: List[float] = [25, 50, 75, 90]

class CorrelationRequest(BaseEdaRequest):
    columns: List[str]

class ScatterPlotRequest(BaseEdaRequest):
    x: str
    y: str

class GroupByRequest(BaseEdaRequest):
    group_column: str
    metric_column: str

class SegmentationRule(BaseModel):
    column: str
    operator: str
    value: Any

class SegmentationRequest(BaseEdaRequest):
    rules: List[SegmentationRule]

class TimeTrendRequest(BaseEdaRequest):
    column: str
    time_unit: str = "month"

class OutlierRequest(BaseEdaRequest):
    column: str

class ReportRequest(BaseEdaRequest):
    sections: List[str]

# --- Common Outputs ---

class SummaryStatsOutput(BaseModel):
    column: str
    min: Optional[float]
    max: Optional[float]
    mean: Optional[float]
    median: Optional[float]
    std_dev: Optional[float]
    valid_count: int

class UniqueValueItem(BaseModel):
    value: Any
    count: int

class UniqueValuesOutput(BaseModel):
    unique_count: int
    top_values: List[UniqueValueItem]

class MissingAnalysisOutput(BaseModel):
    column: str
    missing_percent: float
    pattern_summary: Optional[str]

class BinItem(BaseModel):
    range: str
    count: int

class HistogramOutput(BaseModel):
    bins: List[BinItem]
    narrative: Optional[str]

class BoxPlotOutput(BaseModel):
    median: float
    iqr: List[float]
    outlier_count: int

class PercentilesOutput(BaseModel):
    percentiles: Dict[str, float]

class CorrelationItem(BaseModel):
    x: str
    y: str
    strength: str
    value: Optional[float]

class CorrelationOutput(BaseModel):
    matrix: List[CorrelationItem]

class ScatterPoint(BaseModel):
    x_bin: str
    y_avg: float

class ScatterOutput(BaseModel):
    points: List[ScatterPoint]
    trend: Optional[str]

class GroupItem(BaseModel):
    group: Any
    mean: float
    count: int

class GroupByOutput(BaseModel):
    groups: List[GroupItem]
    narrative: Optional[str]

class SegmentationSummary(BaseModel):
    mean_age: Optional[float]
    mean_bp: Optional[float]
    metrics: Optional[Dict[str, Any]] = None

class SegmentationOutput(BaseModel):
    segment_size: int
    summary: Union[SegmentationSummary, Dict[str, Any]]

class TimeSeriesItem(BaseModel):
    time_period: str
    mean: float

class TimeTrendOutput(BaseModel):
    series: List[TimeSeriesItem]
    key_changes: Optional[str]

class OutlierOutput(BaseModel):
    outlier_count: int
    range: List[float]
    hint: Optional[str]

class ReportOutput(BaseModel):
    report_url: str
