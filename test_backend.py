import engine #THIS IS JUST A TEST CODE IGNORE IF U DONT NEED IT#
import os

# 1. Setup session and index (do this once)
session_id = "biology_session_1"
print("Indexing documents in 'data/' folder...")
engine.process_and_index_pdfs("data", session_id)
print("Ready! You can now ask questions. (Type 'quit' to exit)")

# 2. Interactive Loop
while True:
    user_query = input("\nAsk a question about the papers: ")
    
    if user_query.lower() == 'quit':
        break
        
    print("Searching and thinking...")
    answer = engine.ask_agent(user_query, session_id)
    print(f"\n--- AI RESPONSE ---\n{answer}")
