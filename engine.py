from pypdf import PdfReader

# 1. Define the file path
file_path = "data/sample_biology.pdf"

# 2. Create the reader object
reader = PdfReader(file_path)

# 3. Access the first page
page = reader.pages[0]

# 4. CRITICAL: Use .extract_text() to decode the binary into readable words
text = page.extract_text()

# 5. Print the decoded text
print(text)