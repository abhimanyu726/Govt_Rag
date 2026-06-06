import os

import streamlit as st

from dotenv import load_dotenv

from src.data_loader import (
    DataLoader
)

from src.schema_manager import (
    SchemaManager
)

from src.pipeline import (
    AgriculturePipeline
)


load_dotenv()


DATA_PATH = "data/ICRISAT.csv"


@st.cache_resource
def initialize_pipeline():
    """
    Initialize dataset,
    schema and pipeline once.
    """

    loader = DataLoader(
        DATA_PATH
    )

    dataframe = loader.load()

    schema = SchemaManager(
        dataframe
    )

    metadata = (
        schema.metadata()
    )

    pipeline = AgriculturePipeline(

        dataframe=dataframe,

        schema_manager=schema,

        metadata=metadata,

        api_key=os.getenv(
            "OPENAI_API_KEY"
        )
    )

    return {

        "pipeline":
        pipeline,

        "dataframe":
        dataframe,

        "schema":
        schema
    }


resources = (
    initialize_pipeline()
)

pipeline = (
    resources["pipeline"]
)

dataset = (
    resources["dataframe"]
)

schema = (
    resources["schema"]
)


st.set_page_config(
    page_title="Talk To Government Data",
    page_icon="🌾",
    layout="wide"
)


st.title(
    "🌾 Talk To Government Data"
)

st.markdown(
"""
Ask natural language questions about
crop production, yield and cultivated area.

Answers are generated using
real dataset computations and not
LLM-generated numbers.
"""
)


# ----------------------------------
# Sidebar
# ----------------------------------

with st.sidebar:

    st.header(
        "Dataset"
    )

    st.info(
        "ICRISAT District Level Agricultural Dataset"
    )

    st.header(
        "Dataset Summary"
    )

    st.write(
        f"Rows: {dataset.shape[0]:,}"
    )

    st.write(
        f"Columns: {dataset.shape[1]}"
    )

    st.write(
        f"Crops: {len(schema.get_crops())}"
    )

    st.write(
        f"States: {len(schema.get_states())}"
    )

    st.write(
        f"Years: {len(schema.get_years())}"
    )

    st.header(
        "Example Questions"
    )

    st.markdown(
        """
        - Top 5 rice producing states in 2018

        - Which state produced the most wheat in 2015

        - Compare rice production between Punjab and Haryana

        - Show wheat production trend in Punjab

        - Total maize production in 2018

        - Cotton yield trend in Gujarat

        - Top 10 groundnut producing states
        """
    )


# ----------------------------------
# User Input
# ----------------------------------

question = st.text_area(

    label="Question",

    height=120,

    placeholder=
    "Example: Top 5 rice producing states in 2018"
)


analyze_button = st.button(
    "Analyze"
)


# ----------------------------------
# Query Execution
# ----------------------------------

if analyze_button:

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

        st.stop()

    with st.spinner(
        "Analyzing..."
    ):

        response = (

            pipeline.run_safe(
                question
            )
        )

    if not response["success"]:

        st.error(
            response["error"]
        )

    else:

        result = (
            response["data"]
        )

        # ------------------------
        # Answer
        # ------------------------

        st.subheader(
            "Answer"
        )

        st.success(
            result.answer
        )

        # ------------------------
        # Visualization
        # ------------------------

        if result.chart_path:

            st.subheader(
                "Visualization"
            )

            st.image(
                result.chart_path,
                use_container_width=True
            )

        # ------------------------
        # Result Preview
        # ------------------------

        st.subheader(
            "Result Preview"
        )

        st.write(
            result.result_preview
        )

        # ------------------------
        # Query Plan
        # ------------------------

        with st.expander(
            "Query Plan"
        ):

            st.json(
                result.query_plan
            )

        # ------------------------
        # Provenance
        # ------------------------

        with st.expander(
            "Provenance"
        ):

            st.json(
                result.provenance
            )


# ----------------------------------
# Footer
# ----------------------------------

st.markdown("---")

st.caption(
    """
    Built using OpenAI Structured Outputs,
    Pydantic, Pandas and Streamlit.

    All numerical answers are computed
    directly from the dataset.
    """
)