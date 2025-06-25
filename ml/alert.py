import requests
import datetime


def trigger_alarm():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {"timestamp": timestamp}
    response = requests.get("http://localhost:8000/health", json=data)
    if response.status_code == 200:
        print("Everything is fine at", timestamp)
    else:
        print(f"Inference failed at, {timestamp} because {response.text}")     

if __name__ == "__main__":
    trigger_alarm()
    
    