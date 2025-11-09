# MSG to EML Converter - Azure Function

This Azure Function automatically converts Microsoft Outlook MSG files to standard EML format using blob storage triggers.

## 🚀 Quick Start

**Want to get started immediately?** See [QUICK_START.md](QUICK_START.md)

**Need help with Azure keys?** See [AZURE_KEYS_GUIDE.md](AZURE_KEYS_GUIDE.md)

**Want to understand the code?** See [COMPLETE_CODE_EXPLANATION.md](COMPLETE_CODE_EXPLANATION.md)

## 📚 Documentation

This project has comprehensive documentation:

- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Complete documentation index
- **[QUICK_START.md](QUICK_START.md)** - Get running in 5 minutes
- **[CONFIGURATION_SUMMARY.md](CONFIGURATION_SUMMARY.md)** - Configuration overview
- **[AZURE_KEYS_GUIDE.md](AZURE_KEYS_GUIDE.md)** - Azure keys and configuration
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup instructions
- **[COMPLETE_CODE_EXPLANATION.md](COMPLETE_CODE_EXPLANATION.md)** - Every line explained
- **[PROCESS_FLOW_VISUAL.md](PROCESS_FLOW_VISUAL.md)** - Visual process flow

## 🎯 What This Does

1. **Watches** Azure Blob Storage for new MSG files
2. **Validates** MSG file format
3. **Converts** MSG to EML format
4. **Uploads** EML to output container
5. **Archives** original MSG file
6. **Handles** errors gracefully

## 📁 Project Structure

```
.
├── 📚 Documentation
│   ├── README.md                          # This file
│   ├── DOCUMENTATION_INDEX.md             # Documentation index
│   ├── QUICK_START.md                     # Quick setup
│   ├── CONFIGURATION_SUMMARY.md           # Config guide
│   ├── AZURE_KEYS_GUIDE.md               # Azure keys
│   ├── SETUP_GUIDE.md                    # Complete setup
│   ├── COMPLETE_CODE_EXPLANATION.md      # Code walkthrough
│   └── PROCESS_FLOW_VISUAL.md            # Visual flow
│
├── 🐍 Source Code
│   ├── function_app.py                    # Main Azure Function
│   ├── services/
│   │   ├── msg_converter.py              # MSG to EML conversion
│   │   └── blob_storage.py               # Azure Storage operations
│   ├── utils/
│   │   └── logging.py                    # Logging service
│   └── models/
│       └── conversion_models.py          # Data models
│
└── ⚙️ Configuration
    ├── local.settings.json                # Local config (not in git)
    ├── local.settings.json.example        # Config template
    ├── host.json                          # Azure Functions config
    └── requirements.txt                   # Python dependencies
```

## ⚡ Quick Setup

### Local Development (No Azure Account Needed)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# 3. Install Azurite (Storage Emulator)
npm install -g azurite

# 4. Start Azurite
azurite --silent --location ./__azurite__

# 5. Start Function
func start
```

### Azure Deployment
See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete Azure deployment instructions.

## 🔑 Configuration

**No .env file needed!** This project uses `local.settings.json` for local development.

Key settings:
- `AzureWebJobsStorage`: Connection string (or `UseDevelopmentStorage=true` for local)
- `INPUT_CONTAINER`: msg-input
- `OUTPUT_CONTAINER`: eml-output
- `ARCHIVE_CONTAINER`: msg-archive
- `FAILED_CONTAINER`: msg-failed
- `MAX_FILE_SIZE_MB`: 25

See [CONFIGURATION_SUMMARY.md](CONFIGURATION_SUMMARY.md) for details.

## 📊 Process Flow

```
User uploads MSG → Azure Blob Storage (msg-input)
                        ↓
                Azure Function Triggered
                        ↓
                Validate MSG format
                        ↓
                Convert MSG → EML
                        ↓
                Upload EML (eml-output)
                        ↓
                Archive MSG (msg-archive)
```

See [PROCESS_FLOW_VISUAL.md](PROCESS_FLOW_VISUAL.md) for detailed visual flow.

## 🛠️ Requirements

- Python 3.9 or higher
- Azure Functions Core Tools v4
- Azurite (for local development)
- Azure Storage Account (for production)

## 📖 Learn More

- **New to the project?** Start with [QUICK_START.md](QUICK_START.md)
- **Need Azure help?** Read [AZURE_KEYS_GUIDE.md](AZURE_KEYS_GUIDE.md)
- **Want to understand code?** Read [COMPLETE_CODE_EXPLANATION.md](COMPLETE_CODE_EXPLANATION.md)
- **All documentation:** See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)

## ✅ Features

- ✅ Automatic blob trigger
- ✅ MSG format validation
- ✅ Timeout protection (30s)
- ✅ Error handling
- ✅ File archiving
- ✅ Structured logging
- ✅ Unique filename generation
- ✅ Failed file management

## 🚀 Deployment

```bash
func azure functionapp publish <YourFunctionAppName>
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete deployment instructions.
