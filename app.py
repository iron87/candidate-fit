import streamlit as st
from langchain_ollama import ChatOllama
from openai import OpenAI
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

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
st.title("🧑🏾‍💻👩🏼‍💻🔗 Candidate Fit App")


def generate_response(input_text):
    model = ChatOllama(temperature=0.7, model="llama3.2")
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
    return file_content;


def get_fit_analysis_and_rate(input_text, job_position, max_length):
    chunks = [input_text[i:i+max_length]
        for i in range(0, len(input_text), max_length)]
    results = []
    for i, chunk in enumerate(chunks):
        st.write(f"Analyzing chunk {i + 1}")
        results.append(generate_response(f"Extract relevant information about the experience and the skills of the person: {
                       chunk} and match candidate with the job position: {job_position} Please be concise and write also a match rate"))
    return "\n\n".join(results);

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
            file_content = extract_pdf(uploaded_file);
            # loader = UnstructuredPDFLoader(uploaded_file)
            # documents = loader.load()
            # file_content = "\n".join([doc.page_content for doc in documents])
            # Mostra un'anteprima del contenuto
            st.text_area("Content preview", file_content[:1000], height=250)            
            analysis = get_fit_analysis_and_rate(file_content,JOB_POSITION,4000);
            # Display the combined results
            st.success("Analysis Completed!")
            st.text_area("Analysis Result", analysis, height=300)
        except Exception as e:
            st.error(f"Error during candidate Resume Analysis: {e}")
