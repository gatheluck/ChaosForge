import json
import pathlib
from typing import Final, Set

from wordcloud import STOPWORDS, WordCloud

from src.cvpr.parser import Paper


def main(
    paper_info_path: pathlib.Path,
    source_text_path: pathlib.Path,
    image_save_path: pathlib.Path,
    stopwords: Set[str],
) -> None:
    # Check JSON file existence.
    if not paper_info_path.exists():
        error_message: Final = f"This scripts requires `{str(paper_info_path)}`."
        raise FileNotFoundError(error_message)

    with paper_info_path.open("r") as f:
        papers: Final = [Paper.model_validate(p) for p in json.load(f)]

    # Concat all title.
    source_text: Final = " ".join([paper.title for paper in papers])
    with source_text_path.open("w") as f:
        f.write(source_text)

    # Read source from path.
    text: Final = source_text_path.read_text()

    wordcloud: Final = WordCloud(
        width=1600,
        height=800,
        max_font_size=120,
        min_font_size=12,
        background_color="black",
        stopwords=stopwords,
    ).generate(text)
    wordcloud.to_file(str(image_save_path))


if __name__ == "__main__":
    year: int = 2023
    paper_info_path: Final = pathlib.Path(f"./data/cvpr/papers{year}.json")
    source_text_path: Final = pathlib.Path(f"./data/cvpr/wordcloud_source{year}.txt")
    image_save_path: Final = pathlib.Path(f"./data/cvpr/wordcloud{year}.png")
    stopwords = set(STOPWORDS)
    stopwords.update(
        {
            "Based",
            "Using",
            "via",
            "Aware",
            "Level",
            "Improving",
            "Driven",
            "New",
            "End",
            "Task",
            "Event",
            "Class",
            "Part",
            "Without",
            "Toward",
            "Towards",
        }
    )
    main(
        paper_info_path,
        source_text_path,
        image_save_path,
        stopwords,
    )
