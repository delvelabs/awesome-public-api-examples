from datetime import datetime, timedelta
import os
import requests


ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")
API_BASE_URL = os.getenv("API_BASE_URL", "")

headers = dict(authorization=f"Bearer {ACCESS_TOKEN}", accept="application/json")

now = datetime.now()
start_date = (now - timedelta(days=30)).strftime("%s")
end_date = now.strftime("%s")

params = dict(team="1", tag="12", start_date=start_date, end_date=end_date)

response = requests.get(f"{API_BASE_URL}/metrics/health-score",
                        params=params,
                        headers=headers,
                        verify=False)
response.raise_for_status()

series = response.json().get("health").get("series")
timestamp = next(entry.get("data") for entry in series if entry.get("label") == "timestamp")
values = next(entry.get("data") for entry in series if entry.get("label") == "health")

print(f"Current Health Score: {values[-1]}")
print(f"Current Health Score Variation: {values[-1] - values[0]}")
