from pathlib import Path
from datetime import datetime


EXPORTS_DIR = Path("exports")


def export_answer(
    question,
    sources,
    answer
):
    """
    Export a RAG interaction to markdown.

    Parameters
    ----------
    question : str
    sources : list[dict]
    answer : str

    Returns
    -------
    Path
        Path to created markdown file.
    """

    EXPORTS_DIR.mkdir(
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    export_file = (
        EXPORTS_DIR
        / f"answer_{timestamp}.md"
    )

    markdown = []

    markdown.append(
        "# Local RAG Export\n"
    )

    markdown.append(
        "## Question\n"
    )

    markdown.append(
        f"{question}\n"
    )

    markdown.append(
        "## Retrieved Sources\n"
    )

    for i, source in enumerate(
        sources,
        start=1
    ):

        filename = source.get(
            "filename",
            "Unknown"
        )

        text = source.get(
            "text",
            ""
        )

        markdown.append(
            f"### Source {i}\n"
        )

        markdown.append(
            f"**File:** {filename}\n"
        )

        markdown.append(
            "```text"
        )

        markdown.append(
            text
        )

        markdown.append(
            "```\n"
        )

    markdown.append(
        "## Answer\n"
    )

    markdown.append(
        answer
    )

    with open(
        export_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(markdown)
        )

    return export_file