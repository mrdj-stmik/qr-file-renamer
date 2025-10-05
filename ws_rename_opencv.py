import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def decode_qr_from_image(image_path):
    """Baca QR code dari gambar menggunakan OpenCV QRCodeDetector"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None

        # Buat QR code detector
        qr_detector = cv2.QRCodeDetector()
        
        # Coba decode dengan rotasi 0, 90, 180, 270 derajat
        for angle in [0, 90, 180, 270]:
            if angle != 0:
                # Rotasi gambar
                height, width = img.shape[:2]
                center = (width // 2, height // 2)
                rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
                img_rot = cv2.warpAffine(img, rot_mat, (width, height))
            else:
                img_rot = img
            
            # Coba decode QR code
            data, bbox, rectified_qr = qr_detector.detectAndDecode(img_rot)
            if data:
                return data.strip()
        
        return None
    except Exception as e:
        print(f"Error membaca {image_path}: {e}")
    return None


def process_files(input_folder, output_folder, progress_var, status_label, progress_win):
    """Proses semua file dalam folder dan subfolder"""
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
    import re
    renamed = 0
    for file_path in all_files:
        qr_text = decode_qr_from_image(file_path)
        if qr_text:
            match = re.match(r"(\d{14})", qr_text)
            if match:
                angka14 = match.group(1)
                ext = os.path.splitext(file_path)[1].lower()
                new_name = angka14 + "_2025" + ext
                save_path = os.path.join(os.path.dirname(file_path), new_name)
                try:
                    os.rename(file_path, save_path)
                    renamed += 1
                except Exception as e:
                    print(f"Gagal rename {file_path}: {e}")
        current_file += 1
        progress_var.set(current_file)
        status_label.config(text=f"{current_file}/{total_files} file diproses...")
        progress_win.update_idletasks()

    messagebox.showinfo("Selesai", f"Proses selesai! {renamed} file berhasil di-rename.")


def start_process(entry_input, entry_output, root):
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

    # Buat jendela progress
    progress_win = tk.Toplevel(root)
    progress_win.title("Progress Rename")
    tk.Label(progress_win, text="Progress Rename File").pack(pady=5)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(progress_win, variable=progress_var, maximum=total_files, length=300)
    progress_bar.pack(padx=10, pady=10)

    status_label = tk.Label(progress_win, text="")
    status_label.pack(pady=5)
    progress_win.update()

    process_files(input_folder, None, progress_var, status_label, progress_win)


def browse_folder(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, tk.END)
        entry.insert(0, folder)


def main():
    root = tk.Tk()
    root.title("QR File Renamer - (c) mdrj 2025 for BPS Tasikmalaya")
    root.geometry("500x150")

    tk.Label(root, text="Input Folder:").pack(pady=5)
    entry_input = tk.Entry(root, width=50)
    entry_input.pack(pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_folder(entry_input)).pack()

    tk.Button(root, text="Proses Rename", command=lambda: start_process(entry_input, None, root),
              bg="orange", fg="white").pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()