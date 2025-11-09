# Testing Guide - MSG to EML Converter

## 🧪 How to Test the Converter

### **Prerequisites**
Make sure these are running:
1. ✅ Azurite (storage emulator)
2. ✅ Azure Function (func start)

---

## 📋 Step-by-Step Testing

### **Step 1: Check Running Processes**

You should have these running:
```
Process 1: Azurite
  Command: azurite --silent --location ./__azurite__ --blobPort 10001 --queuePort 10002 --tablePort 10003
  Status: Should show "successfully listening"

Process 2: Azure Function
  Command: func start --port 7072
  Status: Should show function loaded
```

### **Step 2: Create a Test MSG File**

**Option A: Create a minimal test MSG file**
```bash
python create_test_msg.py
```
This creates `test_email.msg` - a minimal valid MSG file.

**Option B: Use a real MSG file**
- Save an email from Outlook as .msg format
- Place it in your project folder

### **Step 3: Upload and Test**

```bash
python test_upload.py test_email.msg
```

Or with a real MSG file:
```bash
python test_upload.py "C:\path\to\your\email.msg"
```

### **Step 4: Watch the Results**

The script will:
1. ✅ Upload the MSG file to `msg-input` container
2. ⏳ Wait for the Azure Function to process it
3. ✅ Check if EML file appears in `eml-output` container
4. 📊 Show conversion results
5. 📁 List all container contents

---

## 📊 Expected Output

### **Successful Conversion:**
```
🧪 MSG to EML Converter - Test Script
============================================================

📤 Uploading MSG file...
✅ Uploaded: test_email.msg
   Size: 1024 bytes
   Waiting for conversion...
   Waiting... (1/15s)
   Waiting... (2/15s)

✅ CONVERSION SUCCESSFUL!
   Output file: test_email.eml
   Size: 512 bytes
   Created: 2024-11-08 14:30:22

📧 EML Preview:
============================================================
From: test@example.com
To: recipient@example.com
Subject: Test Email
Date: Thu, 07 Nov 2024 10:30:00 +0000
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
...
============================================================

📁 Container Status:
============================================================

msg-input/ (0 files)

eml-output/ (1 files)
  - test_email.eml (512 bytes)

msg-archive/ (1 files)
  - test_email_20241108_143022.msg (1024 bytes)

msg-failed/ (0 files)
============================================================
```

### **Failed Conversion:**
```
⚠️ CONVERSION FAILED!
   File moved to: msg-failed/
   - test_email_failed_20241108_143022.msg
```

---

## 🔍 Manual Testing (Alternative)

### **Method 1: Using Python Script**
```python
from azure.storage.blob import BlobServiceClient

connection_string = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10001/devstoreaccount1;"

# Upload file
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client("msg-input")

with open("test.msg", "rb") as f:
    container_client.upload_blob("test.msg", f, overwrite=True)

print("File uploaded! Check eml-output container in a few seconds.")
```

### **Method 2: Using Azure Storage Explorer**
1. Download Azure Storage Explorer
2. Connect to local emulator
3. Navigate to `msg-input` container
4. Upload your MSG file
5. Wait a few seconds
6. Check `eml-output` container for converted file

---

## 🛠️ Troubleshooting

### **Problem: "Azurite not running"**
**Solution:**
```bash
azurite --silent --location ./__azurite__ --blobPort 10001 --queuePort 10002 --tablePort 10003
```

### **Problem: "Function not running"**
**Solution:**
```bash
func start --port 7072
```

### **Problem: "File not converting"**
**Check:**
1. Is Azurite running? (Check process output)
2. Is Function running? (Check process output)
3. Is the file a valid MSG? (Check file signature)
4. Check function logs for errors

### **Problem: "Connection refused"**
**Solution:**
Make sure `local.settings.json` has the correct connection string with custom ports:
```json
"AzureWebJobsStorage": "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10001/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10002/devstoreaccount1;TableEndpoint=http://127.0.0.1:10003/devstoreaccount1;"
```

### **Problem: "Module not found"**
**Solution:**
```bash
pip install -r requirements.txt
```

---

## 📝 Test Checklist

- [ ] Azurite is running
- [ ] Azure Function is running
- [ ] Containers are created (msg-input, eml-output, msg-archive, msg-failed)
- [ ] Test MSG file is ready
- [ ] Upload script works
- [ ] File appears in msg-input
- [ ] Function processes the file
- [ ] EML appears in eml-output
- [ ] Original MSG moves to msg-archive
- [ ] No errors in function logs

---

## 🎯 Quick Test Commands

```bash
# 1. Start Azurite (Terminal 1)
azurite --silent --location ./__azurite__ --blobPort 10001 --queuePort 10002 --tablePort 10003

# 2. Start Function (Terminal 2)
func start --port 7072

# 3. Create test file (Terminal 3)
python create_test_msg.py

# 4. Upload and test
python test_upload.py test_email.msg

# 5. Check results
# Output will show conversion status and container contents
```

---

## 📊 Monitoring

### **Watch Function Logs**
The function logs will show:
- When file is detected
- Validation results
- Conversion progress
- Success/failure status
- Error details (if any)

### **Check Containers**
```python
python test_upload.py test_email.msg
```
This will show all container contents at the end.

---

## 🚀 Testing with Real MSG Files

1. **Save an email from Outlook:**
   - Open email in Outlook
   - File → Save As
   - Save as type: Outlook Message Format (*.msg)

2. **Upload the real MSG file:**
   ```bash
   python test_upload.py "C:\path\to\real_email.msg"
   ```

3. **Check the converted EML:**
   - Should contain all headers (From, To, Subject, Date)
   - Should contain email body
   - Should preserve HTML formatting (if present)

---

## ✅ Success Criteria

A successful test should show:
1. ✅ File uploaded to msg-input
2. ✅ Function triggered automatically
3. ✅ Validation passed
4. ✅ Conversion completed
5. ✅ EML file in eml-output
6. ✅ Original MSG in msg-archive
7. ✅ No files in msg-failed
8. ✅ Logs show success

---

## 📞 Need Help?

If tests fail:
1. Check function logs for error messages
2. Verify Azurite is running
3. Verify function is running
4. Check file is valid MSG format
5. Review error messages in test output

Happy testing! 🎉
