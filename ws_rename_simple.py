import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re
import threading
from datetime import datetime


class SimpleQRRenamer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔥 Simple QR File Renamer")
        self.root.geometry("700x500")
        self.root.configure(bg="white")
        
        self.detector = cv2.QRCodeDetector()
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="darkblue", height=80)
        header.pack(fill=tk.X, pady=(0,10))
        
        tk.Label(header, text="🔥 SIMPLE QR FILE RENAMER", 
                font=("Arial", 18, "bold"), fg="white", bg="darkblue").pack(pady=15)
        
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
                 height=2, relief="raised", bd=3).pack(pady=30)
        
        # Progress section
        self.progress_frame = tk.Frame(self.root, bg="white")
        self.progress_frame.pack(fill=tk.X, padx=20)
        
        self.status_label = tk.Label(self.progress_frame, text="Siap untuk memproses...", 
                                    font=("Arial", 11), bg="white", fg="blue")
        self.status_label.pack(pady=5)
        
        # Log area
        log_frame = tk.Frame(self.root, bg="white")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(log_frame, text="📋 Log Proses:", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, 
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
            self.status_label.config(text=f"Siap memproses {count} file gambar")
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def detect_qr_simple(self, image_path):
        """Deteksi QR dengan method enhanced tapi simple"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None
            
            # Coba berbagai preprocessing
            variants = [img]
            
            # Grayscale
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                variants.append(gray)
                
                # Enhanced contrast
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                enhanced = clahe.apply(gray)
                variants.append(enhanced)
            
            # Coba deteksi dengan rotasi
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
        
        self.log("🚀 Memulai proses rename...")
        
        # Collect all image files
        all_files = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    all_files.append(os.path.join(root, file))
        
        total = len(all_files)
        renamed = 0
        failed = 0
        
        self.log(f"📊 Total file: {total}")
        
        for i, file_path in enumerate(all_files, 1):
            filename = os.path.basename(file_path)
            self.status_label.config(text=f"Memproses {i}/{total}: {filename}")
            
            # Detect QR
            qr_text = self.detect_qr_simple(file_path)
            
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
                        failed += 1
                        self.log(f"❌ {filename} → Error: {e}")
                else:
                    failed += 1
                    self.log(f"⚠️  {filename} → QR: '{qr_text}' (bukan 14 digit)")
            else:
                failed += 1
                self.log(f"❌ {filename} → QR tidak terbaca")
        
        # Summary
        self.log(f"\n🎉 SELESAI!")
        self.log(f"✅ Berhasil rename: {renamed}")
        self.log(f"❌ Gagal: {failed}")
        self.log(f"📊 Success rate: {(renamed/total*100):.1f}%")
        
        self.status_label.config(text=f"Selesai! {renamed} file berhasil, {failed} gagal")
        
        messagebox.showinfo("Selesai", 
                           f"Proses selesai!\n\n"
                           f"✅ Berhasil: {renamed}\n"
                           f"❌ Gagal: {failed}\n"
                           f"📊 Success rate: {(renamed/total*100):.1f}%")
    
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
    app = SimpleQRRenamer()
    app.run()