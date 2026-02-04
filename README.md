## 🌟 Overview
**PDFtoPNGConvertor** was built to solve the headache of manual file conversion. Whether you are dealing with engineering "Flat Plate" drawings in PDF format or modern web images like AVIF and WEBP, this tool standardizes everything into AI-ready PNGs in seconds.

## ✨ Key Features
- **Stepped User Interface:** The UI "unfolds" logically—select folder, customize, then convert.
- **Non-Destructive Workflow:** Smart file-saving logic ensures existing files are never overwritten; it simply adds an increment (e.g., `_1`, `_2`) to the name.
- **Live Terminal Console:** A built-in terminal window provides real-time feedback on every file processed.
- **Dynamic File Peek:** See an instant preview of your new filename as you type your optional prefix.
- **Deep Scan Logic:** Automatically finds all supported files buried deep within nested subfolders.

---

## 🛠️ Technical Specifications
- **PDF Engine:** PyMuPDF (300 DPI high-fidelity rendering)
- **Image Engine:** Pillow (Handles AVIF, WEBP, JPEG, GIF, and PNG)
- **UI Framework:** CustomTkinter (Modern Dark Mode)

---

## 📥 Installation & Setup

### Option 1: For Developers (Source Code)
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/PDFtoPNGConvertor.git](https://github.com/YOUR_USERNAME/PDFtoPNGConvertor.git)
   cd PDFtoPNGConvertor
