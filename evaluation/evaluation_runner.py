import json

import pandas as pd

class EvaluationRunner:
    """
    Runs a predefined evaluation suite
    against the pipeline.
    """

    def __init__(
        self,
        pipeline
    ):
        self.pipeline = pipeline

    def run(
        self,
        question_file
    ):

        with open(
            question_file,
            "r",
            encoding="utf-8"
        ) as file:

            questions = json.load(
                file
            )

        results = []

        for item in questions:

            question = item[
                "question"
            ]

            response = (
                self.pipeline.run_safe(
                    question
                )
            )

            if response["success"]:

                answer = (
                    response["data"]
                    .answer
                )

                status = "PASS"

            else:

                answer = (
                    response["error"]
                )

                status = "FAIL"

            results.append({

                "question":
                question,

                "status":
                status,

                "response":
                answer
            })

        dataframe = pd.DataFrame(
            results
        )

        return dataframe

    def save_report(
        self,
        dataframe,
        output_file="evaluation_report.csv"
    ):

        dataframe.to_csv(
            output_file,
            index=False
        )

        return output_file

    def summary(
        self,
        dataframe
    ):

        total = len(
            dataframe
        )

        passed = len(

            dataframe[
                dataframe["status"]
                == "PASS"
            ]
        )

        failed = len(

            dataframe[
                dataframe["status"]
                == "FAIL"
            ]
        )

        success_rate = 0

        if total > 0:

            success_rate = round(
                (passed / total) * 100,
                2
            )

        return {

            "total":
            total,

            "passed":
            passed,

            "failed":
            failed,

            "success_rate":
            success_rate
        }
