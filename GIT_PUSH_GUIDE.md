# Git Push Guide - MSG to EML Converter

## 📦 Files to Push (Essential for Development)

### **Core Application Files** ✅
```
function_app.py                    # Main Azure Function
host.json                          # Azure Function configuration
requirements.txt                   # Python dependencies
local.settings.json.example        # Configuration template (NO SECRETS)
```

### **Service Layer** ✅
```
services/
  ├── __init__.py
  ├── blob_storage.py              # Blob storage operations
  └── msg_converter.py             # MSG to EML conversion logic
```

### **Utilities** ✅
```
utils/
  ├── __init__.py
  └── logging.py                   # Logging configuration
```

### **Models** ✅
```
models/
  ├── __init__.py
  └── conversion_models.py         # Data models
```

### **Function Configuration** ✅
```
msg_to_eml_converter/
  └── function.json                # Function binding configuration
```

### **Setup Scripts** ✅
```
setup_containers.py                # Creates blob containers
test_upload.py                     # Testing script
```

### **Documentation** ✅
```
README.md                          # Main documentation
SETUP_GUIDE.md                     # Setup instructions
HOW_TO_TEST.md                     # Testing guide
TESTING_GUIDE.md                   # Detailed testing
QUICK_START.md                     # Quick start guide
AZURE_KEYS_GUIDE.md                # Azure configuration help
```

---

## 🚫 Files NOT to Push (Excluded by .gitignore)

### **Local Development**
- `__azurite__/` - Local storage emulator data
- `__pycache__/` - Python cache
- `.venv/`, `venv/` - Virtual environments
- `.kiro/` - IDE specific files

### **Secrets & Config**
- `local.settings.json` - Contains connection strings (NEVER PUSH!)

### **Test Files**
- `*.msg` files - Test email files
- `*.eml` files - Converted output files
- `test_*.py` - Temporary test scripts
- `create_*.py` - File creation scripts

### **Extra Documentation**
- `COPILOT_MASTER_PROMPT.txt`
- `COMPLETE_CODE_EXPLANATION.md`
- `TESTING_SUMMARY.md`
- And other verbose docs

---

## 🚀 How to Push to Git

### **Step 1: Initialize Git (if not done)**
```bash
git init
```

### **Step 2: Check What Will Be Pushed**
```bash
git status
```

This shows files that will be committed. Make sure:
- ✅ No `local.settings.json` (only `.example` version)
- ✅ No `__azurite__/` folder
- ✅ No `.msg` or `.eml` files
- ✅ No `__pycache__/` folders

### **Step 3: Add Files**
```bash
git add .
```

### **Step 4: Commit**
```bash
git commit -m "Initial commit: MSG to EML converter"
```

### **Step 5: Add Remote Repository**
```bash
git remote add origin https://github.com/yourusername/your-repo.git
```

### **Step 6: Push**
```bash
git push -u origin main
```

Or if your default branch is `master`:
```bash
git push -u origin master
```

---

## ✅ Pre-Push Checklist

Before pushing, verify:

- [ ] `.gitignore` is configured correctly
- [ ] `local.settings.json` is NOT in git (check with `git status`)
- [ ] `local.settings.json.example` IS included (template without secrets)
- [ ] No `__azurite__/` folder
- [ ] No test `.msg` or `.eml` files
- [ ] No `__pycache__/` folders
- [ ] `requirements.txt` is up to date
- [ ] `README.md` has clear setup instructions

---

## 📋 Essential File Structure for Git

```
your-repo/
├── .gitignore                     ✅ Push
├── function_app.py                ✅ Push
├── host.json                      ✅ Push
├── requirements.txt               ✅ Push
├── local.settings.json.example    ✅ Push
├── setup_containers.py            ✅ Push
├── test_upload.py                 ✅ Push
├── README.md                      ✅ Push
├── SETUP_GUIDE.md                 ✅ Push
├── HOW_TO_TEST.md                 ✅ Push
├── services/
│   ├── __init__.py                ✅ Push
│   ├── blob_storage.py            ✅ Push
│   └── msg_converter.py           ✅ Push
├── utils/
│   ├── __init__.py                ✅ Push
│   └── logging.py                 ✅ Push
├── models/
│   ├── __init__.py                ✅ Push
│   └── conversion_models.py      ✅ Push
└── msg_to_eml_converter/
    └── function.json              ✅ Push
```

---

## 🔒 Security Notes

**NEVER push:**
- `local.settings.json` - Contains connection strings
- Azure credentials or keys
- Storage account keys
- Any file with secrets

**ALWAYS push:**
- `local.settings.json.example` - Template with placeholder values

---

## 🎯 Quick Commands

```bash
# Check what will be committed
git status

# See what's ignored
git status --ignored

# Check if local.settings.json is tracked (should be NO)
git ls-files | grep local.settings.json

# If local.settings.json is tracked, remove it
git rm --cached local.settings.json
git commit -m "Remove local.settings.json from tracking"
```

---

## 📝 Recommended Commit Message

```bash
git commit -m "Initial commit: Azure Function MSG to EML converter

- Blob-triggered Azure Function
- Converts Outlook MSG files to EML format
- Includes error handling and file archiving
- Local development setup with Azurite
- Comprehensive testing scripts and documentation"
```

---

## 🌿 Branch Strategy (Optional)

For team development:

```bash
# Create development branch
git checkout -b develop

# Create feature branches
git checkout -b feature/add-html-support
git checkout -b feature/add-attachments

# Merge back to main when ready
git checkout main
git merge develop
```

---

## 👥 For Team Members

After cloning the repo, they need to:

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Copy config template:**
   ```bash
   copy local.settings.json.example local.settings.json
   ```

4. **Setup containers:**
   ```bash
   python setup_containers.py
   ```

5. **Start development:**
   - Start Azurite
   - Start Azure Function
   - Test with `python test_upload.py`

---

## ✅ Summary

**Push these:**
- All `.py` files (except test scripts)
- `requirements.txt`
- `host.json`
- `function.json`
- `local.settings.json.example`
- Essential documentation (README, SETUP_GUIDE, HOW_TO_TEST)

**Don't push:**
- `local.settings.json` (secrets!)
- `__azurite__/` (local data)
- `__pycache__/` (cache)
- `.msg` / `.eml` files (test data)
- Verbose documentation files

**Your `.gitignore` is now configured to handle this automatically!** 🎉
