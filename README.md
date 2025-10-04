# ATNYCHI Toolkit

This repository collects the build and release collateral for the ATNYCHI
utility along with a small helper script used during content preparation.
It is intended to accompany the broader ATNYCHI dossier while providing a
clear, reproducible process for creating signed Windows binaries and
verifying their integrity.

## Purpose

- **Release automation reference** – step-by-step instructions for packaging
  the ATNYCHI executable from multiple language implementations.
- **Integrity guarantees** – repeatable hashing and signing practices for the
  published artifacts.
- **Image processing helper** – a lightweight Python tool that deduplicates
  JPEG files and optionally performs OCR to capture embedded text.

## Usage

### Image Processing Utility

The `process_images.py` script mirrors the behaviour from the exploratory
Python session captured in the ATNYCHI dossier.  It scans for JPEG files,
removes duplicates based on an MD5 content hash, and can run OCR when
`pillow` and `pytesseract` are available.

```bash
# Search for JPEG files matching input_file_*.jpeg in the current directory
python process_images.py

# Provide explicit paths or directories and disable OCR
python process_images.py path/to/images --no-ocr
```

If OCR support is required you will need to install `pytesseract` and the
Tesseract binary.

## Build Instructions

The project ships reference implementations in Python, Go, Rust, and .NET.
Choose the toolchain that matches the source you are packaging.

### Python (PyInstaller)

```powershell
py -m venv venv
.\venv\Scripts\pip install --upgrade pip pyinstaller
py -m PyInstaller --onefile src\main.py -n ATNYCHI
```

### Go

```powershell
go build -o dist/ATNYCHI.exe ./cmd/atnychi
```

### Rust

```powershell
cargo build --release
copy .\target\release\atnychi.exe .\dist\ATNYCHI.exe
```

### .NET

```powershell
dotnet publish -c Release -r win-x64 --self-contained true `
  -p:PublishSingleFile=true -p:PublishTrimmed=true
```

## Signing and Integrity

```powershell
# Optional code signing if you own a certificate
signtool sign /tr http://timestamp.digicert.com /td SHA256 /fd SHA256 /a .\dist\ATNYCHI.exe

# Generate a reproducible checksum
Get-FileHash .\dist\ATNYCHI.exe -Algorithm SHA256 > ATNYCHI.sha256.txt
```

## Release Checklist

1. Ensure `dist/ATNYCHI.exe` and `ATNYCHI.sha256.txt` exist and are up to date.
2. Create a signed tag for the release:
   ```powershell
   git tag -s v0.1.0 -m "ATNYCHI v0.1.0"
   git push --tags
   ```
3. Create a GitHub Release attaching:
   - `ATNYCHI.exe`
   - `ATNYCHI.sha256.txt`
   - `LICENSE`
   - `README.md` (this document)
   - `SECURITY.md`
   - `RELEASES.md`

## Directory Structure

```
/dist          # Binary release artifacts (treated as binary via .gitattributes)
/src           # Language-specific sources (Python shown above)
/cmd           # Go entry point
/target        # Cargo release output (Rust)
```

Only `process_images.py` is included in this repository snapshot; the other
folders are referenced to document the expected release workflow.
