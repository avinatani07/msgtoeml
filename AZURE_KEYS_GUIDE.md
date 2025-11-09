# 🔑 Azure Keys Configuration - Visual Guide

## Where to Put Azure Keys

### **NO .env file needed!** This project uses:
- `local.settings.json` for **local development**
- Azure Portal **Application Settings** for **production**

---

## 📍 Local Development

### **File Location:** `local.settings.json` (in project root)

```
your-project/
├── function_app.py
├── local.settings.json  ← PUT YOUR KEYS HERE
├── requirements.txt
└── ...
```

### **What to Put:**

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "YOUR_CONNECTION_STRING_HERE",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "INPUT_CONTAINER": "msg-input",
    "OUTPUT_CONTAINER": "eml-output",
    "ARCHIVE_CONTAINER": "msg-archive",
    "FAILED_CONTAINER": "msg-failed",
    "MAX_FILE_SIZE_MB": "25"
  }
}
```

### **Where to Get Connection String:**

#### **Option 1: Azure Portal (Visual)**
```
1. Open https://portal.azure.com
2. Click "Storage accounts" (left menu)
3. Click your storage account name
4. Click "Access keys" (under Security + networking)
5. Click "Show" next to Key1
6. Click "Copy" button next to "Connection string"
7. Paste into local.settings.json
```

#### **Option 2: Azure CLI (Command)**
```bash
az storage account show-connection-string \
  --name YOUR_STORAGE_ACCOUNT_NAME \
  --resource-group YOUR_RESOURCE_GROUP \
  --query connectionString -o tsv
```

### **Connection String Format:**
```
DefaultEndpointsProtocol=https;
AccountName=msgconverterstorage;
AccountKey=abc123xyz789...==;
EndpointSuffix=core.windows.net
```

---

## ☁️ Azure Production

### **Location:** Azure Portal → Function App → Configuration

```
Azure Portal
└── Function Apps
    └── Your Function App (e.g., msg-converter-func)
        └── Settings
            └── Configuration
                └── Application settings  ← PUT YOUR KEYS HERE
```

### **What to Add:**

| Setting Name | Value | Where to Get |
|--------------|-------|--------------|
| `AzureWebJobsStorage` | Connection string | Storage Account → Access keys |
| `INPUT_CONTAINER` | `msg-input` | Your choice |
| `OUTPUT_CONTAINER` | `eml-output` | Your choice |
| `ARCHIVE_CONTAINER` | `msg-archive` | Your choice |
| `FAILED_CONTAINER` | `msg-failed` | Your choice |
| `MAX_FILE_SIZE_MB` | `25` | Your choice |

### **How to Add (Portal):**
```
1. Go to Function App → Configuration
2. Click "+ New application setting"
3. Enter Name: AzureWebJobsStorage
4. Enter Value: <paste your connection string>
5. Click "OK"
6. Repeat for other settings
7. Click "Save" at the top
```

### **How to Add (CLI):**
```bash
az functionapp config appsettings set \
  --name YOUR_FUNCTION_APP_NAME \
  --resource-group YOUR_RESOURCE_GROUP \
  --settings \
    "AzureWebJobsStorage=YOUR_CONNECTION_STRING" \
    "INPUT_CONTAINER=msg-input" \
    "OUTPUT_CONTAINER=eml-output" \
    "ARCHIVE_CONTAINER=msg-archive" \
    "FAILED_CONTAINER=msg-failed" \
    "MAX_FILE_SIZE_MB=25"
```

---

## 🎯 Quick Decision Tree

```
Do you have an Azure account?
│
├─ NO → Use local emulator (Azurite)
│        Set: "AzureWebJobsStorage": "UseDevelopmentStorage=true"
│        No Azure keys needed!
│
└─ YES → Want to test locally or deploy?
         │
         ├─ Test Locally → Put connection string in local.settings.json
         │                  Get from: Azure Portal → Storage Account → Access keys
         │
         └─ Deploy to Azure → Put connection string in Azure Portal
                               Location: Function App → Configuration → Application settings
```

---

## 🔒 Security Checklist

✅ **local.settings.json is in .gitignore** (already done)  
✅ **Never commit real connection strings to Git**  
✅ **Use different storage accounts for dev/prod**  
✅ **Rotate keys periodically in Azure Portal**  
✅ **Use Azure Key Vault for production secrets** (advanced)

---

## 📋 Complete Setup Example

### **Scenario: First Time Setup with Azure**

**Step 1: Create Storage Account**
```bash
az storage account create \
  --name msgconverter123 \
  --resource-group my-rg \
  --location eastus \
  --sku Standard_LRS
```

**Step 2: Get Connection String**
```bash
az storage account show-connection-string \
  --name msgconverter123 \
  --resource-group my-rg \
  --query connectionString -o tsv
```

**Output:**
```
DefaultEndpointsProtocol=https;AccountName=msgconverter123;AccountKey=abc123...;EndpointSuffix=core.windows.net
```

**Step 3: Update local.settings.json**
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "DefaultEndpointsProtocol=https;AccountName=msgconverter123;AccountKey=abc123...;EndpointSuffix=core.windows.net",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "INPUT_CONTAINER": "msg-input",
    "OUTPUT_CONTAINER": "eml-output",
    "ARCHIVE_CONTAINER": "msg-archive",
    "FAILED_CONTAINER": "msg-failed",
    "MAX_FILE_SIZE_MB": "25"
  }
}
```

**Step 4: Create Containers**
```bash
CONN="DefaultEndpointsProtocol=https;AccountName=msgconverter123;AccountKey=abc123...;EndpointSuffix=core.windows.net"

az storage container create --name msg-input --connection-string "$CONN"
az storage container create --name eml-output --connection-string "$CONN"
az storage container create --name msg-archive --connection-string "$CONN"
az storage container create --name msg-failed --connection-string "$CONN"
```

**Step 5: Test Locally**
```bash
func start
```

**✅ Done!** Your function is now connected to Azure Storage.

---

## ❓ Common Questions

**Q: Do I need to create a .env file?**  
A: **NO.** Use `local.settings.json` instead.

**Q: Where do I put my Azure connection string?**  
A: In `local.settings.json` (local) or Azure Portal → Function App → Configuration (production).

**Q: Is it safe to commit local.settings.json?**  
A: **NO.** It's already in `.gitignore`. Never commit it with real keys.

**Q: Can I test without Azure?**  
A: **YES.** Use `"AzureWebJobsStorage": "UseDevelopmentStorage=true"` and run Azurite.

**Q: What if I don't have Azure CLI?**  
A: Use Azure Portal (web interface) to get connection strings and configure settings.

**Q: How do I know if my keys are working?**  
A: Run `func start` - if it connects without errors, your keys are correct.

---

## 🆘 Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "AzureWebJobsStorage not set" | Missing connection string | Add to `local.settings.json` or start Azurite |
| "Invalid connection string" | Wrong format | Copy full string from Azure Portal |
| "Container not found" | Containers don't exist | Create containers in storage account |
| "Authentication failed" | Wrong key or expired | Regenerate key in Azure Portal |
| Function not triggering | Wrong container name | Check container names match config |

---

## 📞 Need Help?

1. Check `QUICK_START.md` for step-by-step commands
2. Check `SETUP_GUIDE.md` for detailed explanations
3. Check Azure Portal → Storage Account → Access keys for connection string
4. Run `func start` and check terminal output for errors
