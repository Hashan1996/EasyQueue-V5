
import requests

url = 'http://localhost:5000/results'
r = requests.post(url, json={'Year': 2019, 'Month': 1, 'Week': 1, 'weekdayInt': 2,
                             'TimeRangeInt': 1})

print(r.json())
