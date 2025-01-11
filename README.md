# Faramir 🎞️

### Overview
Faramir is a tool designed for analog photographers who digitize their work. It helps you enrich your scanned film photos with accurate EXIF metadata, preserving details like aperture, shutter speed, ISO, GPS, and even the film stock used.

### Why Use This?
When scanning film, metadata often gets lost in the digital process. Using apps like [Émulsion](https://emulsionapp.com/) on your iPhone, you can log metadata during shooting. Faramir takes that CSV and applies the metadata directly to your scans, making your digital archives more informative and complete.

### Features
- Add metadata like aperture, shutter speed, ISO, GPS, and more.
- Rename files based on film stock, location, and roll/frame numbers.
- Simple integration for scanned images.

### Installation
```bash
pip install -r requirements.txt
```

### Usage
```bash
python src/main.py /path/to/images /path/to/metadata.csv --reverse
```

### Testing
Run tests with:
```bash
python -m unittest discover
```

### Example
Input your metadata via Émulsion, export the CSV, and pass it to Faramir to enhance your film scans!

### Contribution
Feel free to fork and improve the project!

---
Developed by someone passionate about analog photography. ☀️
