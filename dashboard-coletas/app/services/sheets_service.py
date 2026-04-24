import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from app.config import GOOGLE_CREDENTIALS_PATH, SPREADSHEET_ID, WORKSHEET_NAME

class SheetsService:
    
    def __init__(self):
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        self.creds = Credentials.from_service_account_file(
            GOOGLE_CREDENTIALS_PATH, 
            scopes=self.scope
        )
        self.client = gspread.authorize(self.creds)

    def get_data(self):
        # try:
            sheet = self.client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)
            data = sheet.get_all_records(numericise_ignore=["all"])
            return pd.DataFrame(data)
        # except Exception as e:
            # print(f"Error fetching data from Google Sheets: {e}")
            # return pd.DataFrame()