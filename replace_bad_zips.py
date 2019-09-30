import os
import pandas as pd
from tqdm import tqdm
import argparse
import csv,shutil

import downloader

def main(old_trackingnet_dir="TrackingNet", new_tracking_dir='', bad_csv="bad_zips.csv", chunks=[], data=["ANNO","ZIPS"]):
    """
    bad_zips.csv saves the bad zips of TrackingNet dataset in the following format：
         trunk_name,zip_name,link,zip_path
    """
    csv_file = bad_csv
    df = pd.read_csv(csv_file)
    for index, row in tqdm(df.iterrows(), desc="Replace bad zips", total=len(df.index)):
        file_name = row["zip_name"]
        chunk_folder = row['trunk_name']
        old_zip_path = os.path.join(old_trackingnet_dir, chunk_folder, "zips", file_name)
        new_zip_path = os.path.join(new_tracking_dir, chunk_folder, "zips", file_name)
        #frames_path = os.path.join(trackingnet_dir, chunk_folder, "zips", Google_drive_file_name)

        if os.path.exists(old_zip_path):
            os.remove(old_zip_path)
        shutil.copy(new_zip_path, old_zip_path)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description='Download the frames for TrackingNet')
    p.add_argument('--old_trackingnet_dir', type=str, default='TrackingNet')
    p.add_argument('--new_zips_dir', type=str, default='TrackingNet')
    p.add_argument('--chunk', type=str, default="ALL",
        help='List of chunks to elaborate [ALL / Train / Test / 4 / 1,2,5].')
    p.add_argument('--data', type=str, default="zips",
        help='Type of data [ALL / zips / anno / zips,anno].')
    p.add_argument('--bad_csv', type=str, default='bad_zips.csv')

    args = p.parse_args()

    # type of data to download (zips/anno)
    try:
        if ("ALL" in args.data.upper()):
            args.data = ["ANNO","ZIPS"]
        else:
            args.data = args.data.upper().split(",")
    except:
        args.data = []

    # chunk of data to download (Test/Train_i)
    try:
        if ("ALL" in args.chunk.upper()):
            args.chunk = ["TRAIN_"+str(c) for c in range(12)]
            args.chunk.insert(0, "TEST")
        elif ("TEST" in args.chunk.upper()):
            args.chunk = ["TEST"]
        elif ("TRAIN" in args.chunk.upper()):
            args.chunk = ["TRAIN_"+str(c) for c in range(12)]
        else :
            args.chunk = ["TRAIN_"+str(int(c)) for c in args.chunk.split(",")]
    except:
        args.chunk = []


    print("Downloading the data files for the following chunks")
    print("CHUNKS:", args.chunk)
    print("DATA:", args.data)

    main(old_trackingnet_dir=args.trackingnet_dir,
         new_tracking_dir=args.new_zips_dir,
         bad_csv=args.bad_csv,
         chunks=args.chunk,
         data=args.data)
