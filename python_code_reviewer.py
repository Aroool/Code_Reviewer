import streamlit as st
import openai
from dotenv import load_dotenv
load_dotenv()
import os
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Set up the Streamlit app
st.set_page_config(page_title="Python Code Reviewer", layout="centered")

st.title("🐍 Python Code Reviewer & Refactorer!!")
st.caption("Paste your Python code below and get review suggestions or a refactored version using GPT-4.")


# 📁 Upload Python file
uploaded_file = st.file_uploader("📂 Upload a Python (.py) file", type=["py"])

# 🔁 Read uploaded file or fallback to blank input
code_input = ""
if uploaded_file:
    code_input = uploaded_file.read().decode("utf-8")

# 🧾 Unified Text Area (only one shown always)
code_input = st.text_area("📥 Paste your Python code here:", value=code_input, height=300, key="code_box")


# Layout for two buttons
col1, col2, col3, col4 = st.columns(4)

# 🔍 Review Code Button
if col3.button("🔍 Review Code"):
    if code_input.strip() == "":
        st.warning("Please enter some code first.")
    else:
        with st.spinner("Reviewing your code..."):
            review_prompt = f""""
You are a senior Python developer. Review the following code for:
- Readability
- Performance
- Code smells or issues
- Suggestions for improvement

Provide bullet-point feedback.

Code:
```python
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
You are a senior Python developer. Refactor the code below to improve:
- Readability and formatting
- Code structure and modularity
- Follow PEP8 standards

Add docstrings and inline comments where appropriate.

Code:
```python
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
You're an expert Python tutor. Explain this code to a beginner in super simple terms. Break it down line by line. Be casual and easy to understand.
```python
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
You're a Python expert. Convert the following code into a Mermaid.js flowchart.

Rules:
- Use 'flowchart TD' format.
- Capture major steps like input, conditionals, loops, and returns.
- Do NOT include actual code — just high-level logic.

Code:
```python
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
