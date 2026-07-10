import engine
import os

# 1. Setup
session_id = "test_session"
data_dir = "data"

# 2. Ensure data folder exists
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print("Created 'data' folder. Please put a PDF in there and run this again!")
    exit()

# 3. Run the Indexer
print("Starting indexing...")
status = engine.process_and_index_pdfs(data_dir, session_id)
print(status)

# 4. Run a Query
print("\nAsking the Agent...")
answer = engine.ask_agent("Summarize the main findings of the uploaded documents.", session_id)
print(f"\n--- AI ANSWER ---\n{answer}")