import os
from tqdm import tqdm
import zipfile
import argparse
import shutil
import pandas as pd
import csv


def main(trackingnet_dir="TrackingNet", overwrite_frames=False, chunks=[], csv_dir='', bad_zips_csv=''):

	bad_zips_header = ['trunk_name','zip_name','link','zip_path']
	bad_zips = []
	bad_num = 0

	for chunk_folder in chunks:
		chunk_folder = chunk_folder.upper()
		zip_folder = os.path.join(trackingnet_dir, chunk_folder, "zips")

		if( os.path.exists(zip_folder)):

			for zip_file in tqdm(os.listdir(zip_folder), desc=chunk_folder):
				if (zip_file.endswith('.zip')):

					frame_folder = os.path.join(trackingnet_dir, chunk_folder, "frames", os.path.splitext(zip_file)[0])

					try:
						with zipfile.ZipFile(os.path.join(zip_folder, zip_file)) as zip_ref:
							
							# create frame folder if does not exist already
							if (os.path.exists(frame_folder)):

								# Check if there is the same number of files within the folder
								same_number_files = len(zip_ref.infolist()) == len(os.listdir(frame_folder))
															
								if (overwrite_frames or not same_number_files):
									shutil.rmtree(frame_folder)
									#print("overwriting", frame_folder, "due to different number of file in the folder.")
									os.makedirs(frame_folder)

							# if frame folder does not exist, jsut create it
							else:	
								same_number_files = False				
								os.makedirs(frame_folder)

							# extract zip if necessary
							if(overwrite_frames or not same_number_files):
								zip_ref.extractall(os.path.join(frame_folder))

							# check that all the files were extracted
							same_number_files = len(zip_ref.infolist()) == len(os.listdir(frame_folder))
							if (not same_number_files):
								print("Warning:", frame_folder, "was not well extracted")


					except zipfile.BadZipFile:

						"""
						bad_zips.csv saves the bad zips of TrackingNet dataset in the following format：
							trunk_name,zip_name,link,zip_path
						"""
						bad_num += 1
						flag = 0
						csv_file = os.path.join(csv_dir, chunk_folder + "_ZIPS.csv")

						df = pd.read_csv(csv_file)
						for index, row in tqdm(df.iterrows(), desc='Search ' + chunk_folder, total=len(df.index)):
							if zip_file == row["name"]:
								flag = 1
								bad_zip = [chunk_folder, zip_file, row["link"],
										   os.path.join(trackingnet_dir, chunk_folder, "zips", zip_file)]
								print("Record bad zip：{} done！".format(bad_zip))
								print("Error: the zip file", zip_file, "is corrupted, please delete it and download it again.")
								break
						if not flag:
							raise Exception("Error occurs when search bad zip-{}.".format(zip_file))
						bad_zips.append(bad_zip)

	print("Total number of the bad zips is {}".format(bad_num))
	with open(bad_zips_csv, 'w', newline='') as csvfile:
		csv_writer = csv.writer(csvfile, delimiter=',')
		csv_writer.writerow(bad_zips_header)
		csv_writer.writerows(bad_zips)


if __name__ == "__main__": 
	p = argparse.ArgumentParser(description='Extract the frames for TrackingNet')
	p.add_argument('--trackingnet_dir', type=str, default='TrackingNet',
		help='Main TrackingNet folder.')
	p.add_argument('--overwrite_frames', action='store_true', default=True,
		help='Folder where to store the frames.')
	p.add_argument('--chunk', type=str, default="ALL",
		help='List of chunks to elaborate [ALL / Train / Test / 4 / 1,2,5].')
	p.add_argument('--csv_dir', type=str, default='csv_link',
				   help='Folder where the csv with the list of frames are. [default=csv_link]')
	p.add_argument('--bad_zips_csv', type=str, default='bad_zips.csv')

	args = p.parse_args()

	try:		
		if ("ALL" in args.chunk.upper()):
			chunk = ["TRAIN_"+str(c) for c in range(12)]
			chunk.insert(0, "TEST")		
		elif ("TEST" in args.chunk.upper()):
			chunk = ["TEST"]
		elif ("TRAIN" in args.chunk.upper()):
			chunk = ["TRAIN_"+str(c) for c in range(12)]
		else :
			chunk = ["TRAIN_"+str(int(c)) for c in args.chunk.split(",")]		
	except:		
		chunk = []


	print("extracting the frames for the following chunks:")
	print(chunk)

	main(args.trackingnet_dir, args.overwrite_frames, chunk, args.csv_dir, args.bad_zips_csv)


