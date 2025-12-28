import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def export_to_google_sheets(df, sheet_name="Campus Connect Feedback"):

    creds = Credentials.from_service_account_file(
        "service_account.json",
        scopes=SCOPE
    )

    client = gspread.authorize(creds)

    # Create or open sheet
    try:
        sheet = client.open(sheet_name)
    except:
        sheet = client.create(sheet_name)

    worksheet = sheet.sheet1
    worksheet.clear()

    worksheet.update(
        [df.columns.values.tolist()] + df.values.tolist()
    )

    return sheet.url
