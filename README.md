# OpenWeather_ETL_Airflow

## Background 

![image](https://github.com/AaronChen589/OpenWeather_ETL_Airflow/assets/80292924/3b4d251f-a449-4464-9642-e1bacf7e1eb0) ![image](https://github.com/AaronChen589/OpenWeather_ETL_Airflow/assets/80292924/4ee62a8a-f3c2-4f1a-8f59-f5ff5bd468d8) ![image](https://github.com/AaronChen589/OpenWeather_ETL_Airflow/assets/80292924/642800e6-fbd6-4b7e-b882-2d0ad1298169)

Curious about the weather condition in your city? How about the last time it snowed? Better yet, when will it snow in the future?

These questions can be tackled through the continious collection of data over a long period of time, for which insights and predictions can be properly made.

Hence, this project attempts to automate this Extract. Load. Transform. pipeline process by first using Python to extract weather data from the Open Weather API and transforming it into usable csv data files to be placed in the s3 bucket. Apache Airflow will be used to orchestrated this process, making sure daily weather data are being collected.


## Requirements
* Windows 11
* Vscode IDE (Python + SSH extensions are also required)
* Access to an AWS account
  - EC2 instance (small instance type is recommended for apache airflow)
  - S3 bucket (For storing the weather data)

## Connect To the EC2 via AWS Dashboard and Setting Up the Linux Terminal
1) Log into AWS and navigate to the EC2 dashboard to create the instance
![image](https://github.com/AaronChen589/OpenWeather_ETL_Airflow/assets/80292924/cc6e1b3f-b884-4ec5-8056-e777a902eeee)

2) Once created, we can access the EC2 linux terminal as shown in the picture
![image](https://github.com/AaronChen589/OpenWeather_ETL_Airflow/assets/80292924/de5d5f32-f9dd-416d-b870-4bf4e9d73d31)
![image](https://github.com/AaronChen589/OpenWeather_ETL_Airflow/assets/80292924/bbd62e0f-5ede-409e-bbec-192603a7137c)

 Make sure to download the dependencies within the EC2 linux with the following commands...
- sudo apt update
- sudo apt install python3-pip
- sudo apt install python3.10-venv
- sudo apt install pandas
- sudo pip install s3fs
- sudo pip install apache-airflow


## Accessing Apache Airflow UI
- Make sure to in an virtual environment within the EC2 linux terminal
- type the command "airflow standalone" into the terminal to download the dependencies
- Log into the Airflow User Interface by typing the EC2 instance IPV4 DNS:Port into the web browser
![image](https://github.com/AaronChen589/OpenWeather_ETL_Airflow/assets/80292924/2ff4be3f-27db-422c-9d26-bfdb1e54f9b1)
- On first entry, sign in with the credentials given during the first activation of airflow standalone
Note: Port depends on the security group defined within the EC2 instance and can be manually changed within the EC2 dashboard

## Setting Up S3 bucket
- Make sure to allow EC2 to access S3's bucket when configuring the bucket

## How the Pipeline Works
- With everything set up, we can create our own Dag python file in the EC2 Linux. (e.g. weather_dags.py)
![image](https://github.com/AaronChen589/OpenWeather_ETL_Airflow/assets/80292924/250f3569-0918-4e0b-a370-b8e0363c09e8)

- is_weather_api_ready checks to see if the Open Weather API is callable
- extract_weather_data checks to see if is_weather_api_ready was successfully exceuted and if so, will call the API again to store the weather data into a JSON file
- transform_load_weather_data checks to see if extract_weather_data was successfully executed and if so, will transform data from the JSON file into a panda dataframe and finally export it as an a csv file into the S3 bucket.





