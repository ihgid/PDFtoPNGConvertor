import os
import fitz  # PyMuPDF
import threading
import time
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from datetime import datetime

class UniversalConverter(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Universal PDF & Image Converter")
        self.geometry("700x700")
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#1A1A1A")

        # --- STEP 1: FOLDER SELECTION ---
        self.header = ctk.CTkLabel(self, text="Step 1: Select your files", font=("SF Pro Display", 22, "bold"))
        self.header.pack(pady=(30, 10))

        self.btn_select = ctk.CTkButton(self, text="📁 Choose Folder", height=40, corner_radius=10, 
                                        fg_color="#007AFF", command=self.select_folder)
        self.btn_select.pack(pady=10)

        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.pack(pady=10)
        self.file_info_label = ctk.CTkLabel(self.info_frame, text="", font=("SF Pro Text", 14))
        self.file_info_label.pack()

        # --- STEP 2: CUSTOMIZATION (Hidden initially) ---
        self.step2_frame = ctk.CTkFrame(self, fg_color="#252525", corner_radius=15)
        
        self.header2 = ctk.CTkLabel(self.step2_frame, text="Step 2: Customization", font=("SF Pro Display", 18, "bold"))
        self.header2.pack(pady=10)

        self.prefix_label = ctk.CTkLabel(self.step2_frame, text="Would you like to add a prefix to the filenames?\n(Leave blank to keep original names)", font=("SF Pro Text", 12))
        self.prefix_label.pack(pady=5)

        self.prefix_entry = ctk.CTkEntry(self.step2_frame, placeholder_text="e.g. ProjectA", width=300)
        self.prefix_entry.pack(pady=5)
        self.prefix_entry.bind("<KeyRelease>", self.update_peek)

        self.peek_label = ctk.CTkLabel(self.step2_frame, text="Preview: filename.png", text_color="#007AFF", font=("Consolas", 12))
        self.peek_label.pack(pady=5)

        # --- STEP 3: EXECUTION ---
        self.btn_run = ctk.CTkButton(self.step2_frame, text="🚀 Convert PDF to PNG", height=45, 
                                     fg_color="#28a745", hover_color="#218838", font=("SF Pro Display", 16, "bold"),
                                     command=self.start_thread)
        self.btn_run.pack(pady=20)

        # --- TERMINAL / LOGS ---
        self.console_label = ctk.CTkLabel(self, text="Conversion Logs:", font=("SF Pro Text", 10))
        self.console_label.pack(pady=(20, 0), padx=40, anchor="w")
        
        self.console = ctk.CTkTextbox(self, height=150, width=620, font=("Consolas", 12), fg_color="#000000", text_color="#00FF00")
        self.console.pack(pady=10, padx=40)

        self.progress_bar = ctk.CTkProgressBar(self, width=620, progress_color="#007AFF")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        # --- FINAL ACTIONS ---
        self.btn_new = ctk.CTkButton(self, text="Start New Task", command=self.reset_ui, fg_color="#3A3A3A")
        
        self.source_dir = ""
        self.first_file_name = ""

    def select_folder(self):
        self.source_dir = filedialog.askdirectory()
        if self.source_dir:
            pdf_count = 0
            img_count = 0
            self.first_file_name = ""
            
            for root, _, files in os.walk(self.source_dir):
                for f in files:
                    ext = f.lower()
                    if not self.first_file_name and (ext.endswith(".pdf") or ext.endswith(('.png', '.jpg', '.jpeg', '.webp', '.avif'))):
                        self.first_file_name = Path(f).stem
                    if ext.endswith(".pdf"): pdf_count += 1
                    elif ext.endswith(('.png', '.jpg', '.jpeg', '.webp', '.avif')): img_count += 1
            
            self.file_info_label.configure(text=f"📂 {pdf_count} PDFs and {img_count} Images ready.")
            self.step2_frame.pack(pady=20, padx=40, fill="x")
            self.update_peek()

    def update_peek(self, event=None):
        prefix = self.prefix_entry.get().strip()
        if self.first_file_name:
            name = f"{prefix}_{self.first_file_name}.png" if prefix else f"{self.first_file_name}.png"
            self.peek_label.configure(text=f"Preview: {name}")

    def log(self, text):
        self.console.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {text}\n")
        self.console.see("end")

    def get_safe_path(self, directory, filename):
        """Ensures non-destructive saving by adding a counter if file exists."""
        base, extension = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        while os.path.exists(os.path.join(directory, new_filename)):
            new_filename = f"{base}_{counter}{extension}"
            counter += 1
        return os.path.join(directory, new_filename)

    def start_thread(self):
        self.btn_run.configure(state="disabled")
        threading.Thread(target=self.process_files, daemon=True).start()

    def process_files(self):
        dest_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Converted_Output")
        os.makedirs(dest_dir, exist_ok=True)
        
        prefix = self.prefix_entry.get().strip()
        all_files = []
        for root, _, files in os.walk(self.source_dir):
            for f in files: all_files.append(os.path.join(root, f))
        
        total = len(all_files)
        self.log(f"Starting conversion of {total} items...")

        for index, path in enumerate(all_files):
            ext = os.path.splitext(path)[1].lower()
            stem = Path(path).stem
            name_base = f"{prefix}_{stem}" if prefix else stem
            
            try:
                if ext == ".pdf":
                    doc = fitz.open(path)
                    for i in range(len(doc)):
                        pix = doc[i].get_pixmap(matrix=fitz.Matrix(2, 2))
                        fname = f"{name_base}_p{i+1}.png"
                        pix.save(self.get_safe_path(dest_dir, fname))
                    doc.close()
                    self.log(f"Converted PDF: {stem}")
                elif ext in ('.png', '.jpg', '.jpeg', '.webp', '.avif'):
                    with Image.open(path) as img:
                        if img.mode in ("RGBA", "P", "LA"): img = img.convert("RGB")
                        fname = f"{name_base}.png"
                        img.save(self.get_safe_path(dest_dir, fname), "PNG")
                    self.log(f"Converted Image: {stem}")
            except Exception as e:
                self.log(f"FAILED: {stem} ({str(e)})")

            self.progress_bar.set((index + 1) / total)

        self.log("✨ ALL TASKS COMPLETED SUCCESSFULLY")
        self.btn_new.pack(pady=10)
        os.startfile(dest_dir)

    def reset_ui(self):
        self.step2_frame.pack_forget()
        self.btn_new.pack_forget()
        self.file_info_label.configure(text="")
        self.progress_bar.set(0)
        self.console.delete("1.0", "end")
        self.prefix_entry.delete(0, "end")
        self.source_dir = ""

if __name__ == "__main__":
    app = UniversalConverter()
    app.mainloop()