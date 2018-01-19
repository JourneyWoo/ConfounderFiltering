# ChestX-ray-Prediction

## Raw data source
Box: https://nihcc.app.box.com/v/ChestXray-NIHCC

`images` refers to the images (after doenloading, you need to extract them first)

`Data_Entry_2017.csv` contains the necessray information related to this method, like the disease distribution

## Baselines
(Original paper of ChestX-ray is: http://openaccess.thecvf.com/content_cvpr_2017/papers/Wang_ChestX-ray8_Hospital-Scale_Chest_CVPR_2017_paper.pdf)

Three baselines (AlexNet, LeNet, VGG) can be found at `/models`

## Running `data_extract.py`
This method is to make the train and test datasets as the tfrecord format

    Python image_path csv_path train_test_choice dataset_choice

`image_path`: the path of your downloaded images

`csv_path`: the path of your downloaded Data_Entry_2017.csv file

`train_test_choice`: if you make train set, you need to set it as 1; if you make test set, you need to set it as 2

`dataset_choice`: if you don't plan to make the dataset with gender as label, you only need to leave it as 1; otherwise, you should set it as 2 

Output files:

a. tfrecord files

b. corresponding log file, which contains the disease name and the number of its images.







