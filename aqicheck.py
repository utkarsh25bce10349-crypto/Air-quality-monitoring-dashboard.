import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

API_TOKEN = "3c4cc31b6d8d36a6fe192e9bbc28882d052" #personalised api token taken individually 

def get_current_aqi(city):
    url = f"http://api.waqi.info/feed/{city}/?token={API_TOKEN}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'ok':
        aqi = data['data']['aqi']
        print(f"Current AQI for {city} is {aqi}")
        return data['data']
    else:
        print(f"Error fetching current AQI for {city}: {data['data']}")
        return None

def fetch_pm25_history(city):
    
    url = f"http://api.waqi.info/feed/{city}/?token={API_TOKEN}"
    response = requests.get(url)
    data = response.json()
    if data['status'] != 'ok':
        print("Error fetching PM2.5 history")
        return [], []



    times = []
    values = []

    
    pm25_value = data['data'].get('iaqi', {}).get('pm25', {}).get('v')
    if pm25_value is None:
        print("PM2.5 data not available")
        return [], []

    now = datetime.utcnow()
    for i in range(3):
        day = now - timedelta(days=i)
        times.append(day)
        values.append(pm25_value)  # Simulated constant value

    times.reverse()
    values.reverse()
    return times, values

def plot_pm25(times, values, city):
    if not times or not values:
        print("No PM2.5 data to plot")
        return
    plt.plot(times, values, marker='o')
    plt.title(f"Simulated PM2.5 AQI in {city} (Last 3 Days)")
    plt.xlabel("Date (UTC)")
    plt.ylabel("PM2.5 AQI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    city = input("Enter your city name: ")
    current_data = get_current_aqi(city)
    if current_data is None:
        return

    times, values = fetch_pm25_history(city)
    plot_pm25(times, values, city)

if __name__ == "__main__":
    main()