"""Logging service for MSG to EML conversion"""
import os
import logging
from datetime import datetime
from typing import Optional


class ConversionLogger:
    """Provides structured logging for MSG to EML conversion operations"""
    
    def __init__(self, logger_name: str = 'msg_to_eml_converter'):
        """
        Initialize the conversion logger
        
        Args:
            logger_name: Name for the logger instance
        """
        self.logger = logging.getLogger(logger_name)
        
        # Configure log level from environment variable
        log_level = os.environ.get('FASTMCP_LOG_LEVEL', 'ERROR').upper()
        self.logger.setLevel(getattr(logging, log_level, logging.ERROR))
        
        # Add console handler if not already present
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_conversion_start(self, filename: str, file_size: int) -> None:
        """
        Logs conversion initiation
        
        Args:
            filename: Name of the MSG file being converted
            file_size: Size of the file in bytes
        """
        file_size_mb = file_size / (1024 * 1024)
        self.logger.info(
            f"Conversion started - filename: {filename}, "
            f"file_size: {file_size_mb:.2f} MB, "
            f"timestamp: {datetime.utcnow().isoformat()}"
        )
    
    def log_conversion_success(self, filename: str, duration: float, 
                               output_url: str) -> None:
        """
        Logs successful conversion with metrics
        
        Args:
            filename: Name of the MSG file that was converted
            duration: Conversion duration in seconds
            output_url: URL of the output EML blob
        """
        self.logger.info(
            f"Conversion successful - filename: {filename}, "
            f"duration: {duration:.3f}s, "
            f"output_url: {output_url}, "
            f"status: success, "
            f"timestamp: {datetime.utcnow().isoformat()}"
        )
    
    def log_conversion_failure(self, filename: str, error: Exception, 
                               duration: float) -> None:
        """
        Logs conversion failure with error details
        
        Args:
            filename: Name of the MSG file that failed to convert
            error: Exception that caused the failure
            duration: Time spent before failure in seconds
        """
        error_type = type(error).__name__
        error_message = str(error)
        
        self.logger.error(
            f"Conversion failed - filename: {filename}, "
            f"duration: {duration:.3f}s, "
            f"error_type: {error_type}, "
            f"error_message: {error_message}, "
            f"status: failed, "
            f"timestamp: {datetime.utcnow().isoformat()}"
        )
