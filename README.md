# 🌾 Talk To Government Data

Natural language analytics system built using OpenAI Structured Outputs, Pydantic, Pandas and Streamlit.

The application allows users to ask questions about agricultural production, yield and cultivated area using natural language.

All numerical answers are generated from actual dataset computations and not from LLM knowledge.

---

## Features

### Natural Language Queries

Examples:

- Top 5 rice producing states in 2018
- Compare rice production between Punjab and Haryana
- Show wheat production trend in Punjab
- Total maize production in 2015

---

### Structured Query Planning

OpenAI Structured Outputs generate a strongly typed QueryPlan.

Example:

```json
{
  "operation": "top_n",
  "crop": "RICE",
  "metric": "PRODUCTION",
  "year": 2018,
  "top_n": 5
}
```

---

### Dataset Driven Computation

The LLM never performs calculations.

All computations are executed using Pandas directly on the dataset.

Supported operations:

- Aggregate
- Top N
- Top 1
- Trend Analysis
- State Comparison

---

### Automatic Validation

The system validates:

- Crops
- Metrics
- States
- Districts
- Years
- Comparison Queries
- Out Of Scope Questions

---

### Visualization

Automatic chart generation:

- Bar Charts
- Line Charts

---

### Provenance Tracking

Every answer includes:

- Operation Used
- Dataset Column Used
- Rows Processed

---

## Project Structure

```text
Talk_To_Govt_Data/

│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── Design_Note.md
│
├── data/
│   └── ICRISAT.csv
│
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── data_loader.py
│   ├── schema_manager.py
│   ├── validator.py
│   ├── prompts.py
│   ├── parser.py
│   ├── executor.py
│   ├── charts.py
│   ├── answer_generator.py
│   └── pipeline.py
│
└── evaluation/
    ├── questions.json
    └── evaluation_runner.py
```

---

## Installation

Create virtual environment:

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create:

```text
.env
```

Add:

```text
OPENAI_API_KEY=your_api_key
```

---

## Run Application

```bash
streamlit run app.py
```

---

## Evaluation

Run evaluation suite:

```python
from evaluation.evaluation_runner import (
    EvaluationRunner
)

runner = EvaluationRunner(
    pipeline
)

results = runner.run(
    "evaluation/questions.json"
)

print(results)
```

---

## Example Workflow

User Question

↓

Top 5 rice producing states in 2018

↓

QueryPlan

↓

Dataset Execution

↓

Chart Generation

↓

Answer Generation

↓

Final Response

---

## Dataset

ICRISAT District Level Agricultural Dataset

Contains:

- State
- District
- Year
- Production
- Area
- Yield

for multiple crops across India.

---

## Technology Stack

- OpenAI Structured Outputs
- Pydantic
- Pandas
- Streamlit
- Matplotlib

---

## Notes

The LLM is used only for query planning.

All calculations are performed using Pandas.

No generated code is executed.

This ensures reproducibility, transparency and trustworthiness.