# Faramir 🎞️

### Overview
Faramir is a tool designed for analog photographers who digitize their work. It helps you enrich your scanned film photos with accurate EXIF metadata, preserving details like aperture, shutter speed, focal length, the date and GPS, and naming each file after its film stock.

### Why Use This?
When scanning film, metadata often gets lost in the digital process. Using apps like [Émulsion](https://emulsionapp.com/) on your iPhone, you can log metadata during shooting. Faramir takes that CSV and applies the metadata directly to your scans, making your digital archives more informative and complete.

### Features
- Add aperture, shutter speed, focal length, date taken and GPS to each scan's EXIF.
- Rename files based on film stock, location, and roll/frame numbers.
- Simple integration for scanned images.

### Installation
Faramir uses [uv](https://docs.astral.sh/uv/):
```bash
uv sync
```

### Usage
```bash
uv run faramir.py "/path/to/Kodak Gold 200/Brooklyn - Fall 2024" /path/to/metadata.csv
```
- The image folder must sit at `<film stock>/<location> - <season year>`. Faramir reads all three from the path.
- The CSV is Émulsion's export. It needs the columns `Frame`, `Aperture`, `Shutter`, `Focal Length`, `Date` (as `MM/DD/YYYY, HH:MM AM`), `Latitude` and `Longitude`.
- Images are matched to rows in filename order. Add `--reverse` if your scans run from the last frame to the first.
- Each `.jpg` is renamed to `<film stock>_<location>_<season year>_R01_F<frame>.jpg`.
- Faramir exits with an error if the folder or the CSV doesn't match this layout.

### Testing
```bash
uv run pytest
```

### Example
Input your metadata via Émulsion, export the CSV, and pass it to Faramir to enhance your film scans!

### Contribution
Feel free to fork and improve the project!

---
Developed by someone passionate about analog photography. ☀️
