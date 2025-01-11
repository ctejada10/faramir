import unittest
import os
from src.main import main

class TestFaramir(unittest.TestCase):
    def setUp(self):
        # Create test environment
        self.test_image_folder = "test_images"
        self.test_csv = "test_metadata.csv"
        os.makedirs(self.test_image_folder, exist_ok=True)

        # Create dummy files
        for i in range(1, 4):
            with open(f"{self.test_image_folder}/image_{i}.jpg", "w") as f:
                f.write("")

        # Create dummy CSV
        with open(self.test_csv, "w") as f:
            f.write("Frame,Aperture,Shutter,ISO,Film,Date,Latitude,Longitude ")
            f.write("1,2.8,¹⁄₁₀₀₀,200,Kodak Gold 200,01/01/2025,40.7128,-74.0060 ")
            f.write("2,4.0,¹⁄₅₀₀,400,Kodak Portra 400,01/02/2025,34.0522,-118.2437 ")

    def tearDown(self):
        # Clean up test environment
        if os.path.exists(self.test_image_folder):
            for file in os.listdir(self.test_image_folder):
                os.remove(os.path.join(self.test_image_folder, file))
            os.rmdir(self.test_image_folder)
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)

    def test_main_function(self):
        try:
            # Run the main function
            main(self.test_image_folder, self.test_csv)
            self.assertTrue(True, "Main function executed without error.")
        except Exception as e:
            self.fail(f"Main function raised an exception: {e}")

    def test_file_renaming(self):
        # Run the main function
        main(self.test_image_folder, self.test_csv)

        # Check that files are renamed correctly
        renamed_files = os.listdir(self.test_image_folder)
        expected_files = [
            "Kodak_Gold_200_test_location_2025_R01_F01.jpg",
            "Kodak_Portra_400_test_location_2025_R01_F02.jpg",
        ]
        self.assertTrue(
            all(any(renamed_file.startswith(expected) for renamed_file in renamed_files) for expected in expected_files),
            "Files were not renamed correctly."
        )

if __name__ == "__main__":
    unittest.main()
