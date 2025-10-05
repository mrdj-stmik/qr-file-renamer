import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import numpy as np
from qreader import QReader
from pyzxing import BarCodeReader
import threading


class MultiQRDetector:
    """Kelas untuk deteksi QR menggunakan multiple library untuk akurasi maksimal"""
    
    def __init__(self):
        # Initialize all detectors
        self.opencv_detector = cv2.QRCodeDetector()
        self.qreader = QReader()
        self.zxing_reader = BarCodeReader()
        
    def enhance_image_variants(self, img):
        """Buat berbagai varian gambar untuk meningkatkan deteksi"""
        variants = []
        
        # Gambar asli
        variants.append(('original', img))
        
        # Convert ke grayscale jika colored
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            variants.append(('grayscale', gray))
        else:
            gray = img
            
        # Tingkatkan kontras dengan CLAHE
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        variants.append(('clahe_enhanced', enhanced))
        
        # Gaussian blur untuk mengurangi noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        variants.append(('blurred', blurred))
        
        # Threshold adaptif
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        variants.append(('adaptive_thresh', thresh))
        
        # Threshold dengan Otsu
        _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        variants.append(('otsu_thresh', otsu))
        
        # Morphological operations
        kernel = np.ones((2,2), np.uint8)
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        variants.append(('morphological', morph))
        
        # Resize untuk ukuran yang berbeda
        h, w = gray.shape
        if min(h, w) < 500:  # Jika terlalu kecil, perbesar
            scale = 500 / min(h, w)
            new_w, new_h = int(w * scale), int(h * scale)
            resized = cv2.resize(gray, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
            variants.append(('upscaled', resized))
        
        return variants
    
    def try_opencv_detector(self, img_variants, rotations=[0, 90, 180, 270]):
        """Coba OpenCV QR detector dengan berbagai variasi"""
        for variant_name, img in img_variants:
            for angle in rotations:
                try:
                    if angle != 0:
                        if len(img.shape) == 3:
                            h, w = img.shape[:2]
                        else:
                            h, w = img.shape
                        center = (w // 2, h // 2)
                        M = cv2.getRotationMatrix2D(center, angle, 1.0)
                        rotated = cv2.warpAffine(img, M, (w, h))
                    else:
                        rotated = img
                    
                    data, bbox, _ = self.opencv_detector.detectAndDecode(rotated)
                    if data and len(data.strip()) > 0:
                        return f"OpenCV({variant_name},rot{angle})", data.strip()
                except:
                    continue
        return None, None
    
    def try_qreader_detector(self, img_variants, rotations=[0, 90, 180, 270]):
        """Coba QReader detector"""
        for variant_name, img in img_variants:
            for angle in rotations:
                try:
                    if angle != 0:
                        if len(img.shape) == 3:
                            h, w = img.shape[:2]
                        else:
                            h, w = img.shape
                        center = (w // 2, h // 2)
                        M = cv2.getRotationMatrix2D(center, angle, 1.0)
                        rotated = cv2.warpAffine(img, M, (w, h))
                    else:
                        rotated = img
                    
                    # QReader butuh 3 channel
                    if len(rotated.shape) == 2:
                        rotated_rgb = cv2.cvtColor(rotated, cv2.COLOR_GRAY2RGB)
                    else:
                        rotated_rgb = cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB)
                    
                    results = self.qreader.detect_and_decode(rotated_rgb)
                    if results and len(results) > 0:
                        for result in results:
                            if result and len(result.strip()) > 0:
                                return f"QReader({variant_name},rot{angle})", result.strip()
                except:
                    continue
        return None, None
    
    def try_zxing_detector(self, original_img):
        """Coba ZXing detector (hanya dengan gambar asli karena butuh file)"""
        try:
            # Simpan temporary file
            temp_path = "temp_qr.jpg"
            cv2.imwrite(temp_path, original_img)
            
            # Decode dengan ZXing
            results = self.zxing_reader.decode(temp_path)
            
            # Hapus file temporary
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            if results and len(results) > 0:
                for result in results:
                    if 'parsed' in result and result['parsed']:
                        return "ZXing", result['parsed'].strip()
        except Exception as e:
            # Cleanup jika error
            if os.path.exists("temp_qr.jpg"):
                os.remove("temp_qr.jpg")
        return None, None
    
    def detect_qr_code(self, image_path):
        """Deteksi QR code menggunakan semua detector secara berurutan"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None, "❌ Tidak bisa membaca gambar"
            
            # Buat berbagai varian gambar
            img_variants = self.enhance_image_variants(img)
            
            # Coba berbagai detector secara berurutan
            detectors = [
                ("OpenCV", lambda: self.try_opencv_detector(img_variants)),
                ("QReader", lambda: self.try_qreader_detector(img_variants)),
                ("ZXing", lambda: self.try_zxing_detector(img))
            ]
            
            for detector_name, detector_func in detectors:
                try:
                    method, result = detector_func()
                    if result:
                        return result, f"✅ Berhasil dengan {method}"
                except Exception as e:
                    continue
            
            return None, "❌ Semua detector gagal"
            
        except Exception as e:
            return None, f"❌ Error: {str(e)}"


def process_files_ultra(input_folder, progress_var, status_label, progress_win, result_text):
    """Proses files dengan ultra-enhanced detection"""
    if not os.path.exists(input_folder):
        messagebox.showerror("Error", "Input folder tidak ditemukan!")
        return

    # Initialize detector
    detector = MultiQRDetector()
    
    # Hitung total file gambar
    all_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                all_files.append(os.path.join(root, file))

    total_files = len(all_files)
    if total_files == 0:
        messagebox.showinfo("Info", "Tidak ada file gambar yang ditemukan.")
        return

    progress_var.set(0)
    current_file = 0
    renamed = 0
    failed_qr = 0
    failed_pattern = 0
    
    log_text = f"=== LAPORAN ULTRA-ENHANCED QR DETECTION ===\n"
    log_text += f"Folder: {input_folder}\n"
    log_text += f"Total file: {total_files}\n"
    log_text += f"Detector: OpenCV + QReader + ZXing\n\n"
    
    for file_path in all_files:
        filename = os.path.basename(file_path)
        log_text += f"📷 {filename}: "
        
        qr_text, detection_info = detector.detect_qr_code(file_path)
        
        if qr_text:
            log_text += f"{detection_info}\n"
            log_text += f"   📄 QR Content: '{qr_text}'\n"
            
            # Cari 14 digit pattern
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
                        log_text += f"   ✅ RENAMED ke: {new_name}\n"
                    else:
                        log_text += f"   ⚠️  Skip (file {new_name} sudah ada)\n"
                except Exception as e:
                    log_text += f"   ❌ Gagal rename: {e}\n"
            else:
                failed_pattern += 1
                log_text += f"   ⚠️  Pattern 14 digit tidak ditemukan\n"
        else:
            failed_qr += 1
            log_text += f"{detection_info}\n"
        
        log_text += "\n"
        
        current_file += 1
        progress_var.set(current_file)
        status_label.config(text=f"{current_file}/{total_files} | ✅{renamed} ❌{failed_qr} ⚠️{failed_pattern}")
        progress_win.update_idletasks()
        
        # Update text secara real-time
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, log_text)
        result_text.see(tk.END)

    log_text += f"=== RINGKASAN FINAL ===\n"
    log_text += f"✅ Berhasil rename: {renamed}\n"
    log_text += f"❌ QR tidak terbaca: {failed_qr}\n"
    log_text += f"⚠️  QR terbaca tapi pattern tidak cocok: {failed_pattern}\n"
    log_text += f"📊 Tingkat keberhasilan: {(renamed/total_files*100):.1f}%\n"
    
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, log_text)
    
    messagebox.showinfo("Selesai", 
                       f"🎉 PROSES SELESAI! 🎉\n\n"
                       f"✅ {renamed} file berhasil di-rename\n"
                       f"❌ {failed_qr} QR tidak terbaca\n"
                       f"⚠️ {failed_pattern} pattern tidak cocok\n\n"
                       f"📊 Success Rate: {(renamed/total_files*100):.1f}%")


def start_process_ultra(entry_input, root):
    input_folder = entry_input.get()
    if not input_folder:
        messagebox.showerror("Error", "Pilih folder input terlebih dahulu!")
        return

    # Hitung total file gambar
    all_files = []
    for root_dir, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                all_files.append(os.path.join(root_dir, file))
    total_files = len(all_files)

    if total_files == 0:
        messagebox.showinfo("Info", "Tidak ada file gambar yang ditemukan.")
        return

    # Buat jendela progress
    progress_win = tk.Toplevel(root)
    progress_win.title("Ultra-Enhanced QR Detection Progress")
    progress_win.geometry("800x600")
    progress_win.resizable(True, True)
    
    # Header
    header_frame = tk.Frame(progress_win, bg="darkblue")
    header_frame.pack(fill=tk.X, padx=5, pady=5)
    
    tk.Label(header_frame, text="🚀 ULTRA-ENHANCED QR DETECTION", 
             font=("Arial", 14, "bold"), fg="white", bg="darkblue").pack(pady=5)
    tk.Label(header_frame, text="OpenCV + QReader + ZXing Multi-Detector", 
             font=("Arial", 10), fg="lightblue", bg="darkblue").pack()

    # Progress bar
    progress_var = tk.DoubleVar()
    progress_frame = tk.Frame(progress_win)
    progress_frame.pack(fill=tk.X, padx=10, pady=5)
    
    progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, 
                                  maximum=total_files, length=500)
    progress_bar.pack(pady=5)

    status_label = tk.Label(progress_frame, text="Memulai proses...", 
                           font=("Arial", 10))
    status_label.pack(pady=2)
    
    # Text area untuk log
    log_frame = tk.Frame(progress_win)
    log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    tk.Label(log_frame, text="📋 Live Detection Log:", 
             font=("Arial", 11, "bold")).pack(anchor="w")
    
    text_frame = tk.Frame(log_frame)
    text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    result_text = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 9),
                         bg="black", fg="lightgreen")
    scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=result_text.yview)
    result_text.configure(yscrollcommand=scrollbar.set)
    
    result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    progress_win.update()

    # Jalankan proses di thread terpisah untuk tidak freeze UI
    def run_process():
        process_files_ultra(input_folder, progress_var, status_label, progress_win, result_text)
    
    thread = threading.Thread(target=run_process)
    thread.daemon = True
    thread.start()


def browse_folder(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, tk.END)
        entry.insert(0, folder)


def main():
    root = tk.Tk()
    root.title("🚀 Ultra QR File Renamer v3.0 - Multi Detector")
    root.geometry("600x200")
    root.configure(bg="lightblue")

    # Header
    header_frame = tk.Frame(root, bg="darkblue")
    header_frame.pack(fill=tk.X, pady=5)
    
    tk.Label(header_frame, text="🔥 ULTRA QR FILE RENAMER 🔥", 
             font=("Arial", 16, "bold"), fg="white", bg="darkblue").pack(pady=5)
    tk.Label(header_frame, text="Triple Detection: OpenCV + QReader + ZXing", 
             font=("Arial", 11), fg="lightblue", bg="darkblue").pack()

    # Input folder
    input_frame = tk.Frame(root, bg="lightblue")
    input_frame.pack(fill=tk.X, padx=20, pady=10)
    
    tk.Label(input_frame, text="📁 Input Folder:", 
             font=("Arial", 12, "bold"), bg="lightblue").pack(anchor="w")
    
    entry_input = tk.Entry(input_frame, width=70, font=("Arial", 10))
    entry_input.pack(pady=5, fill=tk.X)
    
    tk.Button(input_frame, text="🔍 Browse", 
              command=lambda: browse_folder(entry_input),
              bg="blue", fg="white", font=("Arial", 10)).pack(pady=2)

    # Process button
    tk.Button(root, text="🚀 MULAI ULTRA DETECTION", 
              command=lambda: start_process_ultra(entry_input, root),
              bg="red", fg="white", font=("Arial", 14, "bold"), 
              relief="raised", bd=3).pack(pady=20)

    # Info
    info_frame = tk.Frame(root, bg="lightblue")
    info_frame.pack(fill=tk.X, padx=20)
    
    tk.Label(info_frame, text="💡 Menggunakan 3 detector sekaligus untuk akurasi maksimal!", 
             font=("Arial", 10, "italic"), fg="darkgreen", bg="lightblue").pack()

    root.mainloop()


if __name__ == "__main__":
    main()