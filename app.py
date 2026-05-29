# app.py
import streamlit as st
from mock_data import ATTENDEES
from ai_engine import analyze_match

st.set_page_config(page_title="Cohort Builder Agent", page_icon="🎓", layout="wide")

st.title("🎓 Peer-to-Peer Cohort Builder")
st.markdown("### Find your perfect study partner and build together.")

# ==========================================
# SIDEBAR: USER PROFILE SELECTION
# ==========================================
st.sidebar.header("Your Profile")
user_names = [a["name"] for a in ATTENDEES]
selected_name = st.sidebar.selectbox("Select your profile:", user_names)
current_user = next(item for item in ATTENDEES if item["name"] == selected_name)

st.sidebar.divider()
st.sidebar.subheader("Current Stats:")
st.sidebar.write(f"**Role:** {current_user.get('role', 'Attendee')}")
st.sidebar.write(f"**I know:** {', '.join(current_user.get('skills_have', current_user.get('skills', [])))}")
st.sidebar.write(f"**I want to learn:** {', '.join(current_user.get('learning_goals', current_user.get('interests', [])))}")

st.write("Ready to upskill? Let's find attendees who can teach you what you need, and who need what you know.")

# ==========================================
# MAIN LOGIC: FILTER & MATCH
# ==========================================
if st.button("🔍 Find My Study Cohort", type="primary"):
    
    candidates = [a for a in ATTENDEES if a["id"] != current_user["id"]]
    
    # ---------------------------------------------------------
    # STEP 1: FAST PYTHON PRE-FILTER (The Optimization)
    # ---------------------------------------------------------
    my_bar = st.progress(10, text="Running lightning-fast heuristic filter...")
    
    # Safely get the skills and goals, defaulting to empty lists if keys are missing
    user_needs = set(current_user.get('learning_goals', []))
    user_has = set(current_user.get('skills_have', []))
    
    for candidate in candidates:
        cand_needs = set(candidate.get('learning_goals', []))
        cand_has = set(candidate.get('skills_have', []))
        
        # Calculate overlap: What user can teach + What user can learn
        user_can_teach = len(user_has.intersection(cand_needs))
        user_can_learn = len(user_needs.intersection(cand_has))
        
        # Assign a basic math score to rank them before hitting the LLM
        candidate['heuristic_score'] = user_can_teach + user_can_learn

    # Sort purely by the fast math and grab ONLY the top 2 candidates to save time
    candidates.sort(key=lambda x: x.get('heuristic_score', 0), reverse=True)
    top_candidates = candidates[:2] 
    
    # ---------------------------------------------------------
    # STEP 2: AI REASONING ENGINE (Targeted Gemma Calls)
    # ---------------------------------------------------------
    match_results = []
    
    for i, candidate in enumerate(top_candidates):
        with st.spinner(f"Generating AI insights for top match: {candidate['name']}..."):
            
            # Send only the highly probable matches to Gemma
            result = analyze_match(current_user, candidate)
            result["name"] = candidate["name"]
            result["role"] = candidate["role"]
            match_results.append(result)
            
        # Update progress bar smoothly based on the number of AI calls
        my_bar.progress(50 + int((i + 1) / len(top_candidates) * 50), text="Extracting learning plans...")
        
    my_bar.empty()
    
    # Sort the final UI output by the score Gemma assigned
    match_results.sort(key=lambda x: int(x.get("score", 0)), reverse=True)
    
    # ---------------------------------------------------------
    # STEP 3: RENDER UI CARDS
    # ---------------------------------------------------------
    st.divider()
    st.subheader("🎯 Your Recommended Study Partners")
    
    for match in match_results:
        score = match.get("score", 0)
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.metric(label="Synergy Score", value=f"{score}%")
            
        with col2:
            st.markdown(f"### {match['name']} | {match['role']}")
            st.info(f"**Why partner up:** {match.get('reason', 'Great mutual learning opportunity.')}")
            
            # Using an expander for the deep dive educational content
            with st.expander("📚 View Cohort Learning Plan", expanded=True):
                st.write(f"**Knowledge Exchange:** {match.get('learn_from_each_other', '')}")
                st.write(f"**Suggested Project/Course:** {match.get('suggested_course_project', '')}")
                
            st.success(f"**Icebreaker:** {match.get('icebreaker', 'Hey, want to build something together?')}")
            
        st.divider()