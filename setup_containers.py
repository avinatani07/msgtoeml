"""Script to create required blob containers in Azurite"""
from azure.storage.blob import BlobServiceClient

# Connection string for Azurite with custom ports
connection_string = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10001/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10002/devstoreaccount1;TableEndpoint=http://127.0.0.1:10003/devstoreaccount1;"

# Container names
containers = [
    "msg-input",
    "eml-output",
    "msg-archive",
    "msg-failed"
]

try:
    # Create blob service client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    print("Creating containers in Azurite...")
    
    # Create each container
    for container_name in containers:
        try:
            container_client = blob_service_client.create_container(container_name)
            print(f"✓ Created container: {container_name}")
        except Exception as e:
            if "ContainerAlreadyExists" in str(e):
                print(f"✓ Container already exists: {container_name}")
            else:
                print(f"✗ Error creating {container_name}: {e}")
    
    print("\n✅ All containers ready!")
    print("\nYou can now run: func start")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure Azurite is running:")
    print("  azurite --silent --location ./__azurite__ --blobPort 10001 --queuePort 10002 --tablePort 10003")
