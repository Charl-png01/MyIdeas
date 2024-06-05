import PyPDF2
import openpyxl
import docx
import json
import csv
import pygeoip
import warnings

def printRecord(ip):
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    rec = gi.record_by_name(ip)
    city = rec['city']
    country = rec['country_name']
    longitude = rec['longitude']
    lat = rec['latitude']

def extract_metadata(file_path):
    if file_path.lower().endswith('.pdf'):
        try:
            with open(file_path, 'rb') as file:
                pdf_file = PyPDF2.PdfFileReader(file)
                data = pdf_file.getDocumentInfo()

                print("----Metadata of the PDF file----")
                for metadata in data:
                    print(f"{metadata}: {data[metadata]}")
        except PyPDF2.utils.PdfReadError:
            print("Error: The provided file is not a valid PDF.")
    elif file_path.lower().endswith(('.xlsx', '.xlsm', '.xls')):
        try:
            workbook = openpyxl.load_workbook(file_path)
            properties = workbook.properties
            print("----Metadata of the Excel file----")
            print(f"Title: {properties.title}")
            print(f"Author: {properties.author}")
            print(f"Last Modified By: {properties.lastModifiedBy}")
            print(f"GeoInfo:+ printRecord(ip)" )

        except openpyxl.utils.exceptions.InvalidFileException:
            print("Error: The provided file is not a valid Excel file.")
    elif file_path.lower().endswith('.docx'):
        try:
            doc = docx.Document(file_path)
            print("----Metadata of the Word file----")
            print(f"Title: {doc.core_properties.title}")
            print(f"Author: {doc.core_properties.author}")
            print(f"Last Modified By: {doc.core_properties.last_modified_by}")
        except Exception:
            print("Error: The provided file is not a valid Word file.")
    elif file_path.lower().endswith('.json'):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                print("----Metadata of the JSON file----")
                for key, value in data.items():
                    print(f"{key}: {value}")
        except json.JSONDecodeError:
            print("Error: The provided file is not a valid JSON file.")
    elif file_path.lower().endswith('.csv'):
        try:
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)
                print("----Metadata of the CSV file----")
                print(f"Header: {header}")
        except csv.Error:
            print("Error: The provided file is not a valid CSV file.")
    else:
        print("Metadata extraction is not supported for this file type.")

def main():
    # Prompt the user to upload a file
    filename = input("Upload file: ")

    # Extract metadata based on file type
    extract_metadata(filename)

if __name__ == '__main__':
    main()

