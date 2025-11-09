"""Data models for MSG to EML conversion logging and metrics"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ConversionResult:
    """Result of MSG to EML conversion operation"""
    success: bool
    filename: str
    input_size_bytes: int
    output_size_bytes: Optional[int]
    duration_seconds: float
    output_blob_url: Optional[str]
    error_message: Optional[str]
    timestamp: datetime


@dataclass
class ConversionMetrics:
    """Metrics for monitoring and logging"""
    filename: str
    file_size_mb: float
    conversion_duration_ms: int
    status: str  # 'success', 'failed', 'timeout'
    error_type: Optional[str]
    timestamp: datetime
