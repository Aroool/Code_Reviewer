import streamlit as st
import requests
import os
from dotenv import load_dotenv
import openai

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
client = openai.OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(page_title="GitHub Code Analyzer", layout="wide")
st.title("📂 GitHub Code Analyzer")
st.write("Enter a public GitHub repository URL below. We'll fetch its contents and let you select files to analyze.")

repo_url = st.text_input("🔗 GitHub Repo URL", placeholder="https://github.com/username/repo")

def extract_repo_info(url):
    try:
        parts = url.strip().replace("https://github.com/", "").split("/")
        return parts[0], parts[1]
    except:
        return None, None

def fetch_repo_contents(owner, repo, path=""):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    res = requests.get(api_url, headers=HEADERS)
    return res.json() if res.status_code == 200 else []

if repo_url:
    owner, repo = extract_repo_info(repo_url)

    if owner and repo:
        contents = fetch_repo_contents(owner, repo)

        if contents:
            file_options = [item["path"] for item in contents if item["type"] == "file"]
            selected_file = st.selectbox("📄 Choose a file to view:", file_options)

            if selected_file:
                raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{selected_file}"
                file_res = requests.get(raw_url)

            if file_res.status_code == 200:
                file_code = file_res.text
                language = selected_file.split(".")[-1]

    # 🔘 Buttons placed horizontally
                btn1, btn2, btn3, btn4 = st.columns(4)
                prompt = None

                with btn1:
                    if st.button("🧠 Review"):
                        prompt = f"You are a senior developer. Review the following code for readability, performance, and improvements.\n```{file_code}```"
                with btn2:
                    if st.button("🛠️ Refactor"):
                        prompt = f"Refactor the following code to be cleaner and more maintainable.\n```{file_code}```"
                with btn3:
                    if st.button("📖 Explain"):
                        prompt = f"Explain the following code to a beginner in simple terms.\n```{file_code}```"
                with btn4:
                    if st.button("📊 Flowchart"):
                        prompt = f"Generate a Mermaid.js flowchart for the following code:\n```{file_code}```"

    # 💬 GPT Output
                if prompt:
                    try:
                        response = client.chat.completions.create(
                            model="gpt-4",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.4,
                            max_tokens=800,
                        )
                        if "Flowchart" in prompt:
                            st.markdown(f"""```mermaid\n{response.choices[0].message.content.strip()}\n```""", unsafe_allow_html=True)
                        else:
                            st.markdown(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

                # ✅ Code preview should come AFTER GPT section
                st.subheader("📜 Code Preview")
                st.code(file_code, language=language)
