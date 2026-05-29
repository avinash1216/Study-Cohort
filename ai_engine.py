# ai_engine.py
import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"

def analyze_match(user_profile, candidate_profile):
    
    user_name = user_profile.get('name', 'Learner A')
    cand_name = candidate_profile.get('name', 'Learner B')

    prompt = f"""
You are an expert EdTech networking copilot. Your job is to build study cohorts by matching people with complementary skills and learning goals.
Analyze these two learners:

{user_name} (The Learner):
- Role: {user_profile.get('role', 'Attendee')}
- Skills they have: {', '.join(user_profile.get('skills_have', []))}
- What they want to learn: {', '.join(user_profile.get('learning_goals', []))}
- Career Goals: {user_profile.get('goals', '')}

{cand_name} (The Candidate):
- Role: {candidate_profile.get('role', 'Attendee')}
- Skills they have: {', '.join(candidate_profile.get('skills_have', []))}
- What they want to learn: {', '.join(candidate_profile.get('learning_goals', []))}
- Career Goals: {candidate_profile.get('goals', '')}

Output EXACTLY a raw JSON object with these keys (no extra text or markdown blocks):
{{
  "score": <an integer between 1 and 100 based on how well {user_name}'s skills match {cand_name}'s learning goals and vice versa>,
  "reason": "<one sentence explaining why {user_name} and {cand_name} form a good study cohort>",
  "learn_from_each_other": "<one sentence stating exactly what {user_name} can teach {cand_name}, and what {cand_name} can teach {user_name}>",
  "suggested_course_project": "<suggest a specific capstone project or high-level course topic {user_name} and {cand_name} should tackle together>",
  "icebreaker": "<a casual, punchy, single-sentence technical conversation starter for {user_name} to send to {cand_name}>"
}}
"""

    payload = {
        "model": "gemma4:e2b", # Change to gemma2:2b if that's your exact tag
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.2 # Kept low for strict JSON compliance
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        print(f"Ollama response status: {response.status_code}")
        try:
            print(f"Ollama response JSON keys: {list(response.json().keys())}")
            print(f"Ollama response JSON: {response.json()}")
        except Exception as je:
            print(f"Failed to decode response as JSON: {je}. Raw content: {response.text}")
        raw_text = response.json().get("response", "").strip()
        
        # Use regex to find the first curly-braced object block in case of conversational wrapper text
        match = re.search(r"(\{.*\})", raw_text, re.DOTALL)
        if match:
            raw_text = match.group(1)

        return json.loads(raw_text)

    except Exception as e:
        print(f"Error parsing JSON: {e}")
        try:
            print(f"Raw text received from LLM was:\n{raw_text}")
        except NameError:
            print("Could not retrieve raw text (request failed).")
        return {
            "score": 50,
            "reason": "Could not compute exact match.",
            "learn_from_each_other": "You have complementary technical backgrounds.",
            "suggested_course_project": "Build a basic full-stack web application.",
            "icebreaker": f"Hey {candidate_profile['name']}, want to team up and learn together?"
        }