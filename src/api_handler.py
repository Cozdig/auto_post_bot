import os.path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
sheet_id = os.getenv("google_sheets_id")
RANGE = "Релиз!A2:E"
range_links = "Релиз!D2:D"
creds = service_account.Credentials.from_service_account_file(
    "credentials.json", scopes=SCOPES
)

service = build("sheets", "v4", credentials=creds)


def get_hyperlinks():
    result = (
        service.spreadsheets()
        .get(spreadsheetId=sheet_id, ranges=[range_links], includeGridData=True)
        .execute()
    )

    sheets = result.get("sheets", [])
    row_dict = {}

    for sheet in sheets:
        for grid_data in sheet.get("data", []):
            row_data = grid_data.get("rowData", [])

            for row_index, row in enumerate(row_data):
                values = row.get("values", [])
                if not values:
                    row_dict[row_index + 2] = []
                    continue
                else:
                    cell_d = values[0]

                    cell_text = cell_d.get("formattedValue", "").replace(" ", "")
                    hyperlink = None

                    if "hyperlink" in cell_d:
                        hyperlink = cell_d["hyperlink"]
                        text = cell_d.get('userEnteredValue').get('stringValue')
                    elif "richTextValue" in cell_d:
                        for text_run in cell_d["richTextValue"].get("runs", []):
                            if "hyperlink" in text_run:
                                hyperlink = text_run["hyperlink"]
                                break
                    if cell_text[0] == "@":
                        row_dict[row_index + 2] = cell_text
                    else:
                        row_dict[row_index + 2] = [hyperlink, text]
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
    if not values:
        return {}, 0
    row_dict = {}
    row_index = 2
    for row in values:
        if len(row) < 5:
            row_dict[row_index] = row
            row_index += 1
        else:
            row[3] = hyperlinks.get(row_index)
            row_dict[row_index] = row
            row_index += 1
    last_row = list(row_dict.keys())[-1]
    return row_dict, last_row
