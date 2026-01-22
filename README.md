# Patent Title Classification App

This project is a Flask-based web application that uses OpenAI’s API to automatically classify patent titles into high-level technology categories and export the results as a downloadable CSV file.

It is designed for patent analytics, innovation strategy, and technology landscape analysis, allowing users to quickly organize patent data with consistent categorization and ordering.

---
## Features

- Upload a CSV file containing patent titles
- Automatically classify each patent into one of the following categories:
  - Chemical
  - Biotechnology
  - Electrical
  - Mechanical
  - Software
- Group patents by category so related technologies stay together
- Apply a secondary sort by publication number within each category
- Download the classified and sorted results as a CSV file
- Simple web UI for non-technical users

---

## How It Works

1. User uploads a CSV file via the web interface  
2. The app reads the file using pandas  
3. Each patent title is sent to the OpenAI API for classification  
4. The results are:
   - Grouped by category (fixed category order)
   - Sorted by publication number within each category  
5. A new CSV file is generated and returned to the user for download  

---

## Input File Requirements

Your uploaded CSV must include at least the following columns:

- `Title` — the patent title to be classified  
- `Publication Number` — used for secondary sorting  

### Example

```text
Publication Number    Title
US1234567A1           Method for polymer synthesis
WO2020123456          Gene editing platform
```
---
## Output

The output CSV includes all original columns plus:

Category — the AI-assigned patent category

The file is grouped by category and sorted by publication number within each group.

---
## Project Structure
project/
│
├── app.py
├── templates/
│   └── upload.html
├── .env
├── requirements.txt
└── README.md
---
## Setup Instructions
1. Clone the Repository
git clone <your-repo-url>
cd <your-project>

2. Create and Activate a Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key_here
---
## Running the Application
python app.py


Then open your browser and navigate to:

http://127.0.0.1:5000
___
## Technology Stack

Python

Flask

pandas

OpenAI API

HTML (Jinja2 templates)
---
## Use Cases

Patent analytics and portfolio review

Technology trend analysis

Competitive intelligence

Prior art organization

Innovation strategy support
___
## Notes & Limitations

Classification quality depends on the patent title text

Very short or ambiguous titles may be classified as Unknown

API usage is subject to OpenAI rate limits and token costs

___
## Future Improvements

Batch classification optimization

Confidence scores per category

Additional technology categories

Support for Excel uploads

Visualization dashboard (charts by category)
