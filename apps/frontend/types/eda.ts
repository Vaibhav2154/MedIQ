
// Request Types
export interface BaseEdaRequest {
    dataset_id: string;
}

export interface SummaryStatsRequest extends BaseEdaRequest {
    columns: string[];
}
// Response Types
export interface SummaryStats {
    column: string;
    min: number | null;
    max: number | null;
    mean: number | null;
    median: number | null;
    std_dev: number | null;
    valid_count: number;
}

export interface UniqueValue {
    value: string | number;
    count: number;
}
export interface UniqueValuesOutput {
    unique_count: number;
    top_values: UniqueValue[];
}

export interface MissingAnalysisOutput {
    column: string;
    missing_percent: number;
    pattern_summary?: string;
}

export interface HistogramBin {
    range: string;
    count: number;
}
export interface HistogramOutput {
    bins: HistogramBin[];
    narrative?: string;
}

export interface BoxPlotOutput {
    median: number;
    iqr: number[];
    outlier_count: number;
}

export interface PercentilesOutput {
    percentiles: Record<string, number>;
}

export interface CorrelationItem {
    x: string;
    y: string;
    strength: string;
    value: number | null;
}
export interface CorrelationOutput {
    matrix: CorrelationItem[];
}

export interface ScatterPoint {
    x_bin: string;
    y_avg: number;
}
export interface ScatterOutput {
    points: ScatterPoint[];
    trend?: string;
}

export interface GroupItem {
    group: string | number;
    mean: number;
    count: number;
}
export interface GroupByOutput {
    groups: GroupItem[];
    narrative?: string;
}

export interface SegmentationOutput {
    segment_size: number;
    summary: Record<string, any>;
}

export interface TimeSeriesItem {
    time_period: string;
    mean: number;
}
export interface TimeTrendOutput {
    series: TimeSeriesItem[];
    key_changes?: string;
}

export interface OutlierOutput {
    outlier_count: number;
    range: number[];
    hint?: string;
}

export interface ReportOutput {
    report_url: string;
}
