# Design Note

## Problem Statement

Build a natural language interface for a government agricultural dataset.

The system should:

1. Accept natural language questions.
2. Convert questions into structured operations.
3. Execute computations on the dataset.
4. Return answers and visualizations.
5. Reject unsupported questions.

---

# Design Philosophy

The language model should not answer questions directly.

Instead:

Question

↓

Structured Query Plan

↓

Dataset Computation

↓

Answer

This approach prevents hallucinated numerical answers and improves trustworthiness.

---

# Architecture

```text
User Question
      ↓
OpenAI Structured Outputs
      ↓
QueryPlan
      ↓
Validation Layer
      ↓
Pandas Execution Engine
      ↓
Visualization Layer
      ↓
Answer Generator
      ↓
Final Response
```

---

# Core Components

## Query Planning

Implemented in:

```text
src/parser.py
```

Responsibilities:

- Understand user intent
- Produce QueryPlan
- Use Structured Outputs
- Prevent malformed plans

Example:

```json
{
  "operation": "compare",
  "crop": "RICE",
  "metric": "PRODUCTION",
  "state": "Punjab",
  "compare_with": "Haryana"
}
```

---

## Validation Layer

Implemented in:

```text
src/validator.py
```

Responsibilities:

- Validate crop
- Validate metric
- Validate year
- Validate state
- Validate district
- Validate comparisons
- Reject out-of-scope queries

---

## Execution Layer

Implemented in:

```text
src/executor.py
```

Responsibilities:

- Aggregate calculations
- Rankings
- Trend analysis
- State comparisons

All calculations are performed using Pandas.

No generated code is executed.

---

## Visualization Layer

Implemented in:

```text
src/charts.py
```

Responsibilities:

- Generate bar charts
- Generate line charts
- Save chart images
- Return image paths

---

## Answer Generation

Implemented in:

```text
src/answer_generator.py
```

Responsibilities:

- Convert results into natural language
- Add units
- Produce concise explanations

---

## Pipeline Layer

Implemented in:

```text
src/pipeline.py
```

Responsibilities:

- Orchestrate entire workflow
- Handle failures
- Produce FinalResponse

---

# Why Structured Outputs?

Traditional prompting returns text.

Example:

```text
Top 5 rice states are ...
```

This is difficult to validate.

Structured Outputs return:

```json
{
  "operation": "top_n",
  "crop": "RICE",
  "metric": "PRODUCTION",
  "top_n": 5
}
```

Advantages:

- Typed
- Validatable
- Safer
- Easier to debug

---

# Trustworthiness

The application improves trust using:

1. Structured Query Plans
2. Validation Layer
3. Dataset Computation
4. Provenance Tracking

Every answer includes:

- Operation
- Dataset Column
- Rows Processed

---

# Scalability

Future improvements:

## Multiple Datasets

Introduce a dataset router.

```text
Question
     ↓
Dataset Router
     ↓
Dataset Specific Pipeline
```

---

## Faster Query Engine

Replace Pandas with:

- DuckDB
- Polars

for larger datasets.

---

## Authentication

Add:

- User accounts
- Rate limiting
- Access control

---

## Caching

Cache:

- Query plans
- Computation results
- Generated charts

---

# Limitations

Current version:

- Single dataset
- English only
- Fixed operation types

Supported operations:

- Aggregate
- Top N
- Top 1
- Trend
- Compare

---

# Conclusion

The final system combines:

- LLM reasoning
- Structured Outputs
- Validation
- Deterministic Computation

to create a trustworthy natural language interface for agricultural government data.