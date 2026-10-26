# Documentation for Faramir

## Overview
Faramir is a Python tool for adding EXIF metadata to digitized film photos. It helps analog photographers preserve essential information about their images, such as aperture, shutter speed, focal length, the date taken and GPS. The film stock goes into each file's name.

## How It Works
- Use the Émulsion app on your iPhone to capture metadata while shooting film.
- Export the metadata as a CSV file.
- Run Faramir to apply this metadata to your scanned film images.

## Key Features
1. **EXIF Metadata Injection**:
    - Adds aperture, shutter speed, focal length, GPS coordinates and the date and time of the photo.

2. **File Renaming**:
    - Renames images based on a naming scheme: `{Film Stock}_{Location}_{Season Year}_R01_F{Frame}`, reading the film stock, location and season from the folder path `<film stock>/<location> - <season year>`.

## Example Workflow
1. Log metadata in Émulsion while shooting film.
2. Scan your negatives into a folder at `<film stock>/<location> - <season year>`.
3. Run the tool:
    ```bash
    uv run faramir.py "/path/to/Kodak Gold 200/Brooklyn - Fall 2024" /path/to/metadata.csv
    ```
4. Inspect the enriched images using tools like Preview, Finder, or ExifTool.

## Testing
Tests are included to ensure basic functionality:
- Renaming, EXIF writing and GPS conversion on a small generated JPEG.
- Errors for a folder or CSV that doesn't match the expected layout.

Run tests using:
```bash
uv run pytest
```

## Limitations
- Ensure your CSV metadata matches the expected format.
- EXIF data injection works best with JPG images.

## Contribution
Feel free to contribute by improving functionality or fixing bugs. Fork the repository and submit a pull request!

## Support
For questions or issues, please contact the developer.
