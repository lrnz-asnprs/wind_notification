import requests
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Initialize logfile
import logging
import logging.handlers
import os

# Logfile
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

# What you wanna know
variables = 'WindSpeed'

# Sydvestpynten
lat = '55.5633'
lon = '12.5636'

# Return timeseries data
url = f"https://api.fcoo.dk/metoc/v2/data/timeseries?variables=WindSpeed,Wind&lat={lat}&lon={lon}"

# Make the API call
response = requests.get(url)

# Check the response status code
if response.status_code == 200:
    # API call successful
    data = response.json()
else:
    # API call failed
    logger.info(f'API Error: {response.status_code}')

# Data
windspeed_data = data['WindSpeed']['windspeed']['data']
windspeed_timestamps = data['WindSpeed']['windspeed']['time']

# Put it in dataframe
df = pd.DataFrame({'timestamp':windspeed_timestamps, 'windspeed': windspeed_data, 'lat': lat, 'lon': lon})

df['timestamp'] = pd.to_datetime(df['timestamp'])

def extract_date_info(date):
    hour = date.hour
    day = date.strftime('%A')
    month = date.month
    return pd.Series([hour, day, month])

# Extract info
df[['hour', 'day', 'month']] = df['timestamp'].apply(extract_date_info)

df['rolling_3h_average'] = df['windspeed'].rolling(window=3).mean().values

# Send mail with image 

subject = "SEEEEEEND IT!!!"
sender = "windfinder2300@gmail.com"
recipient = "la.aisenpreis@gmail.com"
password = "ntxjglvotfzgbkgb" # make this more secure

def send_email_image(body: str):
    
    with open('send_it.jpeg', 'rb') as f:
        image_part = MIMEImage(f.read())
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = recipient
    html_part = MIMEText(body)
    message.attach(html_part)
    message.attach(image_part)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, password)
    server.sendmail(sender, recipient, message.as_string())
    server.quit()

# Return 3h windows, where wind is on average above X m/s
threshold = 8
min_hour = 10 # starts at 7:00 because of moving average
max_hour = 20 # starts at 17:00 because of moving average

results = df[(df['rolling_3h_average'] > threshold) & (df['hour'] >= min_hour) & (df['hour'] <= max_hour)]

# If forecast already made for one day, then not send email again
blocked_days = set()

for row in results.iterrows(): 

    avg_windspeed = row[1][7]
    end_hour = row[1][4]
    start_hour = end_hour - 3
    day = row[1][5]
    month = row[1][6]

    if day not in blocked_days:
        email_body = f"It's GONNA GET WINDY! There will be an average windspeed of {avg_windspeed:.2f} m/s from {start_hour}:00 to {end_hour}:00 on {day}!"
        
        # Send email
        send_email_image(body=email_body)

        logger.info(f'Email sent. For forecast of average windspeed of {avg_windspeed:.2f} m/s from {start_hour}:00 to {end_hour}:00 on {day}.')
        # Don't send any more emails for this day
        blocked_days.add(day)
    else:
        continue




