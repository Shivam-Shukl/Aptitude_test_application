import streamlit as st
import google.generativeai as genai
import json
import time
import re
import os
from datetime import datetime, timedelta
import asyncio
from typing import Dict, List, Tuple

# Configure Streamlit page
st.set_page_config(
    page_title="AI Aptitude Test",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure Google Gemini API
GEMINI_API_KEY = None

# Try to get API key from multiple sources
try:
    # First try Streamlit secrets
    GEMINI_API_KEY = st.secrets['GEMINI_API_KEY']
except:
    try:
        # Then try environment variable
        GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    except:
        pass

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    st.error("🔑 Gemini API Key not found!")
    st.markdown("""
    ### How to get a FREE Gemini API Key:
    
    **Step 1: Get your FREE API Key**
    1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
    2. Click "Create API key"
    3. Copy your API key
    
    **Step 2: Configure the API Key**
    
    **Option 1: Using Streamlit Secrets (Recommended)**
    1. Create a folder named `.streamlit` in your project directory
    2. Create a file named `secrets.toml` inside the `.streamlit` folder
    3. Add this line to `secrets.toml`: `GEMINI_API_KEY = "your_api_key_here"`
    
    **Option 2: Using Environment Variable**
    1. Set an environment variable: `GEMINI_API_KEY=your_api_key_here`
    
    **Option 3: Temporary Input (Not recommended for production)**
    """)
    
    # Temporary input option for testing
    with st.expander("🔧 Temporary API Key Input (for testing only)"):
        temp_api_key = st.text_input("Enter your Gemini API Key:", type="password")
        if temp_api_key:
            genai.configure(api_key=temp_api_key)
            st.success("API Key configured! Please refresh the page.")
            st.stop()
    
    st.info("💡 **FREE TIER INFO**: Google provides free access to Gemini models through their API with generous rate limits for testing and development!")
    st.stop()

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []
if 'test_started' not in st.session_state:
    st.session_state.test_started = False
if 'test_completed' not in st.session_state:
    st.session_state.test_completed = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = None
if 'selected_difficulty' not in st.session_state:
    st.session_state.selected_difficulty = None
if 'show_review' not in st.session_state:
    st.session_state.show_review = False
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = 'gemini-1.5-flash'

class QuestionGenerator:
    def __init__(self, model_name='gemini-1.5-flash'):
        # Updated model names that work with current API
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)

    def generate_question(self, topic: str, difficulty: str) -> Dict:
        prompt = f"""
        Generate a {difficulty} level aptitude question on {topic}.
        Please format your response as a JSON object with the following structure:
        {{
            "question": "The question text here",
            "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
            "correct_answer": "A",
            "explanation": "Step-by-step solution explanation",
            "topic": "{topic}",
            "difficulty": "{difficulty}"
        }}
        Make sure the question is clear, the options are distinct, and the explanation is comprehensive.
        Only return the JSON object, no additional text.
        """
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up the response text
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
            
            question_data = json.loads(response_text)
            return question_data
        except Exception as e:
            st.error(f"Error generating question: {str(e)}")
            return None

    def generate_test(self, topic: str, difficulty: str, num_questions: int = 20) -> List[Dict]:
        questions = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(num_questions):
            status_text.text(f'Generating question {i+1} of {num_questions}...')
            question = self.generate_question(topic, difficulty)
            if question:
                questions.append(question)
            progress_bar.progress((i + 1) / num_questions)
            time.sleep(0.5)  # Delay to avoid rate limiting
        
        progress_bar.empty()
        status_text.empty()
        return questions

def display_topic_selection():
    """Display topic and difficulty selection interface"""
    st.title("🧠 AI Aptitude Test Generator")
    st.success("🎉 Using FREE Gemini API!")
    st.markdown("---")
    
    # Model selection
    st.subheader("🤖 Select AI Model")
    model_options = {
        'gemini-1.5-flash': '⚡ Gemini 1.5 Flash (Fast & Free)',
        'gemini-1.5-pro': '🎯 Gemini 1.5 Pro (Advanced & Free)',
        'gemini-2.5-flash': '🚀 Gemini 2.5 Flash (Latest)',
    }
    
    selected_model = st.selectbox(
        "Choose AI model",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        index=0
    )
    st.session_state.selected_model = selected_model
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Select Topic")
        topics = [
            "Quantitative Aptitude",
            "Logical Reasoning",
            "Verbal Ability",
            "Data Interpretation",
            "General Awareness",
            "Programming Logic",
            "Mathematics",
            "English Grammar",
            "Analytical Reasoning",
            "Numerical Ability"
        ]
        selected_topic = st.selectbox(
            "Choose a topic",
            topics,
            index=0
        )
    
    with col2:
        st.subheader("⚡ Select Difficulty")
        difficulties = ["Easy", "Medium", "Hard"]
        selected_difficulty = st.selectbox(
            "Choose difficulty level",
            difficulties,
            index=1
        )
    
    # Free tier information
    with st.expander("💰 Free Tier Information"):
        st.markdown("""
        **Google Gemini API - FREE Tier Benefits:**
        - ✅ Completely free for Google AI Studio usage
        - ✅ Generous rate limits for testing and development
        - ✅ Access to latest Gemini 1.5 Flash and Pro models
        - ✅ 1M+ token context window
        - ✅ No credit card required for basic usage
        
        **Rate Limits (Free Tier):**
        - Gemini 1.5 Flash: 15 requests per minute
        - Gemini 1.5 Pro: 2 requests per minute
        
        Perfect for educational projects and testing!
        """)
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Test (20 Questions)", type="primary", use_container_width=True):
            st.session_state.selected_topic = selected_topic
            st.session_state.selected_difficulty = selected_difficulty
            generate_test()

def generate_test():
    """Generate the test questions"""
    with st.spinner("Generating your personalized test..."):
        generator = QuestionGenerator(st.session_state.selected_model)
        questions = generator.generate_test(
            st.session_state.selected_topic,
            st.session_state.selected_difficulty,
            20
        )
        
        if questions:
            st.session_state.questions = questions
            st.session_state.test_started = True
            st.session_state.current_question = 0
            st.session_state.user_answers = [None] * len(questions)
            st.session_state.start_time = datetime.now()
            st.session_state.show_review = False
            st.rerun()
        else:
            st.error("Failed to generate questions. Please try again.")

def display_question():
    """Display current question with timer"""
    if not st.session_state.questions:
        return
    
    current_q = st.session_state.current_question
    question_data = st.session_state.questions[current_q]
    
    # Timer display
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.start_time:
            elapsed = datetime.now() - st.session_state.start_time
            remaining = timedelta(minutes=30) - elapsed
            if remaining.total_seconds() > 0:
                mins, secs = divmod(int(remaining.total_seconds()), 60)
                st.markdown(f"### ⏰ Time Remaining: {mins:02d}:{secs:02d}")
            else:
                st.error("⏰ Time's up!")
                submit_test()
                return
    
    st.markdown("---")
    
    # Progress indicator
    progress = (current_q + 1) / len(st.session_state.questions)
    st.progress(progress)
    st.markdown(f"Question {current_q + 1} of {len(st.session_state.questions)}")
    
    # Topic and difficulty info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**📚 {question_data['topic']}**")
    with col2:
        difficulty_colors = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}
        st.markdown(f"**{difficulty_colors.get(question_data['difficulty'], '⚪')} {question_data['difficulty']}**")
    with col3:
        model_display = {
            'gemini-1.5-flash': '⚡ Flash',
            'gemini-1.5-pro': '🎯 Pro',
            'gemini-2.5-flash': '🚀 2.5 Flash'
        }
        st.markdown(f"**🤖 {model_display.get(st.session_state.selected_model, 'AI')}**")
    
    # Question display
    st.markdown(f"### {question_data['question']}")
    
    # Answer options
    options = question_data['options']
    current_answer_index = None
    if st.session_state.user_answers[current_q] is not None:
        try:
            current_answer_index = options.index(st.session_state.user_answers[current_q])
        except ValueError:
            current_answer_index = None
    
    selected_answer = st.radio(
        "Select your answer:",
        options,
        index=current_answer_index,
        key=f"question_{current_q}"
    )
    
    # Update user answer
    if selected_answer:
        st.session_state.user_answers[current_q] = selected_answer
    
    # Navigation buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if current_q > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        if current_q < len(st.session_state.questions) - 1:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
    
    with col3:
        if st.button("📋 Review", use_container_width=True):
            st.session_state.show_review = True
            st.rerun()
    
    with col4:
        if st.button("✅ Submit Test", type="primary", use_container_width=True):
            submit_test()

def display_review():
    """Display test review page"""
    st.title("📋 Test Review")
    st.markdown("---")
    
    answered = sum(1 for answer in st.session_state.user_answers if answer is not None)
    total = len(st.session_state.questions)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Questions", total)
    with col2:
        st.metric("Answered", answered)
    with col3:
        st.metric("Remaining", total - answered)
    
    st.markdown("### Question Status")
    
    # Display questions in rows of 5
    num_cols = 5
    for row_start in range(0, len(st.session_state.user_answers), num_cols):
        cols = st.columns(num_cols)
        for i in range(num_cols):
            idx = row_start + i
            if idx < len(st.session_state.user_answers):
                with cols[i]:
                    answer = st.session_state.user_answers[idx]
                    status = "✅" if answer else "❌"
                    if st.button(f"{status} Q{idx+1}", key=f"review_{idx}"):
                        st.session_state.current_question = idx
                        st.session_state.show_review = False
                        st.rerun()
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Back to Test", use_container_width=True):
            st.session_state.show_review = False
            st.rerun()
    with col2:
        if st.button("✅ Submit Test", type="primary", use_container_width=True):
            submit_test()

def submit_test():
    """Submit test and show results"""
    st.session_state.test_completed = True
    st.session_state.show_review = False
    st.rerun()

def display_results():
    """Display test results and solutions"""
    st.title("📊 Test Results")
    st.markdown("---")
    
    # Calculate score
    correct_answers = 0
    for i, (user_answer, question) in enumerate(zip(st.session_state.user_answers, st.session_state.questions)):
        if user_answer and user_answer.startswith(question['correct_answer']):
            correct_answers += 1
    
    total_questions = len(st.session_state.questions)
    score_percentage = (correct_answers / total_questions) * 100
    
    # Display score metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Score", f"{correct_answers}/{total_questions}")
    with col2:
        st.metric("Percentage", f"{score_percentage:.1f}%")
    with col3:
        st.metric("Correct", correct_answers)
    with col4:
        st.metric("Incorrect", total_questions - correct_answers)
    
    # Score interpretation
    if score_percentage >= 80:
        st.success("🎉 Excellent! Outstanding performance!")
    elif score_percentage >= 60:
        st.info("👍 Good job! You're on the right track!")
    else:
        st.warning("📚 Keep practicing! You can improve!")
    
    st.markdown("---")
    
    # Detailed solutions
    st.subheader("📝 Detailed Solutions")
    
    for i, (question, user_answer) in enumerate(zip(st.session_state.questions, st.session_state.user_answers)):
        is_correct = user_answer and user_answer.startswith(question['correct_answer'])
        
        with st.expander(f"Question {i+1} - {'✅ Correct' if is_correct else '❌ Incorrect'}"):
            st.markdown(f"**Question:** {question['question']}")
            
            # Display options
            for option in question['options']:
                if option.startswith(question['correct_answer']):
                    st.markdown(f"✅ **{option}** (Correct Answer)")
                elif user_answer == option:
                    st.markdown(f"❌ **{option}** (Your Answer)")
                else:
                    st.markdown(f"   {option}")
            
            st.markdown("**Explanation:**")
            st.markdown(question['explanation'])
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Take Another Test", use_container_width=True):
            reset_test()
    with col2:
        if st.button("📥 Download Results", use_container_width=True):
            download_results(score_percentage, correct_answers, total_questions)

def reset_test():
    """Reset all session state for a new test"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def download_results(score_percentage, correct_answers, total_questions):
    """Generate downloadable results report"""
    report = f"""AI Aptitude Test Results
========================

Test Details:
- Topic: {st.session_state.selected_topic}
- Difficulty: {st.session_state.selected_difficulty}
- AI Model: {st.session_state.selected_model}
- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Performance:
- Score: {correct_answers}/{total_questions}
- Percentage: {score_percentage:.1f}%
- Status: {'Pass' if score_percentage >= 60 else 'Needs Improvement'}

Question-wise Analysis:
"""
    
    for i, (question, user_answer) in enumerate(zip(st.session_state.questions, st.session_state.user_answers)):
        is_correct = user_answer and user_answer.startswith(question['correct_answer'])
        status = '✓' if is_correct else '✗'
        report += f"\n{i+1}. {status} {question['question'][:50]}..."
    
    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name=f"aptitude_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

def main():
    """Main application logic"""
    # Sidebar content
    with st.sidebar:
        st.header("🧠 AI Aptitude Test")
        st.markdown("---")
        
        # Free tier status
        st.success("🆓 Using FREE Gemini API")
        
        if st.session_state.test_started and not st.session_state.test_completed:
            st.subheader("📊 Progress")
            answered = sum(1 for answer in st.session_state.user_answers if answer is not None)
            st.progress(answered / len(st.session_state.questions))
            st.write(f"{answered}/{len(st.session_state.questions)} questions answered")
            
            if st.session_state.start_time:
                elapsed = datetime.now() - st.session_state.start_time
                st.write(f"Time elapsed: {int(elapsed.total_seconds()//60):02d}:{int(elapsed.total_seconds()%60):02d}")
        
        st.markdown("---")
        st.markdown("### Features")
        st.markdown("- 🎯 AI-generated questions")
        st.markdown("- ⏱️ Timed test (30 minutes)")
        st.markdown("- 📊 Instant results")
        st.markdown("- 💡 Detailed explanations")
        st.markdown("- 📥 Downloadable reports")
        st.markdown("- 🆓 Completely FREE!")
    
    # Main content area
    if not st.session_state.test_started:
        display_topic_selection()
    elif st.session_state.test_completed:
        display_results()
    elif st.session_state.show_review:
        display_review()
    else:
        display_question()

if __name__ == "__main__":
    main()