import os
import pandas as pd

# Define the function to parse filenames from files
def parse_filenames_from_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        lines = content.splitlines()
        return [(os.path.splitext(line)[0], os.path.splitext(line)[1]) for line in lines]

# Define the function to parse PDF filenames from nested files
def parse_pdf_filenames(directory_path):
    pdf_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

# Parse filenames from files and store in a pandas data frame
file_path = '/path/to/filename_file.txt'
filenames = parse_filenames_from_file(file_path)
df_filenames = pd.DataFrame(filenames, columns=['filename', 'extension'])

# Parse PDF filenames from nested files and store in a pandas data frame
directory_path = '/path/to/pdf_files_directory'
pdf_filenames = parse_pdf_filenames(directory_path)
df_pdfs = pd.DataFrame(columns=['filename', 'data'])
for pdf_filename in pdf_filenames:
    with open(pdf_filename, 'rb') as f:
        pdf_data = f.read()
        df_pdfs = df_pdfs.append({'filename': os.path.basename(pdf_filename), 'data': pdf_data}, ignore_index=True)

# Merge the two data frames and do any necessary processing
df = pd.merge(df_filenames, df_pdfs, on='filename')

# Save the data frame to a CSV file
df.to_csv('output_file.csv', index=False)
