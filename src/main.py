import logging
from datetime import datetime
from glob import glob
import pandas as pd
import piexif
import os

# Set logging level to WARNING by default to reduce verbosity
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.WARNING,  # Default level set to WARNING
)


def _rename_scan(image_path, film_stock, location, season_year, roll_number, frame_number):
    base_dir = os.path.dirname(image_path)
    extension = os.path.splitext(image_path)[1]
    new_name = f"{film_stock}_{location}_{season_year}_{roll_number}_{frame_number}{extension}"
    new_path = os.path.join(base_dir, new_name)
    os.rename(image_path, new_path)
    logging.debug(f"Renamed: {image_path} -> {new_name}")
    return new_path


def _add_exif(image_path: str, tags):
    try:
        exif_dict = {
            "Exif": {},
            "0th": {},
            "GPS": {},
            "1st": {},
            "Interop": {},
        }

        if pd.notna(tags.Aperture):
            exif_dict["Exif"][piexif.ExifIFD.FNumber] = (int(tags.Aperture * 100), 100)

        if pd.notna(tags.Shutter):
            shutter_value = _parse_shutter(tags.Shutter)
            if shutter_value:
                exif_dict["Exif"][piexif.ExifIFD.ExposureTime] = shutter_value

        if pd.notna(tags["Focal Length"]):
            exif_dict["Exif"][piexif.ExifIFD.FocalLength] = (int(tags["Focal Length"]), 1)

        if pd.notna(tags.Date):
            exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = datetime.strptime(
                tags.Date, "%m/%d/%Y, %I:%M %p"
            ).strftime("%Y:%m:%d %H:%M:%S")

        if pd.notna(tags.Latitude) and pd.notna(tags.Longitude):
            exif_dict["GPS"] = {
                piexif.GPSIFD.GPSLatitude: _convert_to_dms(tags.Latitude),
                piexif.GPSIFD.GPSLatitudeRef: b"N" if tags.Latitude >= 0 else b"S",
                piexif.GPSIFD.GPSLongitude: _convert_to_dms(tags.Longitude),
                piexif.GPSIFD.GPSLongitudeRef: b"E" if tags.Longitude >= 0 else b"W",
            }

        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)
        logging.debug(f"Added EXIF metadata to {image_path}")

    except Exception as e:
        logging.error(f"Error adding EXIF metadata to {image_path}: {e}")


def _parse_shutter(shutter_value):
    try:
        shutter_value = (
            shutter_value.replace("¹⁄", "1/").replace("₁", "1").replace("₂", "2")
            .replace("₃", "3").replace("₄", "4").replace("₅", "5")
            .replace("₆", "6").replace("₇", "7").replace("₈", "8")
            .replace("₉", "9").replace("₀", "0")
        )
        numerator, denominator = map(int, shutter_value.split("/"))
        return numerator, denominator
    except Exception:
        logging.warning(f"Invalid shutter value: {shutter_value}")
        return None


def _convert_to_dms(value):
    degrees = int(abs(value))
    minutes = int((abs(value) - degrees) * 60)
    seconds = int(((abs(value) - degrees) * 60 - minutes) * 60 * 100)
    return (degrees, 1), (minutes, 1), (seconds, 100)


def _extract_parameters_from_path(folder_path):
    try:
        parts = folder_path.strip(os.sep).split(os.sep)
        logging.debug(f"Extracted parts: {parts}")
        film_stock = parts[-2]
        location_season = parts[-1]
        location, season_year = location_season.split(" - ")
        return film_stock, location, season_year
    except ValueError as e:
        logging.error(f"Error extracting parameters from path: {folder_path}")
        raise e


def main(image_folder_path: str, image_info_path: str, *, reverse: bool = False):
    """
    Add EXIF metadata to scanned film photos and rename files.

    :param image_folder_path: Path to the folder containing image files.
    :param image_info_path: Path to the CSV file containing image metadata.
    :param reverse: Process images in descending order of filenames (optional flag).
    """
    try:
        # Convert relative paths to absolute paths
        image_folder_path = os.path.abspath(image_folder_path)
        image_info_path = os.path.abspath(image_info_path)
        
        logging.info(f"Reverse mode: {reverse}")
        film_stock, location, season_year = _extract_parameters_from_path(image_folder_path)

        info = pd.read_csv(image_info_path)
        logging.info(f"Loaded {len(info)} rows from the CSV file.")

        required_columns = {"Frame", "Aperture", "Shutter", "Focal Length", "Date", "Latitude", "Longitude"}
        if not required_columns.issubset(info.columns):
            raise ValueError(f"CSV must contain the columns: {required_columns}")

        image_paths = sorted(glob(f"{image_folder_path}/*.jpg"), reverse=reverse)
        logging.info(f"Found {len(image_paths)} images in the folder.")

        # Handle mismatch of image count and metadata count
        min_count = min(len(image_paths), len(info))
        logging.info(f"Processing {min_count} images and metadata rows.")
        
        # If more images than metadata, log the discrepancy
        if len(image_paths) > len(info):
            logging.warning(f"There are {len(image_paths) - len(info)} more images than metadata, skipping extra images.")

        renamed_files = []
        exif_success = []

        for idx, image_path in enumerate(image_paths, start=1):
            logging.debug(f"Processing image {idx}: {image_path}")

            roll_number = f"R01"
            frame_number = f"F{idx:02d}"

            # Rename the image
            new_path = _rename_scan(
                image_path, film_stock, location, season_year, roll_number, frame_number
            )
            renamed_files.append(new_path)

            # Add EXIF metadata only if metadata exists
            if idx <= len(info):
                image_info = info.iloc[idx - 1]  # We ensure that we only access up to `min_count` indices
                logging.debug(f"Metadata for image {idx}: {image_info}")
                _add_exif(new_path, image_info)
                exif_success.append(new_path)

        logging.info(f"Renamed {len(renamed_files)} images.")
        logging.info(f"Successfully added/updated EXIF metadata for {len(exif_success)} images.")

    except Exception as e:
        logging.error(f"Error in main: {e}")
