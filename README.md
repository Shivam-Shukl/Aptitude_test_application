#  AI Aptitude Test Generator

A comprehensive web-based aptitude test application that generates personalized questions using Google Gemini AI. Take timed tests across multiple topics with instant feedback and detailed explanations.

## ✨ Features

- **🎯 AI-Powered Question Generation** - Dynamic question creation using Google Gemini API
- **📚 Multiple Topics** - 10+ aptitude test categories including Quantitative, Logical Reasoning, Verbal Ability
- **⚡ Difficulty Levels** - Easy, Medium, and Hard difficulty options
- **⏱️ Timed Tests** - 30-minute countdown timer with auto-submission
- **📊 Real-time Progress** - Live tracking of answered questions and time remaining
- **🔍 Test Review** - Review and navigate between questions before submission
- **📈 Comprehensive Results** - Detailed scoring with question-wise analysis
- **💡 Detailed Explanations** - Step-by-step solutions for every question
- **📥 Downloadable Reports** - Export test results as text files
- **📱 Responsive Design** - Works seamlessly on desktop and mobile devices

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Integration**: Google Gemini API
- **UI Components**: Streamlit native components
- **Session Management**: Streamlit session state

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Internet connection for API calls

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-aptitude-test.git
   cd ai-aptitude-test
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Gemini API**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the API key for configuration

## ⚙️ Configuration

### Option 1: Using Streamlit Secrets (Recommended for deployment)

1. Create a `.streamlit/secrets.toml` file in your project root:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```

### Option 2: Using Environment Variables

1. Set the environment variable:
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   ```

### Option 3: Direct Configuration (Not recommended for production)

1. Edit the code to directly include your API key (remember to keep it secure)

## 🎮 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Access the application**
   - Open your browser and go to `http://localhost:8501`

3. **Take a test**
   - Select your desired topic and difficulty level
   - Click "Generate Test" to create 20 AI-generated questions
   - Answer questions within the 30-minute time limit
   - Review your answers before submission
   - View detailed results and explanations

## 📚 Available Topics

- **Quantitative Aptitude** - Mathematical problem-solving
- **Logical Reasoning** - Pattern recognition and logical thinking
- **Verbal Ability** - Language and communication skills
- **Data Interpretation** - Chart and graph analysis
- **General Awareness** - Current affairs and general knowledge
- **Programming Logic** - Basic programming concepts
- **Mathematics** - Pure mathematical problems
- **English Grammar** - Grammar rules and usage
- **Analytical Reasoning** - Critical thinking and analysis
- **Numerical Ability** - Number-based problem solving

## 🎯 Test Structure

- **Number of Questions**: 20 per test
- **Time Limit**: 30 minutes
- **Question Format**: Multiple choice (4 options)
- **Scoring**: 1 point per correct answer
- **Passing Score**: 60% (12/20 questions)

## 📊 Results and Analytics

The application provides comprehensive test results including:

- **Overall Score**: Percentage and fraction format
- **Performance Analysis**: Pass/fail status with recommendations
- **Question-wise Breakdown**: Correct/incorrect status for each question
- **Detailed Explanations**: Step-by-step solutions for all questions
- **Time Analysis**: Total time taken for the test
- **Downloadable Report**: Text-based summary for offline reference

## 🔧 Project Structure

```
ai-aptitude-test/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .streamlit/
│   └── secrets.toml      # Configuration file (create this)

```

## 📦 Dependencies

```txt
streamlit>=1.28.0
google-generativeai>=0.3.0
```

## 🚀 Deployment

### Deploy on Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Add your `GEMINI_API_KEY` in the secrets section
5. Deploy!

### Deploy on Heroku

1. Create a `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Set environment variables:
   ```bash
   heroku config:set GEMINI_API_KEY="your_api_key_here"
   ```

3. Deploy using Heroku CLI

## 🎨 Customization

### Adding New Topics

Edit the `topics` list in the `display_topic_selection()` function:

```python
topics = [
    "Your New Topic",
    # ... existing topics
]
```

### Modifying Timer Duration

Change the timer duration in the `display_question()` function:

```python
remaining = timedelta(minutes=45) - elapsed  # Change from 30 to 45 minutes
```

### Customizing Number of Questions

Modify the `generate_test()` function call:

```python
questions = generator.generate_test(
    st.session_state.selected_topic,
    st.session_state.selected_difficulty,
    25  # Change from 20 to 25 questions
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your Gemini API key is correctly set in secrets or environment variables
   - Verify the API key is active and has sufficient quota

2. **Question Generation Fails**
   - Check your internet connection
   - Verify API key permissions
   - Try reducing the number of questions if you hit rate limits

3. **Timer Issues**
   - Refresh the page if the timer stops working
   - Ensure JavaScript is enabled in your browser

4. **Streamlit Errors**
   - Clear browser cache and cookies
   - Restart the Streamlit server
   - Check Python version compatibility

### Getting Help

- Open an issue on GitHub for bugs or feature requests
- Check the [Streamlit documentation](https://docs.streamlit.io/) for general Streamlit issues
- Refer to [Google AI documentation](https://ai.google.dev/docs) for API-related issues

## 🙏 Acknowledgments

- **Google Gemini AI** for providing the question generation API
- **Streamlit** for the amazing web app framework
- **Open Source Community** for inspiration and resources



Made with ❤️ using Python and AI
