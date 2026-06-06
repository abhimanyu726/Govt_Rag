SYSTEM_PROMPT = """
You are an agricultural dataset query planner.

Your only responsibility is to create
a valid QueryPlan.

You never answer questions.

You never calculate values.

Available operations:

aggregate
top_n
top_1
trend
compare
out_of_scope

Use:

aggregate
for totals.

top_n
for rankings.

top_1
for highest / lowest.

trend
for changes over time.

compare
for comparing two states.

If a question cannot be answered
using the provided dataset metadata,
return:

operation="out_of_scope"

and leave all other fields empty.

Only use crops,
metrics,
states,
districts,
and years that appear
in metadata.

Return only a QueryPlan.
"""


def build_prompt(
    question: str,
    metadata: dict
) -> str:
    """
    Build dataset-aware prompt.
    """

    crop_lines = []

    for crop, metrics in metadata[
        "crop_metric_map"
    ].items():

        metric_list = ", ".join(
            metrics.keys()
        )

        crop_lines.append(
            f"{crop}: {metric_list}"
        )

    crops_section = "\n".join(
        crop_lines
    )

    states_section = ", ".join(
        metadata["states"]
    )

    years_section = (
        f"{min(metadata['years'])}"
        f" - "
        f"{max(metadata['years'])}"
    )

    return f"""
AVAILABLE CROPS AND METRICS

{crops_section}


AVAILABLE STATES

{states_section}


AVAILABLE YEARS

{years_section}


QUESTION

{question}


Generate a QueryPlan.
"""