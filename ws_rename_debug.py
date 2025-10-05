import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re


def decode_qr_from_image(image_path):
    """Baca QR code dari gambar menggunakan OpenCV QRCodeDetector dengan debug info"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"❌ Tidak bisa membaca gambar: {image_path}")
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
                print(f"✅ QR code ditemukan di {os.path.basename(image_path)} (rotasi {angle}°): '{data}'")
                return data.strip()
        
        print(f"❌ QR code tidak ditemukan di: {os.path.basename(image_path)}")
        return None
    except Exception as e:
        print(f"❌ Error membaca {os.path.basename(image_path)}: {e}")
    return None


def test_folder_qr_detection(folder_path):
    """Test QR detection pada semua file dalam folder"""
    if not os.path.exists(folder_path):
        print("❌ Folder tidak ditemukan!")
        return

    print(f"\n🔍 Menganalisis folder: {folder_path}")
    print("=" * 70)
    
    # Ambil semua file gambar
    image_files = []
    for file in os.listdir(folder_path):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            image_files.append(os.path.join(folder_path, file))
    
    print(f"📁 Total file gambar: {len(image_files)}")
    print()
    
    successful_reads = 0
    failed_reads = 0
    pattern_matches = 0
    
    for image_path in image_files:
        filename = os.path.basename(image_path)
        print(f"📷 Memproses: {filename}")
        
        qr_text = decode_qr_from_image(image_path)
        if qr_text:
            successful_reads += 1
            
            # Cek apakah cocok dengan pattern 14 digit
            match = re.match(r"(\d{14})", qr_text)
            if match:
                angka14 = match.group(1)
                pattern_matches += 1
                new_name = angka14 + "_2025" + os.path.splitext(image_path)[1].lower()
                print(f"   ✅ Pattern cocok! Akan diubah ke: {new_name}")
            else:
                print(f"   ⚠️  QR code ditemukan tapi tidak cocok pattern 14 digit: '{qr_text}'")
        else:
            failed_reads += 1
            print(f"   ❌ QR code tidak terbaca")
        
        print()
    
    print("=" * 70)
    print(f"📊 RINGKASAN:")
    print(f"   • Total file: {len(image_files)}")
    print(f"   • QR berhasil dibaca: {successful_reads}")
    print(f"   • QR gagal dibaca: {failed_reads}")
    print(f"   • Pattern 14 digit cocok: {pattern_matches}")
    print(f"   • Persentase keberhasilan: {(successful_reads/len(image_files)*100):.1f}%")


def main():
    root = tk.Tk()
    root.title("QR Debug Tool - Test Pembacaan QR Code")
    root.geometry("600x200")

    tk.Label(root, text="Pilih folder untuk test pembacaan QR code:", font=("Arial", 12)).pack(pady=10)
    
    folder_var = tk.StringVar()
    entry_folder = tk.Entry(root, textvariable=folder_var, width=80)
    entry_folder.pack(pady=5)
    
    def browse_folder():
        folder = filedialog.askdirectory(title="Pilih folder yang berisi gambar QR code")
        if folder:
            folder_var.set(folder)
    
    tk.Button(root, text="Browse Folder", command=browse_folder, bg="blue", fg="white").pack(pady=5)
    
    def start_test():
        folder = folder_var.get()
        if not folder:
            messagebox.showerror("Error", "Pilih folder terlebih dahulu!")
            return
        
        print("\n" + "="*70)
        print("🚀 MEMULAI TEST PEMBACAAN QR CODE")
        print("="*70)
        test_folder_qr_detection(folder)
        messagebox.showinfo("Selesai", "Test selesai! Lihat hasil di console/terminal.")
    
    tk.Button(root, text="🔍 Test Pembacaan QR", command=start_test, 
              bg="green", fg="white", font=("Arial", 11, "bold")).pack(pady=20)
    
    tk.Label(root, text="Hasil akan ditampilkan di console/terminal", 
             font=("Arial", 9), fg="gray").pack()

    root.mainloop()


if __name__ == "__main__":
    main()