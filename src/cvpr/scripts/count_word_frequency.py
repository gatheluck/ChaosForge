import json
import pathlib
from collections import Counter
from typing import Dict, Final

from src.cvpr.parser import Paper


def count_word_frequency(
    paper_info_path: pathlib.Path,
) -> Dict[str, int]:
    """

    Args:
        paper_info_path (pathlib.Path):

    Returns:
        Dict[str, int]: A dictionally of word frequency.

    """
    # Check JSON file existence.
    if not paper_info_path.exists():
        error_message: Final = f"This scripts requires `{str(paper_info_path)}`."
        raise FileNotFoundError(error_message)

    with paper_info_path.open("r") as f:
        papers: Final = [Paper.model_validate(p) for p in json.load(f)]

    # Concat all title.
    source_text: Final = " ".join([paper.title for paper in papers])

    return {k: v for k, v in Counter(source_text.split(" ")).most_common()}


if __name__ == "__main__":
    year: int = 2023
    paper_info_path = pathlib.Path(f"./data/cvpr/papers{year}.json")
    output_path: Final = pathlib.Path(f"./data/cvpr/frequency{year}.json")
    with output_path.open("w") as f:
        json.dump(
            count_word_frequency(paper_info_path), f, ensure_ascii=False, indent=4
        )
