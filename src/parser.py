from openai import OpenAI

from src.models import QueryPlan
from src.prompts import (
    SYSTEM_PROMPT,
    build_prompt
)
from src.validator import QueryValidator


class QueryParser:
    """
    Converts a user question into a
    structured QueryPlan using OpenAI.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4.1-mini"
    ):

        self.client = OpenAI(
            api_key=api_key
        )

        self.model = model

    def parse(
        self,
        question: str,
        metadata: dict
    ) -> QueryPlan:

        prompt = build_prompt(
            question=question,
            metadata=metadata
        )

        try:

            response = (
                self.client
                .beta
                .chat
                .completions
                .parse(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    response_format=QueryPlan
                )
            )

            parsed = (
                response
                .choices[0]
                .message
                .parsed
            )

            if parsed is None:

                raise ValueError(
                    "Failed to parse QueryPlan."
                )

            return parsed

        except Exception as e:

            raise ValueError(
                f"Query parsing failed: {str(e)}"
            )


class QueryPlanner:
    """
    Full planning pipeline.

    Question
        ↓
    QueryParser
        ↓
    QueryPlan
        ↓
    QueryValidator
        ↓
    Valid QueryPlan
    """

    def __init__(
        self,
        metadata: dict,
        schema_manager,
        api_key: str,
        model: str = "gpt-4.1-mini"
    ):

        self.metadata = metadata

        self.parser = QueryParser(
            api_key=api_key,
            model=model
        )

        self.validator = QueryValidator(
            metadata=metadata,
            schema_manager=schema_manager
        )

    def create_plan(
        self,
        question: str
    ) -> QueryPlan:

        if not question.strip():

            raise ValueError(
                "Question cannot be empty."
            )

        plan = self.parser.parse(
            question=question,
            metadata=self.metadata
        )

        self.validator.validate(
            question=question,
            plan=plan
        )

        return plan