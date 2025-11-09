"""MSG to EML conversion service"""
import io
import os
from typing import Optional
from extract_msg import Message


class ConversionError(Exception):
    """Exception raised when MSG to EML conversion fails"""
    pass


class ValidationError(Exception):
    """Exception raised when MSG file validation fails"""
    pass


class MsgToEmlConverter:
    """Converts Microsoft Outlook MSG files to standard EML format"""
    
    def __init__(self, max_file_size_mb: Optional[int] = None):
        """
        Initialize the converter
        
        Args:
            max_file_size_mb: Maximum file size in MB (default from env or 25 MB)
        """
        self.max_file_size_mb = max_file_size_mb or int(
            os.environ.get('MAX_FILE_SIZE_MB', '25')
        )
    
    def validate_msg_format(self, msg_data: bytes) -> None:
        """
        Validates that input data is a valid MSG file
        
        Args:
            msg_data: Raw MSG file content
            
        Raises:
            ValidationError: If validation fails with descriptive error message
        """
        # Check if data is empty
        if not msg_data:
            raise ValidationError("MSG file is empty")
        
        # Validate file size
        file_size_mb = len(msg_data) / (1024 * 1024)
        if file_size_mb > self.max_file_size_mb:
            raise ValidationError(
                f"File size {file_size_mb:.2f} MB exceeds maximum allowed "
                f"size of {self.max_file_size_mb} MB"
            )
        
        # Check MSG file header (MSG files are OLE/CFB format)
        # OLE files start with signature: D0 CF 11 E0 A1 B1 1A E1
        msg_signature = b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1'
        
        if len(msg_data) < 8:
            raise ValidationError("File is too small to be a valid MSG file")
        
        if not msg_data[:8] == msg_signature:
            raise ValidationError(
                "Invalid MSG file format: file header does not match MSG signature"
            )

    def convert(self, msg_data: bytes) -> bytes:
        """
        Converts MSG file bytes to EML format
        
        Args:
            msg_data: Raw MSG file content
            
        Returns:
            EML file content as bytes
            
        Raises:
            ConversionError: If conversion fails
            ValidationError: If MSG file is invalid
        """
        # Validate MSG format first
        self.validate_msg_format(msg_data)
        
        try:
            # Create a BytesIO object from the MSG data
            msg_stream = io.BytesIO(msg_data)
            
            # Parse the MSG file using extract_msg
            msg = Message(msg_stream)
            
            # Generate EML format output
            eml_content = self._generate_eml(msg)
            
            # Close the message to free resources
            msg.close()
            
            return eml_content
            
        except ValidationError:
            # Re-raise validation errors as-is
            raise
        except Exception as e:
            raise ConversionError(f"Failed to convert MSG to EML: {str(e)}") from e
    
    def _generate_eml(self, msg: Message) -> bytes:
        """
        Generate EML format from parsed MSG data
        
        Args:
            msg: Parsed Message object
            
        Returns:
            EML content as bytes
        """
        try:
            # Build EML headers
            eml_lines = []
            
            # Add standard email headers
            if msg.sender:
                eml_lines.append(f"From: {self._encode_header(msg.sender)}")
            
            if msg.to:
                eml_lines.append(f"To: {self._encode_header(msg.to)}")
            
            if msg.cc:
                eml_lines.append(f"Cc: {self._encode_header(msg.cc)}")
            
            if msg.subject:
                eml_lines.append(f"Subject: {self._encode_header(msg.subject)}")
            
            if msg.date:
                eml_lines.append(f"Date: {msg.date}")
            
            # Add message ID if available
            if hasattr(msg, 'messageId') and msg.messageId:
                eml_lines.append(f"Message-ID: {msg.messageId}")
            
            # Add MIME version
            eml_lines.append("MIME-Version: 1.0")
            
            # Determine content type
            if msg.htmlBody:
                eml_lines.append("Content-Type: text/html; charset=utf-8")
                eml_lines.append("Content-Transfer-Encoding: 8bit")
                eml_lines.append("")  # Empty line before body
                eml_lines.append(msg.htmlBody)
            elif msg.body:
                eml_lines.append("Content-Type: text/plain; charset=utf-8")
                eml_lines.append("Content-Transfer-Encoding: 8bit")
                eml_lines.append("")  # Empty line before body
                eml_lines.append(msg.body)
            else:
                eml_lines.append("Content-Type: text/plain; charset=utf-8")
                eml_lines.append("")
                eml_lines.append("")
            
            # Join all lines with CRLF (standard for email)
            eml_content = "\r\n".join(eml_lines)
            
            # Encode to bytes using UTF-8
            return eml_content.encode('utf-8', errors='replace')
            
        except Exception as e:
            raise ConversionError(f"Failed to generate EML format: {str(e)}") from e
    
    def _encode_header(self, header_value: str) -> str:
        """
        Encode header value, handling special characters
        
        Args:
            header_value: Raw header value
            
        Returns:
            Encoded header value safe for EML format
        """
        if not header_value:
            return ""
        
        # Replace any problematic characters
        # Remove or replace control characters except tab
        encoded = ''.join(
            char if (ord(char) >= 32 or char == '\t') else ' '
            for char in header_value
        )
        
        # Ensure proper encoding for non-ASCII characters
        try:
            # Try to encode as ASCII first
            encoded.encode('ascii')
            return encoded
        except UnicodeEncodeError:
            # If non-ASCII characters present, they'll be handled by UTF-8 encoding
            return encoded
