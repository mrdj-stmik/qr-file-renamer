import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import numpy as np


def enhance_image_for_qr(img):
    """Tingkatkan kualitas gambar untuk pembacaan QR yang lebih baik"""
    # Convert ke grayscale
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    # Tingkatkan kontras
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # Gaussian blur untuk mengurangi noise
    blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
    
    # Threshold adaptif
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
    
    return [enhanced, thresh, blurred]


def decode_qr_from_image(image_path):
    """Baca QR code dengan berbagai teknik enhancement"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None

        # Buat QR code detector
        qr_detector = cv2.QRCodeDetector()
        
        # Coba berbagai preprocessing
        variants = [img]  # Gambar asli
        variants.extend(enhance_image_for_qr(img))  # Gambar yang diperbaiki
        
        # Coba decode dengan berbagai variasi gambar dan rotasi
        for variant in variants:
            for angle in [0, 90, 180, 270]:
                if angle != 0:
                    if len(variant.shape) == 3:
                        height, width = variant.shape[:2]
                    else:
                        height, width = variant.shape
                    center = (width // 2, height // 2)
                    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
                    img_rot = cv2.warpAffine(variant, rot_mat, (width, height))
                else:
                    img_rot = variant
                
                # Coba decode QR code
                try:
                    data, bbox, rectified_qr = qr_detector.detectAndDecode(img_rot)
                    if data and len(data.strip()) > 0:
                        return data.strip()
                except:
                    continue
        
        return None
    except Exception as e:
        print(f"Error membaca {image_path}: {e}")
    return None


def process_files(input_folder, progress_var, status_label, progress_win, result_text):
    """Proses semua file dalam folder dan subfolder dengan logging detail"""
    if not os.path.exists(input_folder):
        messagebox.showerror("Error", "Input folder tidak ditemukan!")
        return

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
    
    log_text = f"=== LAPORAN PROSES RENAME ===\n"
    log_text += f"Folder: {input_folder}\n"
    log_text += f"Total file: {total_files}\n\n"
    
    for file_path in all_files:
        filename = os.path.basename(file_path)
        log_text += f"📷 {filename}: "
        
        qr_text = decode_qr_from_image(file_path)
        if qr_text:
            # Coba ekstrak 14 digit pertama
            match = re.search(r"(\d{14})", qr_text)
            if match:
                angka14 = match.group(1)
                ext = os.path.splitext(file_path)[1].lower()
                new_name = angka14 + "_2025" + ext
                new_path = os.path.join(os.path.dirname(file_path), new_name)
                
                try:
                    if not os.path.exists(new_path):  # Hindari overwrite
                        os.rename(file_path, new_path)
                        renamed += 1
                        log_text += f"✅ RENAMED ke {new_name}\n"
                    else:
                        log_text += f"⚠️  Skip (file {new_name} sudah ada)\n"
                except Exception as e:
                    log_text += f"❌ Gagal rename: {e}\n"
            else:
                failed_pattern += 1
                log_text += f"⚠️  QR terbaca '{qr_text}' tapi tidak ada 14 digit\n"
        else:
            failed_qr += 1
            log_text += f"❌ QR tidak terbaca\n"
        
        current_file += 1
        progress_var.set(current_file)
        status_label.config(text=f"{current_file}/{total_files} file diproses... ({renamed} berhasil)")
        progress_win.update_idletasks()

    log_text += f"\n=== RINGKASAN ===\n"
    log_text += f"✅ Berhasil rename: {renamed}\n"
    log_text += f"❌ QR tidak terbaca: {failed_qr}\n"
    log_text += f"⚠️  QR terbaca tapi pattern tidak cocok: {failed_pattern}\n"
    log_text += f"📊 Tingkat keberhasilan: {(renamed/total_files*100):.1f}%\n"
    
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, log_text)
    
    messagebox.showinfo("Selesai", f"Proses selesai!\n\n✅ {renamed} file berhasil di-rename\n❌ {failed_qr} QR tidak terbaca\n⚠️ {failed_pattern} pattern tidak cocok")


def start_process(entry_input, root):
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

    # Buat jendela progress dengan log
    progress_win = tk.Toplevel(root)
    progress_win.title("Progress Rename")
    progress_win.geometry("600x500")
    
    tk.Label(progress_win, text="Progress Rename File", font=("Arial", 12, "bold")).pack(pady=5)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(progress_win, variable=progress_var, maximum=total_files, length=400)
    progress_bar.pack(padx=10, pady=10)

    status_label = tk.Label(progress_win, text="")
    status_label.pack(pady=5)
    
    # Text area untuk log
    tk.Label(progress_win, text="Laporan Detail:", font=("Arial", 10, "bold")).pack(pady=(10,0))
    text_frame = tk.Frame(progress_win)
    text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    result_text = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 9))
    scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=result_text.yview)
    result_text.configure(yscrollcommand=scrollbar.set)
    
    result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    progress_win.update()

    process_files(input_folder, progress_var, status_label, progress_win, result_text)


def browse_folder(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, tk.END)
        entry.insert(0, folder)


def main():
    root = tk.Tk()
    root.title("QR File Renamer v2 - Enhanced Detection")
    root.geometry("500x150")

    tk.Label(root, text="Input Folder:", font=("Arial", 10, "bold")).pack(pady=5)
    entry_input = tk.Entry(root, width=60, font=("Arial", 10))
    entry_input.pack(pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_folder(entry_input)).pack()

    tk.Button(root, text="🚀 Proses Rename (Enhanced)", 
              command=lambda: start_process(entry_input, root),
              bg="orange", fg="white", font=("Arial", 11, "bold")).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()