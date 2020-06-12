from datetime import date, timedelta
import json
import os
import requests


ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")
API_BASE_URL = os.getenv("API_BASE_URL", "")

TEAM_ID = 1
TAG_ID = 12
START_DATE = date.today() - timedelta(days=30)
END_DATE = date.today()

headers = {
        "authorization": f"Bearer {ACCESS_TOKEN}",
    "accept": "application/json",
    "accept-language": "fr"
}
query = {
    "bool": {
        "must": [
            {"team": {"id": f"{TEAM_ID}"}},
            {"tag": {"id": f"{TAG_ID}"}},
        ],
        "should": [
            {"first_discovery_date": {"gte": START_DATE.isoformat()}},
            {"last_seen_date": {"lte":  END_DATE.isoformat()}},
        ]
    }
}
params = dict(q=json.dumps(query), limit=0, offset=0)
response = requests.get(f"{API_BASE_URL}/vulnerability-groups/distribution",
                        params=params,
                        headers=headers,
                        verify=False)
response.raise_for_status()

series = dict(
    base=response.json().get("scoreStepBase").get("series"),
    final=response.json().get("scoreStepFinal").get("series"),
)
values = dict(
    base=next(x.get("data") for x in series.get("base") if x.get("label") == "count"),
    final=next(x.get("data") for x in series.get("final") if x.get("label") == "count")
)

print("Score Distribution Base:")
print([(k, v) for k, v in enumerate(values.get("base"))])

print("\nScore Distribution Final:")
print([(k, v) for k, v in enumerate(values.get("final"))])
