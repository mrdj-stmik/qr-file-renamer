"""
Universal QR File Renamer v2.0
Auto-detects and installs required dependencies

© mrdj 2025 for Team Wilkerstat 3206
BPS (Badan Pusat Statistik) Tasikmalaya

Features:
- Auto dependency installation
- Universal Python environment support
- Enhanced QR detection with multiple variants
- Professional GUI with real-time logging
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re
import threading
from datetime import datetime

# Auto-install dependencies if not available
def install_and_import(package, import_name=None):
    """Install package if not available and import it"""
    if import_name is None:
        import_name = package
    
    try:
        return __import__(import_name)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        try:
            return __import__(import_name)
        except ImportError:
            print(f"Failed to install {package}. Please install manually: pip install {package}")
            return None

# Install required packages
print("🔍 Checking dependencies...")
cv2 = install_and_import("opencv-python", "cv2")
np = install_and_import("numpy")

if cv2 is None:
    messagebox.showerror("Error", "OpenCV installation failed!\n\nPlease run:\npip install opencv-python\n\nThen try again.")
    sys.exit(1)

if np is None:
    messagebox.showerror("Error", "NumPy installation failed!\n\nPlease run:\npip install numpy\n\nThen try again.")
    sys.exit(1)

print("✅ All dependencies ready!")


class UniversalQRRenamer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌍 Universal QR File Renamer v2.0")
        self.root.geometry("700x550")
        self.root.configure(bg="white")
        
        self.detector = cv2.QRCodeDetector()
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="darkblue", height=100)
        header.pack(fill=tk.X, pady=(0,10))
        
        tk.Label(header, text="🌍 UNIVERSAL QR FILE RENAMER", 
                font=("Arial", 18, "bold"), fg="white", bg="darkblue").pack(pady=8)
        tk.Label(header, text="Auto-Install Dependencies | Enhanced Detection | Multi-Environment", 
                font=("Arial", 11), fg="lightblue", bg="darkblue").pack()
        tk.Label(header, text="© mrdj 2025 for Team Wilkerstat 3206", 
                font=("Arial", 9, "italic"), fg="lightgreen", bg="darkblue").pack(pady=2)
        
        # Environment info
        env_frame = tk.Frame(self.root, bg="lightgray")
        env_frame.pack(fill=tk.X, padx=20, pady=5)
        
        python_ver = f"Python {sys.version.split()[0]}"
        cv_ver = f"OpenCV {cv2.__version__}" if cv2 else "OpenCV: Not Available"
        
        tk.Label(env_frame, text=f"🐍 Environment: {python_ver} | 📷 {cv_ver}", 
                font=("Arial", 9), bg="lightgray", fg="darkgreen").pack(pady=3)
        
        # Input section
        input_frame = tk.Frame(self.root, bg="white")
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(input_frame, text="📁 Pilih Folder:", 
                font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        
        folder_frame = tk.Frame(input_frame, bg="white")
        folder_frame.pack(fill=tk.X, pady=5)
        
        self.folder_var = tk.StringVar()
        self.folder_entry = tk.Entry(folder_frame, textvariable=self.folder_var, 
                                    font=("Arial", 10), width=60)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(folder_frame, text="Browse", command=self.browse_folder,
                 bg="blue", fg="white", font=("Arial", 10)).pack(side=tk.RIGHT, padx=(5,0))
        
        # Process button
        tk.Button(self.root, text="🚀 MULAI PROSES RENAME", 
                 command=self.start_process,
                 bg="red", fg="white", font=("Arial", 16, "bold"),
                 height=2, relief="raised", bd=3).pack(pady=20)
        
        # Progress section
        self.progress_frame = tk.Frame(self.root, bg="white")
        self.progress_frame.pack(fill=tk.X, padx=20)
        
        self.status_label = tk.Label(self.progress_frame, text="🌍 Universal mode - Ready for any Python environment", 
                                    font=("Arial", 11), bg="white", fg="blue")
        self.status_label.pack(pady=5)
        
        # Log area
        log_frame = tk.Frame(self.root, bg="white")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(log_frame, text="📋 Live Processing Log:", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, 
                                                 font=("Consolas", 9),
                                                 bg="black", fg="lightgreen")
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Pilih folder yang berisi gambar QR code")
        if folder:
            self.folder_var.set(folder)
            self.log(f"📁 Folder dipilih: {folder}")
            
            # Hitung file
            count = 0
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith((".png", ".jpg", ".jpeg")):
                        count += 1
            
            self.log(f"📊 Ditemukan {count} file gambar")
            self.status_label.config(text=f"Siap memproses {count} file gambar dengan enhanced detection")
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def enhance_image_variants(self, img):
        """Create multiple image variants for better detection"""
        variants = [img]  # Original
        
        # Grayscale
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            variants.append(gray)
            
            # Enhanced contrast
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            variants.append(enhanced)
            
            # Threshold variants
            _, thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            variants.append(thresh1)
            
            _, thresh2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            variants.append(thresh2)
        
        return variants
    
    def detect_qr_enhanced(self, image_path):
        """Enhanced QR detection with multiple variants and rotations"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None
            
            # Create image variants
            variants = self.enhance_image_variants(img)
            
            # Try detection with different variants and rotations
            for variant in variants:
                for angle in [0, 90, 180, 270]:
                    try:
                        if angle != 0:
                            if len(variant.shape) == 3:
                                h, w = variant.shape[:2]
                            else:
                                h, w = variant.shape
                            center = (w // 2, h // 2)
                            M = cv2.getRotationMatrix2D(center, angle, 1.0)
                            rotated = cv2.warpAffine(variant, M, (w, h))
                        else:
                            rotated = variant
                        
                        data, bbox, _ = self.detector.detectAndDecode(rotated)
                        if data and len(data.strip()) > 0:
                            return data.strip()
                    except:
                        continue
            
            return None
        except:
            return None
    
    def process_files(self):
        folder = self.folder_var.get()
        if not folder:
            messagebox.showerror("Error", "Pilih folder terlebih dahulu!")
            return
        
        self.log("🚀 Memulai enhanced QR detection...")
        self.log(f"🔧 Using OpenCV {cv2.__version__} with {len(self.enhance_image_variants(np.zeros((100,100,3), dtype=np.uint8)))} variants × 4 rotations")
        
        # Collect all image files
        all_files = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    all_files.append(os.path.join(root, file))
        
        total = len(all_files)
        renamed = 0
        failed_qr = 0
        failed_pattern = 0
        
        self.log(f"📊 Processing {total} files...")
        
        for i, file_path in enumerate(all_files, 1):
            filename = os.path.basename(file_path)
            self.status_label.config(text=f"Processing {i}/{total}: {filename}")
            
            # Detect QR
            qr_text = self.detect_qr_enhanced(file_path)
            
            if qr_text:
                # Find 14 digit pattern
                match = re.search(r"(\d{14})", qr_text)
                if match:
                    angka14 = match.group(1)
                    ext = os.path.splitext(file_path)[1].lower()
                    new_name = angka14 + "_2025" + ext
                    new_path = os.path.join(os.path.dirname(file_path), new_name)
                    
                    try:
                        if not os.path.exists(new_path):
                            os.rename(file_path, new_path)
                            renamed += 1
                            self.log(f"✅ {filename} → {new_name}")
                        else:
                            self.log(f"⚠️  {filename} → Skip (sudah ada)")
                    except Exception as e:
                        failed_qr += 1
                        self.log(f"❌ {filename} → Rename error: {e}")
                else:
                    failed_pattern += 1
                    self.log(f"⚠️  {filename} → QR: '{qr_text[:30]}...' (bukan 14 digit)")
            else:
                failed_qr += 1
                self.log(f"❌ {filename} → QR tidak terbaca")
        
        # Summary
        success_rate = (renamed/total*100) if total > 0 else 0
        self.log(f"\n🎉 PROSES SELESAI!")
        self.log(f"✅ Berhasil rename: {renamed}")
        self.log(f"❌ QR tidak terbaca: {failed_qr}")
        self.log(f"⚠️  Pattern tidak cocok: {failed_pattern}")
        self.log(f"📊 Success rate: {success_rate:.1f}%")
        
        self.status_label.config(text=f"Selesai! {renamed} berhasil, {failed_qr+failed_pattern} gagal ({success_rate:.1f}%)")
        
        messagebox.showinfo("Proses Selesai", 
                           f"🎉 Universal QR Processing Complete! 🎉\n\n"
                           f"✅ Berhasil: {renamed}\n"
                           f"❌ QR tidak terbaca: {failed_qr}\n"
                           f"⚠️ Pattern tidak cocok: {failed_pattern}\n\n"
                           f"📊 Success rate: {success_rate:.1f}%\n\n"
                           f"© mrdj 2025 for Team Wilkerstat 3206")
    
    def start_process(self):
        if not self.folder_var.get():
            messagebox.showerror("Error", "Pilih folder terlebih dahulu!")
            return
        
        # Run in thread to prevent UI freeze
        thread = threading.Thread(target=self.process_files)
        thread.daemon = True
        thread.start()
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    try:
        print("🌍 Starting Universal QR File Renamer...")
        app = UniversalQRRenamer()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Application error: {e}")
        sys.exit(1)