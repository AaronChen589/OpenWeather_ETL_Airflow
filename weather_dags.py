from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import json
import pandas as pd


def kelvin_to_fahrienhiet(K):
        F = (K - 273.15) * 1.8 + 32
        return round(F, 2)

def transform_load_data(task_instance, city):

    # Pull the data from the previous task, where we called the API 
    data = task_instance.xcom_pull(task_ids=f'extract_weather_data_{city.replace(" ", "_")}')


    # Extract information 
    city = data['name']
    weather = data['weather'][0]['main']
    weather_desc = data['weather'][0]['description']
    latitude = data['coord']['lat']
    longitude = data['coord']['lon']
    temp_F = kelvin_to_fahrienhiet(data['main']['temp'])
    temp_min_F = kelvin_to_fahrienhiet(data['main']['temp_min'])
    temp_max_F = kelvin_to_fahrienhiet(data['main']['temp_max'])
    humidity= data['main']['humidity'] # %
    pressure = data['main']['pressure'] # hPa
    wind_speed = data['wind']['speed'] # meter/sec
    time_of_recording = datetime.utcfromtimestamp(data['dt'])  
    time_of_sunrise = datetime.utcfromtimestamp(data['sys']['sunrise'])
    time_of_sunset = datetime.utcfromtimestamp(data['sys']['sunset'])

    # Adjust time based on the timezone offset
    local_time_of_recording = time_of_recording + timedelta(seconds= data['timezone']) 
    local_sunrise = time_of_sunrise +  timedelta(seconds= data['timezone']) 
    local_sunset = time_of_sunset + timedelta(seconds= data['timezone']) 

    # Put the extracted information into a dictionary 
    cols = {
            "City": city,
            "Weather":weather,
            "Description":weather_desc,
            "Latitude":latitude,
            "Longitude":longitude,
            "Temperature(F)":temp_F,
            "Minimum Temperature(F)":temp_min_F,
            "Maximum Temperature(F)":temp_max_F,
            "Humidity(%)":humidity,
            "Pressure(hPa)":pressure,
            "Wind Speed(m/s)":wind_speed,
            "Time of Record":local_time_of_recording,
            "Time of Sunrise":local_sunrise,
            "Time of Sunset":local_sunset,
        }

    # Place extracted data (from dictionary) into panda dataframe 
    transformed_data_list = [cols]
    df = pd.DataFrame(transformed_data_list)

    # Rename the file to include current date 
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H%M%S")
    dt_string = 'current_weather_data_' + dt_string

    # save as csv file to the s3 bucket
    df.to_csv(f"s3://weatherapi-airflow-bucket/{dt_string}_{city}.csv", index = False)

# Set arguments for how the DAG should run
default_arg = {
            'owner':'airflow',
            'depend_on_past':False,
            'start_date':datetime(2024, 3, 26),
            'email':['aaronchen589@gmail.com'],
            'email_on_failure':False,
            'email_on_retry':False,
            'retries':2,
            'retry_delay': timedelta(minutes=2)
            }

# Cities we want to collect info on
cities = ['New York', 'Beijing', 'France']

with DAG('weather_dags', default_args=default_arg, schedule_interval='@daily', catchup=False) as dag:

    for city in cities:
         # Checks to see if the open weather api is reachable before moving to next task
        task_id = f'extract_weather_data_{city.replace(" ", "_")}'
        is_weather_api_ready = HttpSensor(
            task_id=f'is_weather_api_ready_{city.replace(" ", "_")}',
            http_conn_id='weathermap_api',
            endpoint=f'/data/2.5/weather?q={city}&appid=API_KEY'  
        )
        # Extracts data of the city from the open weather api
        extract_weather_data = SimpleHttpOperator(
            task_id=task_id,
            http_conn_id='weathermap_api',
            endpoint=f'/data/2.5/weather?q={city}&appid=API_KEY',
            method='GET',
            response_filter=lambda r: json.loads(r.text),
            log_response=True
        )
        # Call the python function to transform and load the city's data into s3 bucket
        transform_load_weather_data = PythonOperator(
            task_id=f"transform_load_weather_data_{city.replace(' ', '_')}",
            python_callable=transform_load_data,
            op_kwargs={'city':city}
        )
        is_weather_api_ready >> extract_weather_data >> transform_load_weather_data

