import pdfx
import os

filename = 'filename.txt'
def get_file_contents(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)
file_name = get_file_contents(filename)

pdf = pdfx.PDFx(file_name)

metadata = pdf.get_metadata()

# references_list = pdf.get_references()

# print(references_list)

references_dict = pdf.get_references_as_dict()

# print()

lines = references_dict['pdf']

with open("output.txt", "w") as file:
    # Write each line to the file
    for line in lines:
        file.write(line + "\n")

