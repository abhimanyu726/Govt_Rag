from pathlib import Path
import uuid

import matplotlib.pyplot as plt


class ChartGenerator:
    """
    Generates charts for query results.
    """

    def __init__(
        self,
        output_dir="outputs/charts"
    ):

        self.output_dir = Path(
            output_dir
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def create_chart_path(
        self
    ):

        filename = (
            f"{uuid.uuid4()}.png"
        )

        return (
            self.output_dir
            / filename
        )

    def create_bar_chart(
        self,
        dataframe,
        x_column,
        y_column,
        title
    ):

        chart_path = (
            self.create_chart_path()
        )

        plt.figure(
            figsize=(10, 5)
        )

        plt.bar(
            dataframe[x_column],
            dataframe[y_column]
        )

        plt.title(title)

        plt.xlabel(
            x_column
        )

        plt.ylabel(
            y_column
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.tight_layout()

        plt.savefig(
            chart_path,
            bbox_inches="tight"
        )

        plt.close()

        return str(
            chart_path
        )

    def create_line_chart(
        self,
        dataframe,
        x_column,
        y_column,
        title
    ):

        chart_path = (
            self.create_chart_path()
        )

        plt.figure(
            figsize=(10, 5)
        )

        plt.plot(
            dataframe[x_column],
            dataframe[y_column],
            marker="o"
        )

        plt.title(title)

        plt.xlabel(
            x_column
        )

        plt.ylabel(
            y_column
        )

        plt.grid(
            True,
            alpha=0.3
        )

        plt.tight_layout()

        plt.savefig(
            chart_path,
            bbox_inches="tight"
        )

        plt.close()

        return str(
            chart_path
        )

    def generate(
        self,
        execution_result
    ):

        if (
            execution_result.chart_type
            is None
        ):

            return None

        dataframe = (
            execution_result.result_data
        )

        metric_column = (
            execution_result.metric_column
        )

        context = (
            execution_result.query_context
        )

        crop = context.get(
            "crop",
            ""
        )

        metric = context.get(
            "metric",
            ""
        )

        year = context.get(
            "year"
        )

        title = (
            f"{crop} {metric}"
        )

        if year:

            title += (
                f" ({year})"
            )

        if (
            execution_result.chart_type
            == "line"
        ):

            return self.create_line_chart(

                dataframe=dataframe,

                x_column="Year",

                y_column=metric_column,

                title=title
            )

        return self.create_bar_chart(

            dataframe=dataframe,

            x_column=dataframe.columns[0],

            y_column=metric_column,

            title=title
        )