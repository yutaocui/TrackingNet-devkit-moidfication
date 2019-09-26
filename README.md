# TrackingNet-devkit

Development kit for the dataset **TrackingNet: A Large-Scale Dataset and
Benchmark for Object Tracking in the Wild**.

Compete in our benchmark by submitting your result on our [evaluation server](http://eval.tracking-net.org).

For more details, please refer to our [paper](https://ivul.kaust.edu.sa/Documents/Publications/2018/TrackingNet%20A%20Large%20Scale%20Dataset%20and%20Benchmark%20for%20Object%20Tracking%20in%20the%20Wild.pdf).

```
@InProceedings{Muller_2018_ECCV,
author = {Muller, Matthias and Bibi, Adel and Giancola, Silvio and Alsubaihi, Salman and Ghanem, Bernard},
title = {TrackingNet: A Large-Scale Dataset and Benchmark for Object Tracking in the Wild},
booktitle = {The European Conference on Computer Vision (ECCV)},
month = {September},
year = {2018}
}
```




# Structure of the dataset
There are 12 chunks of 2511 sequences for the training and 1 chunk of 511 sequences for the testing.

Each chunk have subfolders for the zipped sequence (`zips`), the unzipped frame (`frames`) and eventually the annotation (`anno`).

The structure of the dataset is the following:
```
TrackingNet
 - Test / Train_X (with X from 0 to 11)
   - zips
   - frames
   - anno (Test: annotation only for 1st frame)
```



# Create the environment

Tested on Ubuntu 16.04 LTS


 - Create the environment:

`conda env create -f environment.yml`

or (preferred for other platforms)

`conda create -n TrackingNet python=3 requests pandas tqdm numpy`

 - Activate the environment:

`source activate TrackingNet` (`activate TrackingNet` for windows platforms)



# Download the dataset

You can download the whole dataset by running:

`python download_TrackingNet.py --trackingnet_dir <trackingnet_dir>`

### Optional parameters:
  - `--trackingnet_dir`: path where to download the TrackingNet dataset
  - `--data` select the data to download (sequences: `--data zips` / annotations: `--data anno`)
  - `--chunk` select the chunk to download (testing set: `--chunk Test` / training set: `--chunk Train` / selected chunks: `--chunk 0,2,4,11`)
 
Please look at `python download_TrackingNet.py --help` for more details on the optional parameters.


### Disclaimer

In case an error such as `Permission denied: https://drive.google.com/uc?id=<ID>, Maybe you need to change permission over 'Anyone with the link'?` occurs, please check your internet connection and run again the script.
The script will not overwrite the previous sequences of videos if are already completely downloaded.

Note that Google Drive limits the download bandwidth to ~10TB/day. To ensure a good share between all users, avoid downloading the dataset several times and prefer sharing it with your colleagues using an old-fashion HDD.


# Unzip the frames

To extract all the zipped sequences for the complete dataset:

`python extract_frame.py --trackingnet_dir <trackingnet_dir>`

### Optional parameters:
  - `--trackingnet_dir`: path where to download the TrackingNet dataset
  - `--chunk`: select the chunk to download (testing set: `--chunk Test` / training set: `--chunk Train` / selected chunks: `--chunk 0,2,4,11`)
  
### Disclaimer
In this step, make sure you don't have any error message.
You can run this script several times to make sure all the files are properly extracted. 
By default, the unzipping script will not overwrite the frames that are properly extracted.

If any zip file is currupted, a error message will appear `Error: the zip file [zip_file_name] is corrupted`. 
In thas case, remove the corrupted zip file manually and run the download script again. 
By default, the download script will not overwrite the zip files already downloaded.
 


# (Optional) Generate Frames with the annotation boundingboxes

This part requires `opencv`: `conda install -c menpo opencv`

To generate the BB in the frames for the complete dataset:

`python generate_BB_frames.py --output_dir <trackingnet_dir>`

### Optional parameters:
  - `--output_dir`: path where to generate the images with boundingboxes
  - `--chunk` select the chunk to download (testing set: `--chunk Test` / training set: `--chunk Train` / selected chunks: `--chunk 0,2,4,11`)


# Evaluate the results of a tracker with a given ground truth

If you plan to submit results on our [evaluation server](http://eval.tracking-net.org), you may want to validate your results first.

The evaluation code we are using is available on `metrics.py`, whhich can be used as following:

`python metrics.py --GT_zip <GT.zip> --subm_zip <subm.zip>`

A dummy example of file is provided here:

`python metrics.py --GT_zip dummy_GT.zip --subm_zip dummy_subm.zip`




# $\color{red}{Complementary Functions are as follows:}$


## 1. Unzip the frames and record all the bad zips

`python process_bad_frame.py --tracking_dir=<TRACKINGNET_DATA_DIR> ---bad_zips_csv=<SAVE_BAD_ZIP_CSV_PATH> (default is 'bad_zips.csv')`

It will generate `bad_zips.csv` to record the bad zips in the following format:

`'trunk_name','zip_name','link','zip_path'`


## 2. Download the detected bad zips

`python download_bad_zips.py --tracking_dir=<NEW_ZIPS_DATA_DIR>`

It will download the zips in 'bad_zips.csv'.

## 3. Replace the bad zips

`python replace_bad_zips.py --old_trackingnet_dir=<TRACKINGNET_DATA_DIR> --new_zips_dir=<NEW_ZIPS_DATA_DIR> --bad_csv=<BAD_ZIP_CSV_PATH>`

Finally, you can just re-run process_bad_frame.py and set the param `overwrite_frames` to `False`.