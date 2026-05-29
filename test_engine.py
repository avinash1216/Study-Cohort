# test_engine.py
import json
from ai_engine import analyze_match
from mock_data import ATTENDEES

user = ATTENDEES[3]       # Sneha (Data Engineer)
candidate = ATTENDEES[1]  # Priya (ML Engineer)

print(f"Testing match between {user['name']} and {candidate['name']}...")
result = analyze_match(user, candidate)
print(json.dumps(result, indent=2))