from src.models import FinalResponse

from src.parser import QueryPlanner

from src.executor import QueryExecutor

from src.charts import ChartGenerator

from src.answer_generator import AnswerGenerator


class AgriculturePipeline:
    """
    End-to-end analytics pipeline.

    User Question
        |
    Query Planning
        |
    Validation
        |
    Dataset Execution
        |
    Visualization
        |
    Natural Language Answer
        |
    Final Response
    """

    def __init__(self,dataframe,schema_manager,metadata,api_key,model="gpt-4.1-mini"):
        self.schema = schema_manager
        self.planner = QueryPlanner(
            metadata=metadata,
            schema_manager=schema_manager,
            api_key=api_key,
            model=model
        )
        self.executor = QueryExecutor(
            dataframe=dataframe,
            schema_manager=schema_manager
        )
        self.chart_generator = (
            ChartGenerator()
        )
        self.answer_generator = (
            AnswerGenerator()
        )

    def build_provenance(self,plan,result):
        """
        Build provenance information.
        """
        return {
            "operation": plan.operation,
            "crop": plan.crop,
            "metric": plan.metric,
            "year": plan.year,
            "state": plan.state,
            "district": plan.district,
            "dataset_column": result.metric_column,
            "rows_processed": result.summary.get(
                "rows",
                0
            )
        }

    def build_preview(self,result):
        """
        Create UI preview.
        """
        preview = (
            result.preview_data
        )
        try:
            if hasattr(
                preview,
                "head"
            ):
                return preview.head(
                    10
                )
            return preview
        except Exception:
            return preview

    def run(self,question: str) -> FinalResponse:
        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )
        plan = (
            self.planner
            .create_plan(
                question
            )
        )
        result = (
            self.executor
            .execute(
                plan
            )
        )
        unit = (
            self.schema
            .get_unit(
                plan.crop,
                plan.metric
            )
        )
        chart_path = (
            self.chart_generator
            .generate(
                result
            )
        )
        answer = (
            self.answer_generator
            .generate(
                plan,
                result,
                unit
            )
        )
        provenance = (
            self.build_provenance(
                plan,
                result
            )
        )
        preview = (
            self.build_preview(
                result
            )
        )
        return FinalResponse(
            answer=answer,
            chart_path=chart_path,
            query_plan=plan.model_dump(),
            provenance=provenance,
            result_preview=preview
        )

    def run_safe(self,question: str):
        """
        Safe execution wrapper.

        Returns structured errors
        instead of raising exceptions.
        """
        try:
            response = self.run(
                question
            )
            return {
                "success": True,
                "data": response
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
