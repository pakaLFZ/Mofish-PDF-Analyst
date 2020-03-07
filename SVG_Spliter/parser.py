
"""Parse SVG"""
import re
import typing


def is_blank(svg: str) -> bool:
    """Check if passed `svg` is blank page"""
    for indicator in ["BLANK PAGE", "READ THESE INSTRUCTIONS FIRST"]:
        if indicator in svg:
            return True
    return False


def get_page_number_match(svg: str) -> re.Match:
    """Extract page number match from svg page with regex
    Group 1 should be a int (if nothing goes wrong)
    """
    match = re.match(
        r"\<svg:span>.*font-family=\"g_font_2\".*fill=\"rgb(0,0,0)\">(\d)+</svg:tspan>",
        svg
    )
    if match is None:
        raise ValueError("Page number not found")
    return match


def parse_svg_page(svg: str, last_question_number: int) -> dict:
    """Parse svg string"""
    new_question_number: int = last_question_number

    return {
        "lastquestionnumber": last_question_number
    }


def prepare_svg_pages(svg_page_list: List[str]) -> dict:
    """Sort a svg list and prepare metadata"""
    valid_svgs = {}
    for svg in svg_page_list:
        if is_blank(svg):
            continue
        page_number_match = get_page_number_match(svg)
        try:
            page_number: int = int(page_number_match.group(1))
        except ValueError: # raise error if can't convert to int
            raise ValueError("Page number string \"{}\" invalid".format(
                page_number_match.group(1)))
        # get the end pos of the matching to ease parsing
        page_number_end = page_number_match.end(0)
        


def parse_pages(svg_list: typing.Dict[int: dict]):
    """Parse a sorted list of svgs
    """
    page_datas = {}
    # record the last matched question number to ease question matching
    last_question_number = 0
    for count, page in svg_list.items():
        page_datas[count] = parse_svg_page(page["svg"], last_question_number)
