import json
import logging

import altair as alt
import pandas as pd
import streamlit as st
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from PyPDF2 import PdfReader

from githubapiclient import GitHubApiClient

logging.basicConfig(level=logging.ERROR,
                    filename='app.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

JOB_POSITION = """
Position: Engineering Manager

We are looking for an experienced Engineering Manager to lead and manage our engineering team. The ideal candidate will have a strong technical background combined with leadership skills. You will be responsible for overseeing project timelines, resource allocation, and mentoring engineers.

Key responsibilities include driving technical initiatives, ensuring product quality, and collaborating with cross-functional teams. You will provide strategic direction, foster a positive team culture, and ensure continuous improvement.

Technologies:
- Python, Java, and Node.js for backend development
- React and Angular for frontend development
- Cloud platforms (AWS, Azure, or GCP)
- CI/CD pipelines (Jenkins, GitLab)
- Docker, Kubernetes for containerization and orchestration

Requirements:
- Proven experience in managing engineering teams.
- Strong technical expertise in the above technologies.
- Excellent communication and problem-solving skills.
"""

LLM_JSON_TEMPLATE = """"
{'match-rating':'','description':'','experience-in-role':'','what-fits':[],'what-not-fits':[],'what-requires-additional-info':[], 'github-username':'', tech-stack-candidate-match':{{'<technology-name1>':<true|false>},{'<technology-name2>':<true|false>},...}}
"""

st.title("🧑🏾‍💻👩🏼‍💻🔗 Candidate Fit App")


def generate_response(input_text):
    model = ChatOllama(temperature=0.2, model="llama3.2", format="json")
    response = model.invoke(input_text)
    if isinstance(response, str):
        return response
    elif hasattr(response, 'content'):
        return response.content
    else:
        return str(response)


def extract_pdf(file):
    reader = PdfReader(file)
    file_content = "\n".join([page.extract_text() for page in reader.pages])
    return file_content


def get_fit_analysis_and_rate(input_text, job_position, max_length):
    # chunks = [input_text[i:i+max_length]
    #     for i in range(0, len(input_text), max_length)]
    results = []
    # for i, chunk in enumerate(chunks):
    #     st.write(f"Analyzing chunk {i + 1}")
    #     results.append(generate_response(f"Extract relevant information about the experience and the skills of the person: {
    #                    chunk} and match candidate with the job position: {job_position} Please be concise and write also a match rate. The analys should show: the match rating, what fits and what not"))
    results.append(
        generate_response(
            f"Analyze the provided input to extract relevant information about the person's experience and skills: {input_text}, and match the candidate with the job position: {job_position}. Format the output strictly as per the JSON template: {LLM_JSON_TEMPLATE}, including a match rating (0-100) for experience and technologies, alignment details (regarding experience within the role and technologies used, what fits and what not), interview clarifications (what-requires-additional-info), the candidate's GitHub username if available, and a tech-stack-candidate-match field listing job position technologies with booleans indicating the candidate's experience (explicitly stated in the resume). Output only the requested data in JSON format, no additional text"
        ))
    return "\n\n".join(results)


# with st.form("my_form"):
# text = st.text_area(
#     "Enter text:",
#     "What are the three key pieces of advice for learning how to code?",
# )
# submitted = st.form_submit_button("Submit")
# generate_response(text)

uploaded_file = st.file_uploader("Upload the Resume", type=["pdf"])
if uploaded_file is not None:
    with st.spinner("Extractiing file contents..."):
        try:
            file_content = extract_pdf(uploaded_file)
            # loader = UnstructuredPDFLoader(uploaded_file)
            # documents = loader.load()
            # file_content = "\n".join([doc.page_content for doc in documents])

            #st.text_area("Content preview", file_content[:1000], height=250)
            analysis = get_fit_analysis_and_rate(file_content, JOB_POSITION,
                                                 4000)
            st.success("Analysis Completed!")
            st.text_area("Analysis Result", analysis, height=300)
            data = json.loads(analysis)

            rating = int(data['match-rating'])

            st.metric(label="Rating", value=rating, delta="")
            if ('github-username' in data):
                contribution = GitHubApiClient().get_user_contributions(
                    data['github-username'], 12)
                st.metric(label="GitHub Contribution",
                          value=contribution['total_events'],
                          delta="")

            tech_stack_match = data.get('tech-stack-candidate-match', [])
            if tech_stack_match:
                tech_match_df = pd.DataFrame(list(tech_stack_match.items()),
                                             columns=['Technology', 'Match'])
                tech_match_df['Match'] = tech_match_df['Match'].apply(
                    lambda x: '✅' if x else '❌')
                st.write("Tech Stack Match")
                st.table(tech_match_df)
        except Exception as e:
            logging.error(f"Error during candidate Resume Analysis: {e}")
            st.error(f"Error during candidate Resume Analysis: {e}")
