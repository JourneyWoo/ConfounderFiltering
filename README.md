# ChestX-ray-Prediction

Prediction on diseased chest based on the NIH dataset.

## Raw data source

This released dataset, chestX-ray, contains 14 kinds of chest diseases. 

Box: https://nihcc.app.box.com/v/ChestXray-NIHCC

`images` refers to the images (after downloading, you need to extract them first)

`Data_Entry_2017.csv` contains the necessary information related to this method, like the disease distribution

## Baselines

(Original paper of ChestX-ray is: http://openaccess.thecvf.com/content_cvpr_2017/papers/Wang_ChestX-ray8_Hospital-Scale_Chest_CVPR_2017_paper.pdf)

Three baselines (AlexNet, LeNet, VGG-16) can be found at `/models`

## Running `data_extract.py`

This method is to make the trainSet.tfrecords and testSet.tfrecords

    Python data_extract.py image_path csv_path train_test_choice dataset_choice

`image_path`: the path of your downloaded images

`csv_path`: the path of Data_Entry_2017.csv file

`train_test_choice`: if you plan to make trainSet, you need to set it as 1; if you plan to make testSet, you need to set it as 2

`dataset_choice`: if you don't plan to make the dataset with gender as label, you only need to leave it as 1; otherwise, you should set it as 2 

Output files( `train_test_choice` is 1 or 2, `dataset_choice` is 1):

a. tfrecord files (14 `diseaseName_train_healthyordisease.tfrecords` or 14 `diseaseName_test_healthyordisease.tfrecords`)

b. log file, which contains the disease name and the number of its diseased & healthy images. (`train_log.txt` or `test_log.txt`) 

## Running `model.py`
This method contains three baselines: AlexNet, LeNet, VGG-16

    Python modelName.py train_disease_images train_healthy_images train_disease_images test_healthy_images disease_name path
    

`train_disease_images`: (can be found in log file) The number of diseased images of the selected trainSet
`train_healthy_images`: (can be found in log file) The number of diseased images of the selected trainSet
`test_disease_images`: (can be found in log file) The number of healthy images of the selected testSet
`test_disease_images`: (can be found in log file) The number of healthy images of the selected testSet
`disease_name`: selected one disease from 14 kinds of diseases

`path`: the path of all the tfrecord datasets generated






