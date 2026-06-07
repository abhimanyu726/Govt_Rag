import re


class SchemaManager:
    """
    Discovers dataset schema dynamically.

    Builds:

    crop_metric_map

    Example:

    {
        "RICE": {
            "AREA": "RICE AREA (1000 ha)",
            "PRODUCTION": "RICE PRODUCTION (1000 tons)",
            "YIELD": "RICE YIELD (Kg per ha)"
        }
    }

    metric_units

    Example:

    {
        "RICE PRODUCTION (1000 tons)": "1000 tons"
    }
    """

    def __init__(self,dataframe):

        self.df = dataframe

        self.crop_metric_map = {}

        self.metric_units = {}

        self._build_schema()

    def _build_schema(self):

        pattern = re.compile(
            r"^(.*?)\s+(AREA|PRODUCTION|YIELD)\s*(\(.*\))?$"
        )

        for column in self.df.columns:

            match = pattern.match(
                column
            )

            if not match:
                continue

            crop = (
                match
                .group(1)
                .strip()
            )

            metric = (
                match
                .group(2)
                .strip()
            )

            unit = (
                match
                .group(3)
            )

            if crop not in self.crop_metric_map:

                self.crop_metric_map[
                    crop
                ] = {}

            self.crop_metric_map[
                crop
            ][metric] = column

            if unit:

                self.metric_units[
                    column
                ] = (
                    unit
                    .replace("(", "")
                    .replace(")", "")
                )

    def crop_exists(self,crop: str) -> bool:

        return (
            crop
            in
            self.crop_metric_map
        )

    def metric_exists(self,crop: str,metric: str) -> bool:

        if crop not in self.crop_metric_map:

            return False

        return (
            metric
            in
            self.crop_metric_map[crop]
        )

    def get_column(self,crop: str,metric: str):

        return (

            self.crop_metric_map

            .get(crop, {})

            .get(metric)
        )

    def get_unit(self,crop: str,metric: str):

        column = self.get_column(
            crop,
            metric
        )

        if column is None:

            return None

        return self.metric_units.get(
            column
        )

    def get_states(self):

        return sorted(

            self.df["State Name"]

            .dropna()

            .unique()

            .tolist()
        )

    def get_districts(self):

        return sorted(

            self.df["Dist Name"]

            .dropna()

            .unique()

            .tolist()
        )

    def get_years(self):

        return sorted(

            self.df["Year"]

            .dropna()

            .unique()

            .tolist()
        )

    def get_crops(self):

        return sorted(
            self.crop_metric_map.keys()
        )

    def get_crop_metrics(self,crop: str):

        return list(

            self.crop_metric_map

            .get(crop, {})

            .keys()
        )

    def metadata(self):

        return {

            "states":
            self.get_states(),

            "districts":
            self.get_districts(),

            "years":
            self.get_years(),

            "crops":
            self.get_crops(),

            "crop_metric_map":
            self.crop_metric_map
        }