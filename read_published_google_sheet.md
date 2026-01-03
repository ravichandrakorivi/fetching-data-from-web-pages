# Fetching Real Time Data from Web Pages
## If the sheet can be public read-only

You can ask the owner to Publish the sheet as CSV:

`Google Sheet → File → Share → Publish to web → Select sheet → Format: CSV`

You’ll get a link like:

`https://docs.google.com/spreadsheets/d/.../pub?output=csv`


```
import requests
import csv
from io import StringIO

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vScat5grOFnwqnQAqLV9iRuPAArTkXKYyzBrFXiQhEU1nUtdNHBJc-GyIr9lHGEDYdTEilOa1h6czaN/pub?gid=0&single=true&output=csv"

response = requests.get(url)

reader = csv.reader(StringIO(response.text))

for row in reader:
    print(row)
```