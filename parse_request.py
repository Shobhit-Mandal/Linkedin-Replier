from bs4 import BeautifulSoup
import json

# Load the JSON file and extract HTML
file_path = r"C:\Users\ADMIN\Downloads\linkedin replier\file.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract HTML content from the "html" field
raw_html = data[0]["html"] if data and "html" in data[0] else ""

print(f"[DEBUG] Raw HTML length: {len(raw_html)}")

# Parse HTML
soup = BeautifulSoup(raw_html, "html.parser")

# Find all <tr> tags (each row likely has one Q and one A)
rows = soup.find_all("tr")

qna_pairs = []

for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 2:
        question = cols[0].get_text(strip=True)
        answer = cols[1].get_text(strip=True)
        if question and answer:
            qna_pairs.append({
                "question": question,
                "answer": answer
            })

# Output
import sys
sys.stdout.reconfigure(encoding='utf-8')  # Add this line before any print

print(json.dumps(qna_pairs, indent=2, ensure_ascii=False))
