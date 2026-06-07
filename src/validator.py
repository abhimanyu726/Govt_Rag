class QueryValidator:
    """
    Validates generated QueryPlans
    before execution.
    """

    def __init__(self,metadata,schema_manager):

        self.metadata = metadata

        self.schema = schema_manager

    def validate(self,question,plan):
        """
        Validate generated plan.
        """

        # ---------------------------------
        # Out Of Scope
        # ---------------------------------

        if (
            plan.operation
            == "out_of_scope"
        ):

            raise ValueError(
                "Question is outside the "
                "scope of this agricultural dataset."
            )

        # ---------------------------------
        # Crop Validation
        # ---------------------------------

        if not self.schema.crop_exists(
            plan.crop
        ):

            available_crops = (
                ", ".join(
                    self.metadata["crops"][:10]
                )
            )

            raise ValueError(
                f"Crop '{plan.crop}' not found. "
                f"Available crops include: "
                f"{available_crops}"
            )

        # ---------------------------------
        # Metric Validation
        # ---------------------------------

        if not self.schema.metric_exists(
            plan.crop,
            plan.metric
        ):

            available_metrics = (
                self.schema.get_crop_metrics(
                    plan.crop
                )
            )

            raise ValueError(
                f"Metric '{plan.metric}' "
                f"is not available for "
                f"crop '{plan.crop}'. "
                f"Available metrics: "
                f"{available_metrics}"
            )

        # ---------------------------------
        # State Validation
        # ---------------------------------

        if (
            plan.state
            and
            plan.state
            not in self.metadata["states"]
        ):

            raise ValueError(
                f"State '{plan.state}' "
                f"not found in dataset."
            )

        # ---------------------------------
        # Compare State Validation
        # ---------------------------------

        if (
            plan.compare_with
            and
            plan.compare_with
            not in self.metadata["states"]
        ):

            raise ValueError(
                f"State '{plan.compare_with}' "
                f"not found in dataset."
            )

        # ---------------------------------
        # District Validation
        # ---------------------------------

        if (
            plan.district
            and
            plan.district
            not in self.metadata["districts"]
        ):

            raise ValueError(
                f"District '{plan.district}' "
                f"not found in dataset."
            )

        # ---------------------------------
        # Year Validation
        # ---------------------------------

        if (
            plan.year
            and
            plan.year
            not in self.metadata["years"]
        ):

            min_year = min(
                self.metadata["years"]
            )

            max_year = max(
                self.metadata["years"]
            )

            raise ValueError(
                f"Year '{plan.year}' is not available. "
                f"Dataset contains years from "
                f"{min_year} to {max_year}."
            )

        # ---------------------------------
        # Compare Validation
        # ---------------------------------

        if (
            plan.operation
            == "compare"
        ):

            if not plan.state:

                raise ValueError(
                    "Compare operation "
                    "requires state."
                )

            if not plan.compare_with:

                raise ValueError(
                    "Compare operation "
                    "requires compare_with."
                )

            if (
                plan.state
                == plan.compare_with
            ):

                raise ValueError(
                    "States being compared "
                    "must differ."
                )

        # ---------------------------------
        # Top N Validation
        # ---------------------------------

        if (
            plan.operation
            == "top_n"
        ):

            if (
                plan.top_n is None
                or
                plan.top_n <= 0
            ):

                raise ValueError(
                    "top_n must be greater "
                    "than zero."
                )

        # ---------------------------------
        # Top 1 Validation
        # ---------------------------------

        if (
            plan.operation
            == "top_1"
        ):

            if (
                plan.top_n is not None
                and
                plan.top_n <= 0
            ):

                raise ValueError(
                    "top_n must be greater "
                    "than zero."
                )

        return True