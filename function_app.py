import azure.functions as func
import logging
import os
import time
from datetime import datetime
from services.msg_converter import MsgToEmlConverter, ConversionError, ValidationError
from services.blob_storage import BlobStorageService, BlobStorageError
from utils.logging import ConversionLogger
from models.conversion_models import ConversionResult

app = func.FunctionApp()

# Initialize services
converter = MsgToEmlConverter()
blob_service = BlobStorageService()
conversion_logger = ConversionLogger()

# Get container names from environment
INPUT_CONTAINER = os.environ.get('INPUT_CONTAINER', 'msg-input')
OUTPUT_CONTAINER = os.environ.get('OUTPUT_CONTAINER', 'eml-output')
ARCHIVE_CONTAINER = os.environ.get('ARCHIVE_CONTAINER', 'msg-archive')
FAILED_CONTAINER = os.environ.get('FAILED_CONTAINER', 'msg-failed')

# Timeout configuration (30 seconds)
TIMEOUT_SECONDS = 30


@app.blob_trigger(arg_name="inputBlob", 
                  path=f"{INPUT_CONTAINER}/{{name}}",
                  connection="AzureWebJobsStorage")
def msg_to_eml_converter(inputBlob: func.InputStream):
    """
    Azure Function triggered by blob upload to convert MSG files to EML format.
    
    Args:
        inputBlob: Input stream containing MSG file data
    """
    start_time = time.time()
    filename = inputBlob.name.split('/')[-1]  # Extract filename from blob path
    file_size = inputBlob.length
    
    # Log conversion start
    conversion_logger.log_conversion_start(filename, file_size)
    
    try:
        # Check timeout before starting conversion
        elapsed = time.time() - start_time
        if elapsed >= TIMEOUT_SECONDS:
            raise TimeoutError(
                f"Timeout exceeded before conversion started: {elapsed:.2f}s"
            )
        
        # Read MSG file from input blob stream
        msg_data = inputBlob.read()
        
        # Check timeout after reading
        elapsed = time.time() - start_time
        if elapsed >= TIMEOUT_SECONDS:
            raise TimeoutError(
                f"Timeout exceeded after reading file: {elapsed:.2f}s"
            )
        
        # Validate MSG format before conversion
        converter.validate_msg_format(msg_data)
        
        # Check timeout after validation
        elapsed = time.time() - start_time
        if elapsed >= TIMEOUT_SECONDS:
            raise TimeoutError(
                f"Timeout exceeded after validation: {elapsed:.2f}s"
            )
        
        # Convert MSG to EML
        eml_content = converter.convert(msg_data)
        
        # Check timeout after conversion
        elapsed = time.time() - start_time
        if elapsed >= TIMEOUT_SECONDS:
            raise TimeoutError(
                f"Timeout exceeded after conversion: {elapsed:.2f}s"
            )
        
        # Upload EML to output container
        output_url = blob_service.upload_eml(
            OUTPUT_CONTAINER, 
            filename, 
            eml_content
        )
        
        # Check timeout after upload
        elapsed = time.time() - start_time
        if elapsed >= TIMEOUT_SECONDS:
            raise TimeoutError(
                f"Timeout exceeded after upload: {elapsed:.2f}s"
            )
        
        # Archive original MSG file after successful conversion
        blob_service.archive_msg(
            INPUT_CONTAINER,
            filename,
            ARCHIVE_CONTAINER
        )
        
        # Calculate final duration
        duration = time.time() - start_time
        
        # Log successful conversion
        conversion_logger.log_conversion_success(filename, duration, output_url)
        
        logging.info(
            f"Successfully converted {filename} to EML in {duration:.3f}s. "
            f"Output: {output_url}"
        )
        
    except TimeoutError as e:
        # Handle timeout
        duration = time.time() - start_time
        conversion_logger.logger.error(
            f"Conversion timeout - filename: {filename}, "
            f"duration: {duration:.3f}s, "
            f"error_type: TimeoutError, "
            f"error_message: {str(e)}, "
            f"status: timeout, "
            f"timestamp: {datetime.utcnow().isoformat()}"
        )
        
        # Move to failed container
        try:
            blob_service.move_to_failed(INPUT_CONTAINER, filename, FAILED_CONTAINER)
        except BlobStorageError as move_error:
            logging.error(f"Failed to move timeout file to failed container: {move_error}")
        
        raise
        
    except ValidationError as e:
        # Handle validation errors
        duration = time.time() - start_time
        conversion_logger.log_conversion_failure(filename, e, duration)
        
        # Move to failed container
        try:
            blob_service.move_to_failed(INPUT_CONTAINER, filename, FAILED_CONTAINER)
        except BlobStorageError as move_error:
            logging.error(f"Failed to move invalid file to failed container: {move_error}")
        
        logging.error(f"Validation failed for {filename}: {str(e)}")
        raise
        
    except ConversionError as e:
        # Handle conversion errors
        duration = time.time() - start_time
        conversion_logger.log_conversion_failure(filename, e, duration)
        
        # Move to failed container
        try:
            blob_service.move_to_failed(INPUT_CONTAINER, filename, FAILED_CONTAINER)
        except BlobStorageError as move_error:
            logging.error(f"Failed to move failed file to failed container: {move_error}")
        
        logging.error(f"Conversion failed for {filename}: {str(e)}")
        raise
        
    except BlobStorageError as e:
        # Handle blob storage errors
        duration = time.time() - start_time
        conversion_logger.log_conversion_failure(filename, e, duration)
        
        logging.error(f"Blob storage error for {filename}: {str(e)}")
        raise
        
    except Exception as e:
        # Handle unexpected errors
        duration = time.time() - start_time
        conversion_logger.log_conversion_failure(filename, e, duration)
        
        # Try to move to failed container
        try:
            blob_service.move_to_failed(INPUT_CONTAINER, filename, FAILED_CONTAINER)
        except BlobStorageError as move_error:
            logging.error(f"Failed to move file to failed container: {move_error}")
        
        logging.error(f"Unexpected error converting {filename}: {str(e)}")
        raise
