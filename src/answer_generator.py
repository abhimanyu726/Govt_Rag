class AnswerGenerator:
    """
    Converts execution results into
    human-readable answers.
    """

    UNIT_MAPPING = {
        "1000 tons": "thousand tons",
        "1000 ha": "thousand hectares",
        "Kg per ha": "kg/hectare"
    }

    @staticmethod
    def format_number(
        value
    ):

        try:

            return (
                f"{float(value):,.2f}"
            )

        except Exception:

            return str(value)

    def normalize_unit(
        self,
        unit
    ):

        if not unit:

            return ""

        return self.UNIT_MAPPING.get(
            unit,
            unit
        )

    def aggregate(
        self,
        result,
        unit
    ):

        context = (
            result.query_context
        )

        crop = context["crop"]

        metric = context["metric"]

        year = context.get(
            "year"
        )

        value = (
            result.result_data
        )

        unit = self.normalize_unit(
            unit
        )

        answer = (

            f"Total "

            f"{crop.lower()} "

            f"{metric.lower()} "

            f"is "

            f"{self.format_number(value)}"
        )

        if unit:

            answer += (
                f" {unit}"
            )

        if year:

            answer += (
                f" in {year}"
            )

        answer += "."

        return answer

    def top_n(
        self,
        result,
        unit
    ):

        df = result.result_data

        context = (
            result.query_context
        )

        crop = context["crop"]

        metric = context["metric"]

        year = context.get(
            "year"
        )

        unit = self.normalize_unit(
            unit
        )

        leader = df.iloc[0]

        group_column = (
            df.columns[0]
        )

        metric_column = (
            result.metric_column
        )

        answer = (

            f"{leader[group_column]} "

            f"had the highest "

            f"{crop.lower()} "

            f"{metric.lower()}"
        )

        if year:

            answer += (
                f" in {year}"
            )

        answer += (

            f" with "

            f"{self.format_number(leader[metric_column])}"
        )

        if unit:

            answer += (
                f" {unit}"
            )

        answer += "."

        return answer

    def trend(
        self,
        result,
        unit
    ):

        df = result.result_data

        context = (
            result.query_context
        )

        crop = context["crop"]

        metric = context["metric"]

        metric_column = (
            result.metric_column
        )

        unit = self.normalize_unit(
            unit
        )

        start_value = (
            df.iloc[0][metric_column]
        )

        end_value = (
            df.iloc[-1][metric_column]
        )

        start_year = (
            df.iloc[0]["Year"]
        )

        end_year = (
            df.iloc[-1]["Year"]
        )

        if end_value > start_value:

            direction = (
                "increased"
            )

        elif end_value < start_value:

            direction = (
                "decreased"
            )

        else:

            direction = (
                "remained stable"
            )

        answer = (

            f"{crop.lower()} "

            f"{metric.lower()} "

            f"{direction} "

            f"from "

            f"{self.format_number(start_value)}"
        )

        if unit:

            answer += (
                f" {unit}"
            )

        answer += (

            f" in {start_year} "

            f"to "

            f"{self.format_number(end_value)}"
        )

        if unit:

            answer += (
                f" {unit}"
            )

        answer += (
            f" in {end_year}."
        )

        return answer

    def compare(
        self,
        result,
        unit
    ):

        df = result.result_data

        context = (
            result.query_context
        )

        crop = context["crop"]

        metric = context["metric"]

        year = context.get(
            "year"
        )

        metric_column = (
            result.metric_column
        )

        unit = self.normalize_unit(
            unit
        )

        rows = []

        for _, row in df.iterrows():

            value = (
                self.format_number(
                    row[
                        metric_column
                    ]
                )
            )

            state = row[
                "State Name"
            ]

            rows.append(
                f"{state}: {value}"
            )

        answer = (

            f"Comparison of "

            f"{crop.lower()} "

            f"{metric.lower()}"
        )

        if year:

            answer += (
                f" in {year}"
            )

        answer += (
            " -> "
        )

        answer += (
            " | ".join(rows)
        )

        if unit:

            answer += (
                f" {unit}"
            )

        answer += "."

        return answer

    def generate(
        self,
        plan,
        result,
        unit
    ):

        operation_map = {

            "aggregate":
            self.aggregate,

            "top_n":
            self.top_n,

            "top_1":
            self.top_n,

            "trend":
            self.trend,

            "compare":
            self.compare
        }

        return operation_map[
            plan.operation
        ](
            result,
            unit
        )