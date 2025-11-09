# Azure Keys & Configuration Setup Guide

## Overview
This project uses **local.settings.json** (NOT .env) for local development and **Azure Application Settings** for production. The `.gitignore` already protects your secrets.

---

## 🔑 Where to Get Azure Keys

### **Storage Account Connection String**

1. Go to **Azure Portal** → **Storage Accounts**
2. Select your storage account (or create one)
3. Go to **Security + networking** → **Access keys**
4. Copy **Connection string** from Key1 or Key2

**Format looks like:**
```
DefaultEndpointsProtocol=https;AccountName=youraccount;AccountKey=abc123...==;EndpointSuffix=core.windows.net
```

---

## 📝 Local Development Configuration

### **File: `local.settings.json`** (Already exists in your project)

**For Local Testing with Emulator (Current Setup):**
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

**For Local Testing with Real Azure Storage:**
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "DefaultEndpointsProtocol=https;AccountName=YOUR_ACCOUNT;AccountKey=YOUR_KEY;EndpointSuffix=core.windows.net",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "INPUT_CONTAINER": "msg-input",
    "OUTPUT_CONTAINER": "eml-output",
    "ARCHIVE_CONTAINER": "msg-archive",
    "FAILED_CONTAINER": "msg-failed",
    "MAX_FILE_SIZE_MB": "25"
  }
}
```

**⚠️ IMPORTANT:** 
- `local.settings.json` is already in `.gitignore` - it won't be committed
- Never commit real Azure keys to Git
- This file is ONLY for local development

---

## ☁️ Azure Production Configuration

### **Option 1: Using Azure Portal (Recommended)**

1. Go to **Azure Portal** → **Function App** → Your function app
2. Go to **Settings** → **Configuration**
3. Click **+ New application setting** for each:

| Name | Value | Example |
|------|-------|---------|
| `AzureWebJobsStorage` | Your storage connection string | `DefaultEndpointsProtocol=https;AccountName=...` |
| `FUNCTIONS_WORKER_RUNTIME` | `python` | `python` |
| `INPUT_CONTAINER` | `msg-input` | `msg-input` |
| `OUTPUT_CONTAINER` | `eml-output` | `eml-output` |
| `ARCHIVE_CONTAINER` | `msg-archive` | `msg-archive` |
| `FAILED_CONTAINER` | `msg-failed` | `msg-failed` |
| `MAX_FILE_SIZE_MB` | `25` | `25` |

4. Click **Save**

### **Option 2: Using Azure CLI**

```bash
# Set storage connection string
az functionapp config appsettings set --name <YourFunctionAppName> \
  --resource-group <YourResourceGroup> \
  --settings "AzureWebJobsStorage=<YourConnectionString>"

# Set other settings
az functionapp config appsettings set --name <YourFunctionAppName> \
  --resource-group <YourResourceGroup> \
  --settings "INPUT_CONTAINER=msg-input" \
             "OUTPUT_CONTAINER=eml-output" \
             "ARCHIVE_CONTAINER=msg-archive" \
             "FAILED_CONTAINER=msg-failed" \
             "MAX_FILE_SIZE_MB=25"
```

---

## 🚀 Step-by-Step Setup Process

### **Step 1: Local Development (Using Emulator)**

1. **Keep current `local.settings.json`** (already configured)
2. **Install Azurite:**
   ```bash
   npm install -g azurite
   ```
3. **Start Azurite:**
   ```bash
   azurite --silent --location ./__azurite__
   ```
4. **Run function:**
   ```bash
   func start
   ```
5. **Create containers** (using Azure Storage Explorer or CLI):
   ```bash
   az storage container create --name msg-input --connection-string "UseDevelopmentStorage=true"
   az storage container create --name eml-output --connection-string "UseDevelopmentStorage=true"
   az storage container create --name msg-archive --connection-string "UseDevelopmentStorage=true"
   az storage container create --name msg-failed --connection-string "UseDevelopmentStorage=true"
   ```

### **Step 2: Test with Real Azure Storage (Optional)**

1. **Create Storage Account in Azure Portal**
2. **Get connection string** (Access keys section)
3. **Update `local.settings.json`:**
   - Replace `"UseDevelopmentStorage=true"` with your connection string
4. **Create containers in Azure Storage:**
   ```bash
   az storage container create --name msg-input --connection-string "<YourConnectionString>"
   az storage container create --name eml-output --connection-string "<YourConnectionString>"
   az storage container create --name msg-archive --connection-string "<YourConnectionString>"
   az storage container create --name msg-failed --connection-string "<YourConnectionString>"
   ```

### **Step 3: Deploy to Azure**

1. **Create Function App in Azure Portal:**
   - Runtime: Python 3.9+
   - OS: Linux
   - Plan: Consumption or Premium

2. **Configure Application Settings** (see Azure Production Configuration above)

3. **Deploy:**
   ```bash
   func azure functionapp publish <YourFunctionAppName>
   ```

---

## 🔒 Security Best Practices

✅ **DO:**
- Use `local.settings.json` for local development (already in `.gitignore`)
- Use Azure Application Settings for production
- Use Azure Key Vault for sensitive production keys (advanced)
- Rotate storage keys periodically

❌ **DON'T:**
- Commit `local.settings.json` with real keys
- Use `.env` files (this project uses `local.settings.json`)
- Share connection strings in chat/email
- Hardcode keys in Python files

---

## 🧪 Quick Test Commands

### **Test Local Function:**
```bash
# Terminal 1: Start Azurite
azurite --silent --location ./__azurite__

# Terminal 2: Start Function
func start
```

### **Upload Test File:**
```bash
# Using Azure CLI
az storage blob upload --container-name msg-input \
  --file test.msg --name test.msg \
  --connection-string "UseDevelopmentStorage=true"
```

### **Check Results:**
- Converted file: `eml-output` container
- Original archived: `msg-archive` container
- Failed conversions: `msg-failed` container

---

## 📊 Monitoring & Logs

### **Local:**
- Watch terminal output from `func start`
- Check `__azurite__` folder for storage logs

### **Azure:**
- Function App → Functions → msg_to_eml_converter → Monitor
- Application Insights (if enabled)
- Storage Account → Monitoring → Insights

---

## ❓ FAQ

**Q: Do I need a .env file?**  
A: No. Use `local.settings.json` for local and Azure Application Settings for production.

**Q: Where do I put my Azure connection string?**  
A: In `local.settings.json` for local testing, or Azure Portal → Function App → Configuration for production.

**Q: Is my connection string safe?**  
A: Yes, if you follow the setup. `local.settings.json` is in `.gitignore` and won't be committed.

**Q: Can I test without Azure?**  
A: Yes! Use Azurite emulator with `"UseDevelopmentStorage=true"` (current setup).

**Q: How do I get my storage connection string?**  
A: Azure Portal → Storage Account → Access keys → Copy connection string.
