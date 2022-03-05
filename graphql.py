import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

API_Key = "NRAK-XXXXXXXXXXXXXXXXXXXXXXXXXXX"

endpoint = "https://api.newrelic.com/graphql"
headers = {"API-Key": f"{API_Key}", "Content-Type": "application/json"}

apm_query = """query GetSpans {
  actor {
    account(id: 1234567) {
      nrql(query: "SELECT timestamp, duration, request.uri from Transaction WHERE appName = 'FlaskApp - Heroku (APM)' SINCE 24 HOURS AGO LIMIT MAX") {
        results
      }
    }
  }
}
"""
r = requests.post(endpoint, json={"query": apm_query}, headers=headers)

if r.status_code == 200:
  df = pd.json_normalize(data=r.json()["data"]["actor"]["account"]["nrql"],record_path=["results"])
  #df.head()
else:
  raise Exception(f"Query failed to run with a {r.status_code}.")

# Convert UNIX epoch time to YYYY-MM-DD HH:mm:ss AM/PM and convert timezone as needed
df.sort_values(by=["timestamp"], inplace=True)
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
df["timestamp"] = df["timestamp"].dt.tz_localize("Etc/GMT+2").dt.tz_convert("America/Toronto").dt.strftime(date_format = "%I:%M:%S %p")
#df.head()

# Plot the counts.
plt.style.use("dark_background")
fig, ax = plt.subplots()
ax.scatter(pd.to_datetime(df["timestamp"]), 1000*df[(df["request.uri"]=="/ping")]["duration"], c="red", s=2, label="/ping")

# Format plot.
plt.title("New Relic GraphQL Example", fontsize=16)
plt.xlabel("Timestamp", fontsize=12)
fig.autofmt_xdate()
xfmt = mdates.DateFormatter('%I:%M %p')
ax.xaxis.set_major_formatter(xfmt)
plt.ylabel("Seconds", fontsize=12)
plt.tick_params(axis="both", which="major", labelsize=16)
ax.set_ylim(bottom=0)

# Add legend.
ax.legend(loc="upper right", frameon=True)

# Fix trimming issue with output chart
plt.tight_layout()

plt.savefig("nr1_graphql.png", dpi=150)
plt.show()
