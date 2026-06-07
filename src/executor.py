import pandas as pd

from src.models import QueryPlan, ExecutionResult


class QueryExecutor:
    """
    Executes validated QueryPlans
    against the dataset.
    """

    def __init__(self,dataframe: pd.DataFrame,schema_manager):

        self.df = dataframe

        self.schema = schema_manager

    def get_metric_column(self,plan: QueryPlan) -> str:

        column = self.schema.get_column(
            plan.crop,
            plan.metric
        )

        if column is None:

            raise ValueError(
                f"No column found for "
                f"{plan.crop} {plan.metric}"
            )

        return column

    def build_context(self,plan: QueryPlan) -> dict:

        return {

            "crop":
            plan.crop,

            "metric":
            plan.metric,

            "year":
            plan.year,

            "state":
            plan.state,

            "district":
            plan.district,

            "operation":
            plan.operation
        }

    def apply_filters(self,dataframe: pd.DataFrame,plan: QueryPlan) -> pd.DataFrame:

        df = dataframe.copy()

        if plan.year is not None:

            df = df[
                df["Year"]
                == plan.year
            ]

        if plan.state:

            df = df[
                df["State Name"]
                == plan.state
            ]

        if plan.district:

            df = df[
                df["Dist Name"]
                == plan.district
            ]

        if df.empty:

            raise ValueError(
                "No matching records found."
            )

        return df

    def aggregate(self,plan: QueryPlan) -> ExecutionResult:

        metric_column = (
            self.get_metric_column(
                plan
            )
        )

        filtered = (
            self.apply_filters(
                self.df,
                plan
            )
        )

        value = (

            filtered[
                metric_column
            ]

            .fillna(0)

            .sum()
        )

        return ExecutionResult(

            result_data=value,

            preview_data=value,

            metric_column=metric_column,

            chart_type=None,

            summary={
                "operation":
                "aggregate",

                "rows":
                len(filtered),

                "column":
                metric_column
            },

            query_context=
            self.build_context(plan)
        )

    def top_n(self,plan: QueryPlan) -> ExecutionResult:

        metric_column = (
            self.get_metric_column(
                plan
            )
        )

        filtered = (
            self.apply_filters(
                self.df,
                plan
            )
        )

        group_column = (
            plan.group_by
            if plan.group_by
            else "State Name"
        )

        result = (

            filtered

            .groupby(
                group_column
            )[metric_column]

            .sum()

            .reset_index()

            .sort_values(
                metric_column,
                ascending=False
            )

            .head(
                plan.top_n
            )
        )

        return ExecutionResult(

            result_data=result,

            preview_data=result,

            metric_column=metric_column,

            chart_type="bar",

            summary={
                "operation":
                "top_n",

                "rows":
                len(filtered),

                "column":
                metric_column
            },

            query_context=
            self.build_context(plan)
        )

    def top_1(self,plan: QueryPlan) -> ExecutionResult:

        plan.top_n = 1

        return self.top_n(
            plan
        )

    def trend(self,plan: QueryPlan) -> ExecutionResult:

        metric_column = (
            self.get_metric_column(
                plan
            )
        )

        filtered = (
            self.apply_filters(
                self.df,
                plan
            )
        )

        result = (

            filtered

            .groupby(
                "Year"
            )[metric_column]

            .sum()

            .reset_index()

            .sort_values(
                "Year"
            )
        )

        return ExecutionResult(

            result_data=result,

            preview_data=result,

            metric_column=metric_column,

            chart_type="line",

            summary={
                "operation":
                "trend",

                "rows":
                len(filtered),

                "column":
                metric_column
            },

            query_context=
            self.build_context(plan)
        )

    def compare(self,plan: QueryPlan) -> ExecutionResult:

        metric_column = (
            self.get_metric_column(
                plan
            )
        )

        states = [

            plan.state,

            plan.compare_with
        ]

        filtered = (

            self.df[
                self.df[
                    "State Name"
                ].isin(states)
            ]
        )

        if plan.year is not None:

            filtered = (

                filtered[
                    filtered["Year"]
                    == plan.year
                ]
            )

        if filtered.empty:

            raise ValueError(
                "No comparison data found."
            )

        result = (

            filtered

            .groupby(
                "State Name"
            )[metric_column]

            .sum()

            .reset_index()

            .sort_values(
                metric_column,
                ascending=False
            )
        )

        return ExecutionResult(

            result_data=result,

            preview_data=result,

            metric_column=metric_column,

            chart_type="bar",

            summary={
                "operation":
                "compare",

                "rows":
                len(filtered),

                "column":
                metric_column
            },

            query_context=
            self.build_context(plan)
        )

    def execute(self,plan: QueryPlan) -> ExecutionResult:

        operation_map = {

            "aggregate":
            self.aggregate,

            "top_n":
            self.top_n,

            "top_1":
            self.top_1,

            "trend":
            self.trend,

            "compare":
            self.compare
        }

        if (
            plan.operation
            not in operation_map
        ):

            raise ValueError(
                f"Unsupported operation: "
                f"{plan.operation}"
            )

        return operation_map[
            plan.operation
        ](plan)