import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "service_account.json",
    scope
)

client = gspread.authorize(creds)

sheet = client.open_by_key("1VWLCnQ5AHMS-WEDVWqDEsDSjb74ZryiUsWaMYcQYmok").worksheet("Population")

data = sheet.get_all_records(
    head=2   # 👈 tell gspread header row = Row 2
)

for row in data:
    print(row)