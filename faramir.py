from glob import glob

import numpy as np
import pandas as pd
from clize import run
from exif import Image
from datetime import datetime


def _update_image_tags (image_path : str, tags):
	i = Image(image_path)

	i.aperture = tags.Aperture
	i.shutter_speed_value = tags.Shutter
	i.focal_length_in_35mm_film = tags[5]
	i.datetime = datetime.strptime(tags.Date, '%m/%d/%y %I:%M %p')
	i.gps_latitude = tags.Longitude
	i.gps_longitude = tags.Latitude

def main(image_folder_path : str, image_info_path : str):
	info = pd.read_csv(image_info_path, delimiter=',')
	image_paths = glob(image_folder_path)

	if len(info) != len(image_paths):
		return -1
	
	for image_path, image_info in zip (image_paths, info.itertuples()):
		_update_image_tags(image_path, image_info)