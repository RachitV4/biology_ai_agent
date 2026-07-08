from pypdf import PdfReader

# We are telling the code: "Go to the 'data' folder and open 'test.pdf'"
file_path = "data/test.pdf"

# Initialize the reader
reader = PdfReader(file_path)

# Look at the first page
page = reader.pages[0]

# Extract the text from that page
text = page.extract_text()

# Print it
print(text)