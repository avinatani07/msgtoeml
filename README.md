# MSG to EML Converter - Azure Function

Azure Function that automatically converts Microsoft Outlook MSG files to standard EML format using blob storage triggers.

## 🎯 What It Does

Monitors Azure Blob Storage for new MSG files and automatically:
1. Validates MSG file format
2. Converts to EML format
3. Saves converted file to output container
4. Archives original MSG file
5. Handles errors gracefully with detailed logging

## 🎯 What This Does

1. **Watches** Azure Blob Storage for new MSG files
2. **Validates** MSG file format
3. **Converts** MSG to EML format
4. **Uploads** EML to output container
5. **Archives** original MSG file
6. **Handles** errors gracefully

## 📁 Project Structure

```
msg-to-eml-converter/
├── function_app.py              # Main Azure Function entry point
├── host.json                    # Azure Functions configuration
├── requirements.txt             # Python dependencies
├── local.settings.json.example  # Configuration template
│
├── services/
│   ├── msg_converter.py         # MSG to EML conversion logic
│   └── blob_storage.py          # Azure Blob Storage operations
│
├── utils/
│   └── logging.py               # Logging configuration
│
├── models/
│   └── conversion_models.py    # Data models
│
├── msg_to_eml_converter/
│   └── function.json            # Function binding configuration
│
└── setup_containers.py          # Setup script for blob containers
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Azure Functions Core Tools v4
- Azurite (for local development) or Azure Storage Account

### Local Development Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Azure Functions Core Tools:**
   ```bash
   npm install -g azure-functions-core-tools@4 --unsafe-perm true
   ```

3. **Install Azurite (local storage emulator):**
   ```bash
   npm install -g azurite
   ```

4. **Configure settings:**
   ```bash
   copy local.settings.json.example local.settings.json
   ```

5. **Create blob containers:**
   ```bash
   python setup_containers.py
   ```

6. **Start Azurite (Terminal 1):**
   ```bash
   azurite --silent --location ./__azurite__ --blobPort 10001 --queuePort 10002 --tablePort 10003
   ```

7. **Start Azure Function (Terminal 2):**
   ```bash
   func start --port 7072
   ```

8. **Test the converter:**
   ```bash
   python test_upload.py your_email.msg
   ```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) and [HOW_TO_TEST.md](HOW_TO_TEST.md) for detailed instructions.

## ⚙️ Configuration

Configuration is managed through `local.settings.json` (not committed to git).

**Key Settings:**
```json
{
  "AzureWebJobsStorage": "Connection string or UseDevelopmentStorage=true",
  "INPUT_CONTAINER": "msg-input",
  "OUTPUT_CONTAINER": "eml-output",
  "ARCHIVE_CONTAINER": "msg-archive",
  "FAILED_CONTAINER": "msg-failed",
  "MAX_FILE_SIZE_MB": "25"
}
```

**For local development:** Use `local.settings.json.example` as a template.

**For Azure deployment:** Configure application settings in Azure Portal.

## 📊 How It Works

```
1. MSG file uploaded to msg-input container
   ↓
2. Azure Function automatically triggered
   ↓
3. Validate MSG file format and size
   ↓
4. Extract email data (headers, body, metadata)
   ↓
5. Generate EML format
   ↓
6. Upload EML to eml-output container
   ↓
7. Archive original MSG to msg-archive container
   ↓
8. Log success (or move to msg-failed on error)
```

## ✨ Features

- Automatic blob storage trigger
- MSG format validation
- Timeout protection (30 seconds)
- Comprehensive error handling
- Automatic file archiving
- Failed file management
- Detailed structured logging
- Unique filename generation with timestamps

## 🧪 Testing

1. **Get a real MSG file** from Microsoft Outlook:
   - Open any email in Outlook
   - File → Save As → Outlook Message Format (.msg)

2. **Upload and test:**
   ```bash
   python test_upload.py your_email.msg
   ```

3. **Check results:**
   - Converted EML in `eml-output` container
   - Original MSG in `msg-archive` container
   - Function logs show conversion details

See [HOW_TO_TEST.md](HOW_TO_TEST.md) for detailed testing instructions.

## 🚀 Azure Deployment

1. **Create Azure resources:**
   - Azure Function App (Python 3.9+)
   - Azure Storage Account

2. **Configure application settings** in Azure Portal with the same keys from `local.settings.json`

3. **Deploy:**
   ```bash
   func azure functionapp publish <YourFunctionAppName>
   ```

4. **Create containers** in your Azure Storage Account:
   - msg-input
   - eml-output
   - msg-archive
   - msg-failed

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete deployment guide.

## 📚 Documentation

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Complete setup instructions
- [HOW_TO_TEST.md](HOW_TO_TEST.md) - Testing guide
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Detailed testing scenarios
- [AZURE_KEYS_GUIDE.md](AZURE_KEYS_GUIDE.md) - Azure configuration help
- [QUICK_START.md](QUICK_START.md) - Quick start guide

## 🛠️ Tech Stack

- **Runtime:** Python 3.9+
- **Framework:** Azure Functions v4
- **Storage:** Azure Blob Storage
- **Libraries:** 
  - `extract-msg` - MSG file parsing
  - `azure-functions` - Function runtime
  - `azure-storage-blob` - Blob operations

## 📝 License

This project is open source and available for use and modification.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
