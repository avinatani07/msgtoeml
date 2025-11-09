# Quick Start Guide

## 🎯 Get Running in 5 Minutes

### **Option A: Local Testing (No Azure Account Needed)**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# 3. Install Azurite (Storage Emulator)
npm install -g azurite

# 4. Start Azurite (Terminal 1)
azurite --silent --location ./__azurite__

# 5. Start Function (Terminal 2)
func start

# 6. Create containers (Terminal 3)
az storage container create --name msg-input --connection-string "UseDevelopmentStorage=true"
az storage container create --name eml-output --connection-string "UseDevelopmentStorage=true"
az storage container create --name msg-archive --connection-string "UseDevelopmentStorage=true"
az storage container create --name msg-failed --connection-string "UseDevelopmentStorage=true"

# 7. Upload a test MSG file
az storage blob upload --container-name msg-input --file test.msg --name test.msg --connection-string "UseDevelopmentStorage=true"
```

**✅ Done!** Check `eml-output` container for converted file.

---

### **Option B: Azure Production Deployment**

#### **1. Create Azure Resources**

```bash
# Login to Azure
az login

# Create resource group
az group create --name msg-converter-rg --location eastus

# Create storage account
az storage account create \
  --name msgconverterstorage \
  --resource-group msg-converter-rg \
  --location eastus \
  --sku Standard_LRS

# Get connection string (save this!)
az storage account show-connection-string \
  --name msgconverterstorage \
  --resource-group msg-converter-rg \
  --query connectionString -o tsv

# Create containers
CONN_STRING="<paste-connection-string-here>"
az storage container create --name msg-input --connection-string "$CONN_STRING"
az storage container create --name eml-output --connection-string "$CONN_STRING"
az storage container create --name msg-archive --connection-string "$CONN_STRING"
az storage container create --name msg-failed --connection-string "$CONN_STRING"

# Create Function App
az functionapp create \
  --resource-group msg-converter-rg \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4 \
  --name msg-converter-func \
  --storage-account msgconverterstorage \
  --os-type Linux
```

#### **2. Configure Function App**

```bash
# Set application settings
az functionapp config appsettings set \
  --name msg-converter-func \
  --resource-group msg-converter-rg \
  --settings \
    "INPUT_CONTAINER=msg-input" \
    "OUTPUT_CONTAINER=eml-output" \
    "ARCHIVE_CONTAINER=msg-archive" \
    "FAILED_CONTAINER=msg-failed" \
    "MAX_FILE_SIZE_MB=25"
```

#### **3. Deploy**

```bash
func azure functionapp publish msg-converter-func
```

**✅ Done!** Upload MSG files to `msg-input` container in Azure Portal.

---

## 🔑 Where to Get Azure Keys

### **Method 1: Azure Portal (GUI)**
1. Go to https://portal.azure.com
2. Navigate to **Storage Accounts** → Your storage account
3. Click **Access keys** (left menu)
4. Copy **Connection string** from Key1

### **Method 2: Azure CLI**
```bash
az storage account show-connection-string \
  --name <your-storage-account-name> \
  --resource-group <your-resource-group> \
  --query connectionString -o tsv
```

---

## 📝 Configuration Files

### **local.settings.json** (Local Development)

**Current setup (uses emulator):**
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "INPUT_CONTAINER": "msg-input",
    "OUTPUT_CONTAINER": "eml-output",
    "ARCHIVE_CONTAINER": "msg-archive",
    "FAILED_CONTAINER": "msg-failed",
    "MAX_FILE_SIZE_MB": "25"
  }
}
```

**To use real Azure Storage locally:**
Replace `"UseDevelopmentStorage=true"` with your connection string:
```json
"AzureWebJobsStorage": "DefaultEndpointsProtocol=https;AccountName=msgconverterstorage;AccountKey=abc123...;EndpointSuffix=core.windows.net"
```

---

## 🧪 Testing

### **Upload Test File (Local):**
```bash
az storage blob upload \
  --container-name msg-input \
  --file test.msg \
  --name test.msg \
  --connection-string "UseDevelopmentStorage=true"
```

### **Upload Test File (Azure):**
```bash
az storage blob upload \
  --container-name msg-input \
  --file test.msg \
  --name test.msg \
  --account-name msgconverterstorage
```

### **Check Results:**
- Converted EML: `eml-output` container
- Archived MSG: `msg-archive` container  
- Failed files: `msg-failed` container

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| `AzureWebJobsStorage not set` | Start Azurite or add connection string to `local.settings.json` |
| `Module not found` | Run `pip install -r requirements.txt` |
| `func: command not found` | Install Azure Functions Core Tools |
| Function not triggering | Check container names match in config |
| Conversion fails | Check function logs for error details |

---

## 📚 Next Steps

- Read `SETUP_GUIDE.md` for detailed configuration
- Check `README.md` for project structure
- View logs in Azure Portal → Function App → Monitor
- Enable Application Insights for detailed telemetry
