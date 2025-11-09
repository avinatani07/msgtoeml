# Quick Git Push Commands

## 🚀 Step-by-Step (Copy & Paste)

### **1. Initialize Git**
```bash
git init
```

### **2. Check What Will Be Pushed**
```bash
git status
```

**Make sure you DON'T see:**
- ❌ `local.settings.json` (only `.example` should show)
- ❌ `__azurite__/` folder
- ❌ `.msg` or `.eml` files
- ❌ `__pycache__/` folders

### **3. Add All Files**
```bash
git add .
```

### **4. Commit**
```bash
git commit -m "Initial commit: MSG to EML Azure Function converter"
```

### **5. Create GitHub Repo**
- Go to https://github.com/new
- Create a new repository
- Copy the repository URL

### **6. Connect to GitHub**
```bash
git remote add origin YOUR_REPO_URL_HERE
```

Example:
```bash
git remote add origin https://github.com/yourusername/msg-to-eml-converter.git
```

### **7. Push to GitHub**
```bash
git push -u origin main
```

If it says branch is `master` instead:
```bash
git branch -M main
git push -u origin main
```

---

## ✅ What Gets Pushed

**Essential files (will be pushed):**
- `function_app.py` - Main function
- `services/` - All service files
- `utils/` - Utilities
- `models/` - Data models
- `requirements.txt` - Dependencies
- `host.json` - Configuration
- `local.settings.json.example` - Config template
- `README.md`, `SETUP_GUIDE.md`, `HOW_TO_TEST.md` - Docs
- `setup_containers.py`, `test_upload.py` - Setup scripts

**Excluded (won't be pushed):**
- `local.settings.json` - Your secrets ✅
- `__azurite__/` - Local storage data ✅
- `__pycache__/` - Python cache ✅
- `.kiro/` - IDE files ✅
- `*.msg`, `*.eml` - Test files ✅
- Extra documentation files ✅

---

## 🔒 Security Check

Before pushing, verify:
```bash
git status | findstr "local.settings.json"
```

**Should show:** `local.settings.json.example`  
**Should NOT show:** `local.settings.json`

If `local.settings.json` appears, run:
```bash
git rm --cached local.settings.json
```

---

## 🎯 Done!

After pushing, your team can clone and run:
```bash
git clone YOUR_REPO_URL
cd your-repo
pip install -r requirements.txt
copy local.settings.json.example local.settings.json
python setup_containers.py
```
