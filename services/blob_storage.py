"""Azure Blob Storage service for MSG to EML converter"""
import os
import uuid
from datetime import datetime
from typing import Optional
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


class BlobStorageError(Exception):
    """Exception raised when blob storage operations fail"""
    pass


class BlobStorageService:
    """Handles Azure Blob Storage operations for MSG and EML files"""
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize the blob storage service
        
        Args:
            connection_string: Azure Storage connection string (default from env)
        """
        self.connection_string = connection_string or os.environ.get(
            'AzureWebJobsStorage'
        )
        
        if not self.connection_string:
            raise BlobStorageError(
                "Azure Storage connection string not provided and "
                "AzureWebJobsStorage environment variable not set"
            )
        
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(
                self.connection_string
            )
        except Exception as e:
            raise BlobStorageError(
                f"Failed to initialize BlobServiceClient: {str(e)}"
            ) from e
    
    def upload_eml(self, container: str, filename: str, content: bytes) -> str:
        """
        Uploads EML file to specified container
        
        Args:
            container: Target container name
            filename: Name for the EML file (original filename preserved)
            content: EML file content
            
        Returns:
            Blob URL of uploaded file
            
        Raises:
            BlobStorageError: If upload fails
        """
        try:
            # Get container client
            container_client = self.blob_service_client.get_container_client(container)
            
            # Generate EML filename with proper naming convention
            eml_filename = self._generate_eml_filename(container_client, filename)
            
            # Get blob client
            blob_client = container_client.get_blob_client(eml_filename)
            
            # Upload the content
            blob_client.upload_blob(content, overwrite=False)
            
            # Return the blob URL
            return blob_client.url
            
        except Exception as e:
            raise BlobStorageError(
                f"Failed to upload EML file '{filename}' to container '{container}': {str(e)}"
            ) from e
    
    def _generate_eml_filename(self, container_client: ContainerClient, 
                               original_filename: str) -> str:
        """
        Generate EML filename with proper naming convention
        
        Preserves original filename with .eml extension.
        Generates unique identifier for duplicate filenames.
        
        Args:
            container_client: Container client to check for existing files
            original_filename: Original MSG filename
            
        Returns:
            EML filename with proper extension and uniqueness
        """
        # Remove .msg extension if present and add .eml
        base_name = original_filename.rsplit('.', 1)[0] if '.' in original_filename else original_filename
        eml_filename = f"{base_name}.eml"
        
        # Check if file already exists
        blob_client = container_client.get_blob_client(eml_filename)
        
        try:
            # Check if blob exists
            blob_client.get_blob_properties()
            
            # File exists, generate unique identifier
            unique_id = str(uuid.uuid4())[:8]
            eml_filename = f"{base_name}_{unique_id}.eml"
            
        except Exception:
            # Blob doesn't exist, use original name
            pass
        
        return eml_filename

    def archive_msg(self, source_container: str, filename: str, 
                    archive_container: str) -> None:
        """
        Moves original MSG file to archive container
        
        Args:
            source_container: Source container name
            filename: MSG filename
            archive_container: Archive container name
            
        Raises:
            BlobStorageError: If archive operation fails
        """
        try:
            # Get source and destination blob clients
            source_blob_client = self.blob_service_client.get_blob_client(
                source_container, filename
            )
            
            # Generate timestamp-based name for archive
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
            extension = filename.rsplit('.', 1)[1] if '.' in filename else 'msg'
            archive_filename = f"{base_name}_{timestamp}.{extension}"
            
            dest_blob_client = self.blob_service_client.get_blob_client(
                archive_container, archive_filename
            )
            
            # Copy blob to archive container
            dest_blob_client.start_copy_from_url(source_blob_client.url)
            
            # Wait for copy to complete (for small files this is usually instant)
            # In production, you might want to check copy status
            
            # Delete the source blob
            source_blob_client.delete_blob()
            
        except Exception as e:
            raise BlobStorageError(
                f"Failed to archive MSG file '{filename}' from '{source_container}' "
                f"to '{archive_container}': {str(e)}"
            ) from e
    
    def move_to_failed(self, source_container: str, filename: str,
                       failed_container: str) -> None:
        """
        Moves failed MSG file to failed-conversion container
        
        Args:
            source_container: Source container name
            filename: MSG filename
            failed_container: Failed conversion container name
            
        Raises:
            BlobStorageError: If move operation fails
        """
        try:
            # Get source and destination blob clients
            source_blob_client = self.blob_service_client.get_blob_client(
                source_container, filename
            )
            
            # Generate timestamp-based name for failed file
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
            extension = filename.rsplit('.', 1)[1] if '.' in filename else 'msg'
            failed_filename = f"{base_name}_failed_{timestamp}.{extension}"
            
            dest_blob_client = self.blob_service_client.get_blob_client(
                failed_container, failed_filename
            )
            
            # Copy blob to failed container
            dest_blob_client.start_copy_from_url(source_blob_client.url)
            
            # Delete the source blob
            source_blob_client.delete_blob()
            
        except Exception as e:
            raise BlobStorageError(
                f"Failed to move MSG file '{filename}' from '{source_container}' "
                f"to '{failed_container}': {str(e)}"
            ) from e
