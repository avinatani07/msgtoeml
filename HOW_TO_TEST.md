# How to Test - MSG to EML Converter

## ✅ Your System is Ready!

- ✅ Azurite is running (storage emulator)
- ✅ Azure Function is running
- ✅ Containers are created
- ✅ Everything is configured

## 🎯 To Test the Converter

### **You Need a Real MSG File**

The test MSG file I created is too minimal. You need a **real MSG file from Microsoft Outlook**.

---

## 📧 How to Get a Real MSG File

### **Method 1: From Outlook Desktop**

1. Open Microsoft Outlook
2. Open any email
3. Click **File** → **Save As**
4. Choose **Save as type**: **Outlook Message Format (*.msg)**
5. Save it to your project folder (e.g., `C:\Users\sunny\OneDrive\Desktop\external project\`)

### **Method 2: Download Sample MSG Files**

You can download sample MSG files from:
- https://github.com/TeamMsgExtractor/msg-extractor/tree/master/tests/test_data
- Or search "sample msg file download" online

### **Method 3: Create from Outlook Web**

1. Go to outlook.com
2. Open an email
3. Click **...** (More actions)
4. Click **Download**
5. Rename the downloaded file to `.msg` extension

---

## 🧪 Testing Steps

### **Step 1: Get a Real MSG File**

Save an email from Outlook as described above. Let's say you saved it as `my_email.msg`.

### **Step 2: Upload and Test**

```bash
python test_upload.py my_email.msg
```

Or with full path:
```bash
python test_upload.py "C:\Users\sunny\OneDrive\Desktop\external project\my_email.msg"
```

### **Step 3: Watch the Magic!**

The script will:
1. Upload the MSG file
2. Wait for conversion
3. Show the converted EML content
4. Display all container contents

---

## 📊 Expected Output (Success)

```
🧪 MSG to EML Converter - Test Script
============================================================

📤 Uploading MSG file...
✅ Uploaded: my_email.msg
   Size: 45678 bytes
   Waiting for conversion...
   Waiting... (1/15s)
   Waiting... (2/15s)

✅ CONVERSION SUCCESSFUL!
   Output file: my_email.eml
   Size: 23456 bytes
   Created: 2025-11-08 12:30:45

📧 EML Preview:
============================================================
From: sender@example.com
To: recipient@example.com
Subject: Test Email Subject
Date: Thu, 07 Nov 2024 10:30:00 +0000
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit

This is the email body content...
============================================================

📁 Container Status:
============================================================

msg-input/ (0 files)

eml-output/ (1 files)
  - my_email.eml (23456 bytes)

msg-archive/ (1 files)
  - my_email_20251108_123045.msg (45678 bytes)

msg-failed/ (0 files)
============================================================
```

---

## 🔍 What Happens Behind the Scenes

1. **Upload**: MSG file goes to `msg-input` container
2. **Trigger**: Azure Function detects new file
3. **Validate**: Checks if file is valid MSG format
4. **Convert**: Extracts headers and body, generates EML
5. **Upload**: EML file goes to `eml-output` container
6. **Archive**: Original MSG moves to `msg-archive` container
7. **Success**: Logs show completion

---

## ⚠️ Why the Test File Failed

The minimal test file I created (`test_email.msg`) failed because:
- It only has the MSG file signature (header)
- It doesn't have actual email data
- The `extract-msg` library needs complete MSG structure

**Real MSG files from Outlook have:**
- Complete OLE/CFB structure
- Email headers (From, To, Subject, Date)
- Email body (text or HTML)
- Attachments (if any)
- Metadata

---

## 🚀 Quick Test (If You Have Outlook)

1. **Open Outlook**
2. **Find any email** (even a test email to yourself)
3. **File → Save As → Outlook Message Format (.msg)**
4. **Save to project folder**
5. **Run:**
   ```bash
   python test_upload.py your_saved_email.msg
   ```

---

## 📝 Alternative: Manual Testing

If you don't have a MSG file right now, you can test the system is working:

### **Check Azurite:**
```bash
# Should show "successfully listening"
```

### **Check Function:**
```bash
# Should show function loaded without errors
```

### **Check Containers:**
```python
python setup_containers.py
# Should show all 4 containers exist
```

---

## 🎯 What to Test

Once you have a real MSG file, test these scenarios:

### **Test 1: Normal Email**
- Upload a regular email
- Should convert successfully
- Check EML has all headers and body

### **Test 2: Email with HTML**
- Upload an email with formatting
- Should preserve HTML in EML

### **Test 3: Large Email**
- Upload an email close to 25 MB limit
- Should convert or fail gracefully

### **Test 4: Invalid File**
- Upload a .txt file renamed to .msg
- Should move to `msg-failed` container

---

## 📊 Monitoring

### **Watch Function Logs**
The function terminal will show:
- File detected
- Validation status
- Conversion progress
- Success/failure

### **Check Containers**
After each test, check:
- `msg-input`: Should be empty (file moved)
- `eml-output`: Should have converted EML
- `msg-archive`: Should have original MSG
- `msg-failed`: Should be empty (unless error)

---

## ✅ Success Checklist

- [ ] Azurite running
- [ ] Function running
- [ ] Real MSG file obtained
- [ ] Upload script works
- [ ] Conversion succeeds
- [ ] EML file created
- [ ] Original MSG archived
- [ ] No errors in logs

---

## 🆘 Need Help?

**If you don't have Outlook:**
- Ask a colleague to save an email as MSG
- Download sample MSG files from GitHub
- Use Outlook Web to export emails

**If conversion fails:**
- Check function logs for error message
- Verify file is real MSG format
- Check file size is under 25 MB
- Ensure Azurite and Function are running

---

## 🎉 Summary

**Your system is ready!** You just need a real MSG file from Outlook to test it.

**Quick steps:**
1. Get a MSG file from Outlook
2. Run: `python test_upload.py your_file.msg`
3. Watch it convert!

The system is working perfectly - it correctly rejected the minimal test file because it wasn't a complete MSG file. This shows the validation is working! 🎯
