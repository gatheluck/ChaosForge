"""

This script generate json file which includes all CVPR 2023 papers info.

"""
import json
import logging
import pathlib
from typing import Final

from src.cvpr.parser import get_paper_page_urls, parse_paper_page

logger: Final = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main(
    year: int,
    output_dir: pathlib.Path = pathlib.Path("./data/cvpr/"),
) -> None:
    urls: Final = get_paper_page_urls(year)
    logger.info(f"{len(urls)} urls are founds.")

    papers = list()
    for i, url in enumerate(urls):
        logger.info(f"[{i+1}/{len(urls)}] parsing `{url}`.")
        paper = parse_paper_page(url, year)
        papers.append(paper.model_dump(mode="json"))

    output_path: Final = output_dir / f"papers{year}.json"
    with output_path.open("w") as f:
        json.dump(papers, f)


if __name__ == "__main__":
    main(2023)
