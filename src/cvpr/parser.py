import logging
from typing import Final, List

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, HttpUrl

logger: Final = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Paper(BaseModel):
    """

    Pydantic model which stores single paper infomation.

    """

    title: str
    author: str
    abstract: str
    cvf: HttpUrl
    pdf: HttpUrl


def get_paper_page_urls(year: int) -> List[str]:
    """

    Return a list of CVF page URL.
    The list includes all papers accepted by CVPR.

    Args:
        year (int): A target year.

    """

    cvf_root_url: Final = "https://openaccess.thecvf.com"
    cvf_all_paper_url: Final = cvf_root_url + f"/CVPR{year}?day=all"

    html: Final = requests.get(cvf_all_paper_url).text
    bs: Final = BeautifulSoup(html, "html.parser")
    parsed_tags = bs.select(".ptitle > a")
    return [cvf_root_url + parsed_tag.get("href") for parsed_tag in parsed_tags]


def parse_paper_page(page_url: str, year: int) -> Paper:
    """

    Parse a paper page and return Paper object.

    """

    html: Final = requests.get(page_url).text
    bs: Final = BeautifulSoup(html, "html.parser")

    cvf: Final = page_url
    pdf: Final = (
        f"https://openaccess.thecvf.com/content/CVPR{year}/papers/"
        + page_url.removesuffix(".html").split("/")[-1]
        + (".pdf")
    )

    try:
        title: Final = bs.select_one("#papertitle").text.strip()
        author: Final = bs.select_one("#authors b").text.strip()
        abstract: Final = bs.select_one("#abstract").text.strip()

        return Paper(
            title=title,
            author=author,
            abstract=abstract,
            cvf=cvf,  # type: ignore
            pdf=pdf,  # type: ignore
        )
    except AttributeError:
        logger.warn(f"Failed to parse `{page_url}`.")
        return Paper(
            title="",
            author="",
            abstract="",
            cvf=cvf,  # type: ignore
            pdf=pdf,  # type: ignore
        )
