# OpenWeather_ETL_Airflow

## Background 

![image](https://github.com/AaronChen589/OpenWeather_ETL_Airflow/assets/80292924/3b4d251f-a449-4464-9642-e1bacf7e1eb0) ![image](https://github.com/AaronChen589/OpenWeather_ETL_Airflow/assets/80292924/4ee62a8a-f3c2-4f1a-8f59-f5ff5bd468d8) ![image](https://github.com/AaronChen589/OpenWeather_ETL_Airflow/assets/80292924/642800e6-fbd6-4b7e-b882-2d0ad1298169)

Curious about the weather condition in your city? How about the last time it snowed? Better yet, when will it snow in the future?

These questions can be tackled through the continious collection of data over a long period of time, for which insights and predictions can be properly made.

Hence, this project attempts to automate this Extract. Load. Transform. pipeline process using Apache Airflow, Python and AWS EC2 and S3 and the Open Weather API.



## Installing
* Windows 11
* Vscode IDE (Python + SSH extensions are also required)
* Access to an AWS account
  - EC2 instance (small instance type is recommended for apache airflow)
  - S3 bucket

## Setting Up EC2 Linux Instance
1) Once you create an EC2 instance, make sure to properly update the linux with the following commands...
- sudo apt update
- sudo apt install python3-pip
- sudo apt install python3.10-venv
- sudo apt install pandas
- sudo pip install s3fs
- sudo pip install apache-airflow
- airflow standalone

## Setting Up S3 bucket
- Make sure to allow EC2 to access S3's bucket when configuring

- 









