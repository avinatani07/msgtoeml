"""Script to upload MSG files to Azurite and test the conversion"""
import os
import time
from azure.storage.blob import BlobServiceClient

# Connection string for Azurite with custom ports
connection_string = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10001/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10002/devstoreaccount1;TableEndpoint=http://127.0.0.1:10003/devstoreaccount1;"

def upload_msg_file(file_path):
    """Upload a MSG file to the input container"""
    try:
        # Create blob service client
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Get container client
        container_client = blob_service_client.get_container_client("msg-input")
        
        # Get filename
        filename = os.path.basename(file_path)
        
        # Read file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Upload
        blob_client = container_client.get_blob_client(filename)
        blob_client.upload_blob(file_data, overwrite=True)
        
        print(f"✅ Uploaded: {filename}")
        print(f"   Size: {len(file_data)} bytes")
        print(f"   Waiting for conversion...")
        
        return filename
        
    except Exception as e:
        print(f"❌ Error uploading file: {e}")
        return None

def check_conversion(filename, timeout=10):
    """Check if conversion completed"""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Expected EML filename
        eml_filename = filename.replace('.msg', '.eml')
        
        # Wait for conversion
        for i in range(timeout):
            time.sleep(1)
            
            # Check output container
            output_container = blob_service_client.get_container_client("eml-output")
            try:
                blob_client = output_container.get_blob_client(eml_filename)
                properties = blob_client.get_blob_properties()
                
                print(f"\n✅ CONVERSION SUCCESSFUL!")
                print(f"   Output file: {eml_filename}")
                print(f"   Size: {properties.size} bytes")
                print(f"   Created: {properties.creation_time}")
                
                # Download and show preview
                eml_content = blob_client.download_blob().readall()
                preview = eml_content.decode('utf-8', errors='ignore')[:500]
                print(f"\n📧 EML Preview:")
                print("=" * 60)
                print(preview)
                print("=" * 60)
                
                return True
            except:
                print(f"   Waiting... ({i+1}/{timeout}s)")
        
        # Check if file moved to failed
        failed_container = blob_service_client.get_container_client("msg-failed")
        blobs = list(failed_container.list_blobs())
        if blobs:
            print(f"\n⚠️ CONVERSION FAILED!")
            print(f"   File moved to: msg-failed/")
            for blob in blobs:
                print(f"   - {blob.name}")
        else:
            print(f"\n⏱️ TIMEOUT - Conversion taking longer than {timeout}s")
        
        return False
        
    except Exception as e:
        print(f"❌ Error checking conversion: {e}")
        return False

def list_containers():
    """List all containers and their contents"""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        print("\n📁 Container Status:")
        print("=" * 60)
        
        for container_name in ["msg-input", "eml-output", "msg-archive", "msg-failed"]:
            container_client = blob_service_client.get_container_client(container_name)
            blobs = list(container_client.list_blobs())
            
            print(f"\n{container_name}/ ({len(blobs)} files)")
            for blob in blobs:
                print(f"  - {blob.name} ({blob.size} bytes)")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error listing containers: {e}")

if __name__ == "__main__":
    print("🧪 MSG to EML Converter - Test Script")
    print("=" * 60)
    
    # Check if MSG file provided
    import sys
    if len(sys.argv) < 2:
        print("\nUsage: python test_upload.py <path_to_msg_file>")
        print("\nExample:")
        print("  python test_upload.py test.msg")
        print("  python test_upload.py C:\\path\\to\\email.msg")
        print("\nOr create a test MSG file first!")
        sys.exit(1)
    
    msg_file = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(msg_file):
        print(f"❌ File not found: {msg_file}")
        sys.exit(1)
    
    # Upload file
    print(f"\n📤 Uploading MSG file...")
    filename = upload_msg_file(msg_file)
    
    if filename:
        # Check conversion
        check_conversion(filename, timeout=15)
        
        # List all containers
        list_containers()
