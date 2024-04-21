# Import the necessary libraries for this project.
import requests
import boto3
import json
import datetime as dt

# Set the variables to add to the API call.
# Please input your OpenWeather API Key in WEATHER_API_KEY
WEATHER_API_KEY = ""
UNITS = "metric"
CITY = "Manila"

# Set the URL to fetch API data from OpenWeather.
URL = "https://api.openweathermap.org/data/2.5/weather?" + \
    "appid=" + WEATHER_API_KEY + \
    "&q=" + CITY + \
    "&units=" + UNITS

# Get weather data with requests and the URL with the OpenWeather API
response = requests.get(URL)

# Set AWS Access Credentials.
# Kindly ensure that there is an existing bucket to upload OpenWeather Data. Enter the name of the bucket in S3_BUCKET.
ACCESS_KEY = ""
SECRET_KEY = ""
S3_BUCKET = ""

# Set the connection to AWS S3.
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# Prepare the data to be uploaded in S3.
response_s3_upload = json.loads(response.text)

# Get the UTC datetime when this script is run.
# NOTE: It can be argued that we can set the timezone here in Manila time, but storing the data as raw as possible is the best setup.
# If other cities are included for weather tracking, it will be easy to join the datetime schedules since everything was downloaded in UTC.
datetime_now_str = str(dt.datetime.now())

# Set the path inside S3 that will be used to store the data uploaded.
s3_path = 'openweather/manila' + datetime_now_str

# Upload the data in S3.
s3.put_object(Body=json.dumps(response_s3_upload), Bucket=S3_BUCKET, Key=s3_path, ContentType='application/json')