import piexif
import pytest

from src.main import _convert_to_dms, _parse_shutter, main

# Smallest JPEG piexif accepts: SOI, a JFIF APP0 segment, an empty scan, EOI.
JPEG = bytes.fromhex("FFD8FFE000104A46494600010100000100010000FFDA0008010100003F0000FFD9")

CSV = (
    "Frame,Aperture,Shutter,Focal Length,Date,Latitude,Longitude\n"
    '1,2.8,¹⁄₁₀₀₀,50,"01/01/2025, 10:30 AM",40.7128,-74.0060\n'
    '2,4.0,¹⁄₅₀₀,35,"01/02/2025, 03:15 PM",34.0522,-118.2437\n'
)


@pytest.fixture
def roll(tmp_path):
    folder = tmp_path / "Kodak Gold 200" / "Brooklyn - Fall 2024"
    folder.mkdir(parents=True)
    for i in (1, 2):
        (folder / f"scan_{i}.jpg").write_bytes(JPEG)
    csv = tmp_path / "metadata.csv"
    csv.write_text(CSV, encoding="utf-8")
    return folder, csv


def test_renames_by_stock_location_and_frame(roll):
    folder, csv = roll
    main(str(folder), str(csv))
    assert sorted(p.name for p in folder.iterdir()) == [
        "Kodak Gold 200_Brooklyn_Fall 2024_R01_F01.jpg",
        "Kodak Gold 200_Brooklyn_Fall 2024_R01_F02.jpg",
    ]


def test_writes_exif_from_the_csv(roll):
    folder, csv = roll
    main(str(folder), str(csv))
    exif = piexif.load(str(folder / "Kodak Gold 200_Brooklyn_Fall 2024_R01_F01.jpg"))
    assert exif["Exif"][piexif.ExifIFD.FNumber] == (280, 100)
    assert exif["Exif"][piexif.ExifIFD.ExposureTime] == (1, 1000)
    assert exif["Exif"][piexif.ExifIFD.FocalLength] == (50, 1)
    assert exif["Exif"][piexif.ExifIFD.DateTimeOriginal] == b"2025:01:01 10:30:00"
    assert exif["GPS"][piexif.GPSIFD.GPSLatitudeRef] == b"N"
    assert exif["GPS"][piexif.GPSIFD.GPSLongitudeRef] == b"W"


def test_reverse_matches_rows_from_the_last_scan(roll):
    folder, csv = roll
    main(str(folder), str(csv), reverse=True)
    # scan_2 is processed first, so it becomes frame 1 with the first row's focal length.
    exif = piexif.load(str(folder / "Kodak Gold 200_Brooklyn_Fall 2024_R01_F01.jpg"))
    assert exif["Exif"][piexif.ExifIFD.FocalLength] == (50, 1)
    assert not (folder / "scan_2.jpg").exists()


def test_folder_outside_the_layout_raises(tmp_path, roll):
    _, csv = roll
    folder = tmp_path / "scans"
    folder.mkdir()
    with pytest.raises(ValueError):
        main(str(folder), str(csv))


def test_csv_missing_columns_raises(roll, tmp_path):
    folder, _ = roll
    csv = tmp_path / "short.csv"
    csv.write_text("Frame,Aperture\n1,2.8\n", encoding="utf-8")
    with pytest.raises(ValueError, match="CSV must contain"):
        main(str(folder), str(csv))


@pytest.mark.parametrize(
    ("value", "expected"),
    [("¹⁄₁₀₀₀", (1, 1000)), ("¹⁄₆₀", (1, 60)), ("1/250", (1, 250)), ("bulb", None)],
)
def test_parse_shutter(value, expected):
    assert _parse_shutter(value) == expected


def test_convert_to_dms():
    assert _convert_to_dms(40.5) == ((40, 1), (30, 1), (0, 100))
    assert _convert_to_dms(-74.25) == ((74, 1), (15, 1), (0, 100))
