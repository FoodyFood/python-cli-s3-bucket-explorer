# Python S3 Bucket Explorer

This is a comand line interface written in python that allows browsing of an AWS S3 bucket. It can download files, or even entire folders.

## Configuration

In the top of the [script](./main.py) you need to point it at the aws profile and bucket you want to explore.

```python
bucket_name = '<bucket name>'
aws_profile = '<aws profile name>'
```

## Running The Code

```bash
python3 ./main.py
```

## Interface

After running the script you will see the files in the main directory of the bucket

![After Starting](./docs/browser-main.jpg)

Once you select a folder you will get a prompt ask ing what you would like to do

![After Selection](./docs/after-folder-selection.jpg)

You can select a single file to download and it will download into the currect direcory

![Select Single File](./docs/select-single-file.jpg)

If you want to download the whole folder, it will tell you how many files there are and prompt for confirmation before downloading

The files will be downlaoded into a folder of the same name as the last one selected in the bucket

![Download Whole Folder](./docs/download-whole-folder.jpg)

