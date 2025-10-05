# QR File Renamer v2025 - Distribution Package

## 📦 **Portable Distribution (No Python Required for End Users)**

Since creating a full .exe requires significant disk space, we've created a **portable distribution** that's easy to share and use.

## 🚀 **Distribution Options**

### **Option 1: Portable Launcher (Recommended)**
**File:** `QR_RENAMER_PORTABLE.bat`

**Features:**
- ✅ **Menu-driven interface**
- ✅ **Multiple version selection**
- ✅ **Auto dependency installation**
- ✅ **Help and instructions**  
- ✅ **Error handling**

**How to use:**
1. Copy entire folder to target computer
2. Double-click `QR_RENAMER_PORTABLE.bat`
3. Choose version to run
4. Follow on-screen instructions

### **Option 2: One-Click Installer**
**File:** `INSTALL_QR_RENAMER.bat`

**Features:**
- ✅ **Automatic Python detection**
- ✅ **Dependency installation**
- ✅ **Desktop shortcut creation**
- ✅ **Installation testing**
- ✅ **Launch option**

**How to use:**
1. Copy entire folder to target computer
2. Double-click `INSTALL_QR_RENAMER.bat`
3. Follow installation steps
4. Use desktop shortcut or batch files

### **Option 3: Universal Python Script**
**File:** `ws_rename_universal.py`

**Features:**
- ✅ **Auto-install dependencies**
- ✅ **Works with any Python 3.7+**
- ✅ **Enhanced QR detection**
- ✅ **Professional GUI**

**How to use:**
```bash
python ws_rename_universal.py
```

## 📋 **Distribution Checklist**

### **Files to Include in Distribution:**
```
✅ ws_rename_universal.py      - Main universal version
✅ ws_rename_stable.py         - Advanced stable version
✅ ws_rename_simple.py         - Basic version
✅ ws_rename_debug.py          - Debug tools
✅ QR_RENAMER_PORTABLE.bat     - Portable launcher
✅ INSTALL_QR_RENAMER.bat      - One-click installer
✅ run_qr_renamer.bat          - Simple runner
✅ README.md                   - Documentation
✅ RUN_INSTRUCTIONS.md         - Detailed instructions
✅ requirements.txt            - Python dependencies
```

### **Optional Files:**
```
⚪ test_gui.py                 - GUI testing
⚪ LICENSE                     - MIT License
⚪ .gitignore                  - For developers
```

## 🎯 **Recommended Distribution Method**

### **For End Users (Non-Technical):**
1. **Copy entire folder** to USB or shared drive
2. **Include `INSTALL_QR_RENAMER.bat`** as main installer
3. **Include `QR_RENAMER_PORTABLE.bat`** as launcher
4. **Add simple README.txt** with basic instructions

### **For Technical Users:**
1. **Share GitHub repository:** https://github.com/mrdj-stmik/qr-file-renamer
2. **Clone and run:** `python ws_rename_universal.py`

## 💾 **Creating Distribution ZIP**

```bash
# Create distribution folder
mkdir QR_File_Renamer_v2025_Distribution
copy ws_rename_universal.py QR_File_Renamer_v2025_Distribution/
copy ws_rename_stable.py QR_File_Renamer_v2025_Distribution/
copy QR_RENAMER_PORTABLE.bat QR_File_Renamer_v2025_Distribution/
copy INSTALL_QR_RENAMER.bat QR_File_Renamer_v2025_Distribution/
copy README.md QR_File_Renamer_v2025_Distribution/
copy RUN_INSTRUCTIONS.md QR_File_Renamer_v2025_Distribution/

# Compress to ZIP
# Ready for distribution!
```

## 🔧 **System Requirements**

**Minimum:**
- Windows 7/10/11
- Python 3.7+ (auto-installed by installers)
- 100MB free space
- Internet connection (for dependency installation)

**Recommended:**
- Windows 10/11
- Python 3.9+
- 500MB free space
- Stable internet connection

## 📞 **Support Information**

**Created by:** mrdj 2025 for Team Wilkerstat 3206  
**Version:** 2025  
**Repository:** https://github.com/mrdj-stmik/qr-file-renamer  
**License:** MIT

---

**This portable distribution provides an excellent alternative to .exe files while maintaining full functionality and ease of use!** 🎉