import tkinter as tk
from tkinter import filedialog, messagebox
import os

def test_gui():
    """Test sederhana untuk memastikan GUI berjalan"""
    root = tk.Tk()
    root.title("Test GUI - QR Renamer")
    root.geometry("400x300")
    root.configure(bg="lightblue")
    
    # Test label
    tk.Label(root, text="🚀 GUI Test Berhasil!", 
             font=("Arial", 16, "bold"), bg="lightblue").pack(pady=20)
    
    # Test input
    tk.Label(root, text="Input Folder:", bg="lightblue").pack()
    entry = tk.Entry(root, width=50)
    entry.pack(pady=5)
    
    def browse_test():
        folder = filedialog.askdirectory()
        if folder:
            entry.delete(0, tk.END)
            entry.insert(0, folder)
            messagebox.showinfo("Success", f"Folder dipilih: {folder}")
    
    # Test browse button
    tk.Button(root, text="🔍 Browse Folder", 
              command=browse_test, 
              bg="blue", fg="white", 
              font=("Arial", 12)).pack(pady=10)
    
    # Test process button
    def test_process():
        folder = entry.get()
        if folder:
            # Hitung file
            count = 0
            for root_dir, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith((".png", ".jpg", ".jpeg")):
                        count += 1
            
            messagebox.showinfo("Test", f"Ditemukan {count} file gambar di folder ini!")
        else:
            messagebox.showerror("Error", "Pilih folder dulu!")
    
    tk.Button(root, text="🚀 TEST PROSES", 
              command=test_process,
              bg="green", fg="white", 
              font=("Arial", 14, "bold")).pack(pady=20)
    
    tk.Label(root, text="Jika Anda bisa melihat window ini,\nberarti GUI berfungsi dengan baik!", 
             bg="lightblue", fg="darkgreen").pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    print("Membuka GUI Test...")
    test_gui()
    print("GUI Test selesai.")