# Documentation for Faramir

## Overview
Faramir is a Python tool for adding EXIF metadata to digitized film photos. It helps analog photographers preserve essential information about their images, such as aperture, shutter speed, ISO, GPS, and film stock.

## How It Works
- Use the Émulsion app on your iPhone to capture metadata while shooting film.
- Export the metadata as a CSV file.
- Run Faramir to apply this metadata to your scanned film images.

## Key Features
1. **EXIF Metadata Injection**:
    - Adds metadata like aperture, shutter speed, ISO, GPS coordinates, and the date/time of the photo.
    - Supports adding custom fields like film stock.

2. **File Renaming**:
    - Renames images based on a naming scheme: `{Film Stock}_{Location}_{Year}_{Roll}_{Frame}`.

## Example Workflow
1. Log metadata in Émulsion while shooting film.
2. Scan your negatives and organize them in a folder.
3. Run the tool:
    ```bash
    python src/main.py /path/to/images /path/to/metadata.csv
    ```
4. Inspect the enriched images using tools like Preview, Finder, or ExifTool.

## Testing
Tests are included to ensure basic functionality:
- Verifies that the tool runs without errors.
- Ensures images are renamed correctly.

Run tests using:
```bash
python -m unittest discover
```

## Limitations
- Ensure your CSV metadata matches the expected format.
- EXIF data injection works best with JPG images.

## Contribution
Feel free to contribute by improving functionality or fixing bugs. Fork the repository and submit a pull request!

## Support
For questions or issues, please contact the developer.
