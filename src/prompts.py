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

Use aggregate for totals.

Use top_n for rankings.

Use top_1 for highest or lowest entities.

Use trend for changes over time.

Use compare for comparing two states.

IMPORTANT:

When the user asks:

- Which year had highest production?
- In which year was production maximum?
- Peak production year
- Highest yield year
- When was production maximum

Use:

operation="top_1"
group_by="Year"

When the user asks:

- Which state produced the most?
- Highest producing state
- Top producing state

Use:

group_by="State Name"

When the user asks:

- Which district produced the most?
- Highest producing district

Use:

group_by="Dist Name"

Never generate a year
outside the available range.

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


def build_prompt(question: str,metadata: dict) -> str:

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