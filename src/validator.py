class QueryValidator:
    """
    Validates generated QueryPlans.
    """

    def __init__(
        self,
        metadata,
        schema_manager
    ):

        self.metadata = metadata

        self.schema = schema_manager

    def validate(
        self,
        question,
        plan
    ):
        """
        Validate generated plan.
        """

        if (
            plan.operation
            == "out_of_scope"
        ):

            raise ValueError(
                "Question is outside the "
                "scope of this dataset."
            )

        if not self.schema.crop_exists(
            plan.crop
        ):

            raise ValueError(
                f"Crop '{plan.crop}' "
                f"not found."
            )

        if not self.schema.metric_exists(
            plan.crop,
            plan.metric
        ):

            raise ValueError(
                f"Metric '{plan.metric}' "
                f"is not available for "
                f"crop '{plan.crop}'."
            )

        if (
            plan.state
            and
            plan.state
            not in self.metadata["states"]
        ):

            raise ValueError(
                f"State '{plan.state}' "
                f"not found."
            )

        if (
            plan.compare_with
            and
            plan.compare_with
            not in self.metadata["states"]
        ):

            raise ValueError(
                f"State '{plan.compare_with}' "
                f"not found."
            )

        if (
            plan.district
            and
            plan.district
            not in self.metadata["districts"]
        ):

            raise ValueError(
                f"District '{plan.district}' "
                f"not found."
            )

        if (
            plan.year
            and
            plan.year
            not in self.metadata["years"]
        ):

            raise ValueError(
                f"Year '{plan.year}' "
                f"not found."
            )

        if (
            plan.operation == "compare"
            and
            not plan.state
        ):

            raise ValueError(
                "Compare operation "
                "requires state."
            )

        if (
            plan.operation == "compare"
            and
            not plan.compare_with
        ):

            raise ValueError(
                "Compare operation "
                "requires compare_with."
            )

        if (
            plan.operation == "compare"
            and
            plan.state == plan.compare_with
        ):

            raise ValueError(
                "States being compared "
                "must differ."
            )

        if (
            plan.operation == "top_n"
            and
            (
                plan.top_n is None
                or
                plan.top_n <= 0
            )
        ):

            raise ValueError(
                "top_n must be greater "
                "than zero."
            )

        return True