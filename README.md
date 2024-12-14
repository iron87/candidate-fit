# Candidate Fit App

## Overview

This project provides a web-based interface to upload a candidate's CV and obtain a match with a job position. Currently, the job position is represented as a predefined string within the code. The system leverages **Streamlit** for the user interface and **Ollama** for the matching functionality.

## Requirements

To use this project, ensure you have the following installed on your computer:

- **Ollama**: The Ollama service must be installed and running on your machine.
- **Python**: A compatible version of Python is required.

## Installation and Usage

Follow these steps to install and run the application:

1. Clone the project repository to your local machine.
2. Install the required Python dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Streamlit application by executing:
   ```bash
   streamlit run app.py
   ```

Once running, you can interact with the application via your web browser. Upload a CV file to see how well it matches the predefined job position.
