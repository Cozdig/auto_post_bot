import os.path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
sheet_id = os.getenv("google_sheets_id")
RANGE = "A2:F"
creds = service_account.Credentials.from_service_account_file(
    "credentials.json", scopes=SCOPES
)

service = build("sheets", "v4", credentials=creds)


def get_hyperlinks():
    result = (
        service.spreadsheets()
        .get(spreadsheetId=sheet_id, ranges=[RANGE], includeGridData=True)
        .execute()
    )

    sheets = result.get("sheets", [])

    row_dict = {}

    for sheet in sheets:
        for grid_data in sheet.get("data", []):
            row_data = grid_data.get("rowData", [])

            for row_index, row in enumerate(row_data):
                values = row.get("values", [])
                cell_b = values[1]

                cell_text = cell_b.get("formattedValue", "").replace(" ", "")
                hyperlink = None

                if "hyperlink" in cell_b:
                    hyperlink = cell_b["hyperlink"]
                elif "richTextValue" in cell_b:
                    for text_run in cell_b["richTextValue"].get("runs", []):
                        if "hyperlink" in text_run:
                            hyperlink = text_run["hyperlink"]
                            break
                if cell_text[0] == "@":
                    row_dict[row_index + 2] = cell_text
                else:
                    row_dict[row_index + 2] = hyperlink

    return row_dict


def get_info():
    hyperlinks = get_hyperlinks()
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=sheet_id, range=RANGE)
        .execute()
    )
    values = result.get("values", [])
    row_dict = {}
    row_index = 2
    for row in values:
        row[1] = hyperlinks.get(row_index)
        row_dict[row_index] = row
        row_index += 1
    last_row = list(row_dict.keys())[-1]
    return row_dict, last_row


if __name__ == "__main__":
    get_info()
