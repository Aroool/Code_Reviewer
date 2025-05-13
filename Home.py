import streamlit as st
import openai
import time
from dotenv import load_dotenv
load_dotenv()
import os
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])



# 🚫 Hide sidebar and the toggle button completely
st.set_page_config(page_title="DevSensei", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)


# Typing animation for DevSensei title
title_placeholder = st.empty()
full_title = "🥋 DevSensei"

typed_title = ""
for char in full_title:
    typed_title += char
    title_placeholder.markdown(
        f"<h1 style='text-align: center; font-size: 48px;'>{typed_title}</h1>",
        unsafe_allow_html=True
    )
    time.sleep(0.1)  # Typing speed (adjust as needed)

# Optional subtitle with fade effect
st.markdown(
    "<p style='text-align: center; font-size: 20px; color: #666;'>Your Multi-Language Code Mentor</p>",
    unsafe_allow_html=True
)


# Other Home page content...

# Navigation Button
if st.button("🧠 Go to GitHub Code Analyzer"):
    st.switch_page("pages/Github_Code_Analyzer.py")


# st.title(" DevSensei")
# st.caption("Paste your Python code below and get review suggestions or a refactored version using GPT-4.")



# Language selector
language = st.selectbox("Select Programming Language", ["Python", "JavaScript", "Java", "C++", "Go", "Rust"])

# Map each language to its appropriate file extensions
file_types = {
    "Python": ["py"],
    "JavaScript": ["js"],
    "Java": ["java"],
    "C++": ["cpp", "h"],
    "Go": ["go"],
    "Rust": ["rs"]
}

# Get the appropriate extension(s) for the selected language
allowed_exts = file_types.get(language, ["txt"])  # default to txt if somehow missing

# File uploader that adapts to the selected language
uploaded_file = st.file_uploader(f"📂 Upload your {language} file", type=allowed_exts)

# 🔁 Read uploaded file or fallback to blank input
code_input = ""
if uploaded_file:
    code_input = uploaded_file.read().decode("utf-8")

# 🧾 Unified Text Area (only one shown always)
code_input = st.text_area(f"📥 Paste your {language} code here:", value=code_input, height=300, key="code_box")


# Layout for two buttons
col1, col2, col3, col4 = st.columns(4)

# 🔍 Review Code Button
if col3.button("🔍 Review Code"):
    if code_input.strip() == "":
        st.warning("Please enter some code first.")
    else:
        with st.spinner("Reviewing your code..."):
            review_prompt = f""""
You are a senior {language} developer. Review the following code for:
- Readability
- Performance
- Code smells or issues
- Suggestions for improvement

Provide bullet-point feedback.

Code:
```{language.lower()}
{code_input}
```
"""
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": review_prompt}],
                    temperature=0.5,
                    max_tokens=1000,
                )
                st.success("🧠 Code Review Suggestions:")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"❌ Error: {e}")

# 🛠️ Refactor Code Button
if col2.button("🛠️ Refactor Code"):
    if code_input.strip() == "":
        st.warning("Please enter some code first.")
    else:
        with st.spinner("Refactoring your code..."):
            refactor_prompt = f""""
You are a senior {language} developer. Refactor the code below to improve:
- Readability and formatting
- Code structure and modularity
- Follow PEP8 standards

Add docstrings and inline comments where appropriate.

Code:
```{language.lower()}
{code_input}
```
"""
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": refactor_prompt}],
                    temperature=0.5,
                    max_tokens=1000,
                )
                st.success("🔧 Refactored Code:")
                st.code(response.choices[0].message.content, language="python")
            except Exception as e:
                st.error(f"❌ Error: {e}")


# 📖 Explain Code Button

if col1.button("📖 Explain Code"):
    if code_input.strip() == "":
        st.warning("Please enter some code first.")
    else:
        with st.spinner("Explaining your code..."):
            explain_prompt = f"""
You're an expert {language} tutor. Explain this code to a beginner in super simple terms. Break it down line by line. Be casual and easy to understand.
```{language.lower()}
{code_input}
```
"""
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": explain_prompt}],
                    temperature=0.5,
                    max_tokens=1000,
                )
                st.success("📜 Code Explanation:")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"❌ Error: {e}")


# 🗺️ Flowchart Generator Button
if col4.button("🗺️ Flowchart"):
    if code_input.strip() == "":
        st.warning("Please enter some code first.")
    else:
        with st.spinner("Generating flowchart..."):
            flowchart_prompt = f"""
You're a {language} expert. Convert the following code into a Mermaid.js flowchart.

Rules:
- Use 'flowchart TD' format.
- Capture major steps like input, conditionals, loops, and returns.
- Do NOT include actual code — just high-level logic.

Code:
```{language.lower()}
{code_input}
```
"""
            try:
                response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": flowchart_prompt}],
                temperature=0.3,
                max_tokens=500,
                )
                st.success("🧭 Flowchart Generated:")
                st.markdown(f"mermaid\n{response.choices[0].message.content}\n", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Error: {e}")
