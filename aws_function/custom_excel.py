from openpyxl import load_workbook
from io import BytesIO


def modify_worksheet(file_content, modifications):
    # Load the workbook from the file content
    workbook = load_workbook(filename=BytesIO(file_content))
    sheet = workbook.active

    # Apply modifications
    for cell, value in modifications.items():
        sheet[cell] = value

    # Save the modified workbook to a BytesIO object
    modified_workbook = BytesIO()
    workbook.save(modified_workbook)
    modified_workbook.seek(0)

    return modified_workbook.read()
