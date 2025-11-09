# MSG to EML Converter - Azure Function

Azure Function that automatically converts Microsoft Outlook MSG files to standard EML format using blob storage triggers.

## 🎯 What It Does

Monitors Azure Blob Storage for new MSG files and automatically:
1. Validates MSG file format
2. Converts to EML format
3. Saves converted file to output container
4. Archives original MSG file
5. Handles errors gracefully with detailed logging



## 📁 Project Structure

```
msg-to-eml-converter/
├── function_app.py                # Main Azure Function entry point
├── host.json                      # Azure Functions configuration
├── requirements.txt               # Python dependencies
├── local.settings.json.example    # Configuration template
│
├── services/
│   ├── msg_converter.py           # MSG to EML conversion logic
│   └── blob_storage.py            # Azure Blob Storage operations
│
├── utils/
│   └── logging.py                 # Logging configuration
│
├── models/
│   └── conversion_models.py      # Data models
│
├── msg_to_eml_converter/
│   └── function.json              # Function binding configuration
│
├── setup_containers.py            # Setup script for blob containers
├── test_conversion_only.py        # Test conversion without Azure Function
└── test_upload.py                 # Test full workflow with blob storage
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

### Option 1: Test Conversion Only (No Azure Function needed)

Test just the MSG to EML conversion logic:

```bash
python test_conversion_only.py your_email.msg
```

**What it does:**
- Reads your MSG file
- Converts to EML format
- Shows preview of converted content
- Saves EML file locally
- No Azurite or Azure Function required

**Perfect for:** Quick testing, debugging conversion issues, or when you just want to convert a file.

### Option 2: Full End-to-End Test (With Azure Function)

Test the complete workflow with blob storage:

1. **Start Azurite and Azure Function** (see Quick Start above)

2. **Run the test:**
   ```bash
   python test_upload.py your_email.msg
   ```

**What it does:**
- Uploads MSG to blob storage
- Triggers Azure Function automatically
- Waits for conversion
- Shows results from all containers
- Tests the complete production workflow

**Perfect for:** Testing the full system, verifying blob triggers, checking error handling.

### Getting a Test MSG File

**From Microsoft Outlook:**
1. Open any email in Outlook
2. File → Save As → Outlook Message Format (.msg)
3. Save to your project folder

**Note:** You need a real MSG file from Outlook. Programmatically created files won't work with the `extract-msg` library.

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
