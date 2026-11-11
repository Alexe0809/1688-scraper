from openpyxl import load_workbook
from pathlib import Path

def read_urls(excel_file : str):
    file_path = Path(excel_file)
    wb = load_workbook(file_path)
    source = wb.active
    url_rows = []
    for row in source.iter_rows(min_row = 2, min_col=1, max_col=1):
        if row[0].value is not None:
            url_rows.append(row[0].value)
    return url_rows


