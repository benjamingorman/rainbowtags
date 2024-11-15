"""
This module provides functionality to generate an SVG file for a tag design.
It uses the svgwrite library to create an SVG with a specified tag design,
including a rectangle and a circle. The design parameters are specified using
the TagDesign class, and the SVG is saved to a file.
"""

import argparse
import xml.etree.ElementTree as ET

from pydantic import BaseModel
import svgwrite

from rainbowtags.barcode import create_barcode_svg


TAG_WIDTH_MM = 85
TAG_HEIGHT_MM = 30

HOLE_RADIUS = 2
HOLE_PADDING = 2.5

RR_LOGO_WIDTH = 23.5

PADDING = 10
FRONT_BACK_PADDING = 20


class TagDesign(BaseModel):
    """The parameters to use for a tag design."""

    name: str | None
    mobile_number: str | None
    barcode_number: str


def mm(x: float) -> str:
    return f"{x}mm"


def create_tag_svg(output_filename: str, tag_design: TagDesign):
    # Create an SVG drawing
    front_rect_x = PADDING
    front_rect_y = PADDING

    dwg = svgwrite.Drawing(
        output_filename,
        size=(
            mm(TAG_WIDTH_MM + 2 * PADDING),
            mm(TAG_HEIGHT_MM * 2 + FRONT_BACK_PADDING + 2 * PADDING),
        ),
    )

    # FRONT
    # First rectangle
    front_rect_x = PADDING
    front_rect_y = PADDING
    dwg.add(
        dwg.rect(
            insert=(mm(front_rect_x), mm(front_rect_y)),
            size=(mm(TAG_WIDTH_MM), mm(TAG_HEIGHT_MM)),
            fill="none",
            stroke="black",
        )
    )

    # Inner hole for ring on the first rectangle
    dwg.add(
        dwg.circle(
            center=(
                mm(front_rect_x + HOLE_PADDING + HOLE_RADIUS),
                mm(front_rect_y + HOLE_PADDING + HOLE_RADIUS),
            ),
            r=mm(HOLE_RADIUS),
            fill="none",
            stroke="black",
        )
    )

    # Barcode

    # BACK
    # Second rectangle
    back_rect_x = PADDING
    back_rect_y = PADDING + TAG_HEIGHT_MM + FRONT_BACK_PADDING

    dwg.add(
        dwg.rect(
            insert=(mm(back_rect_x), mm(back_rect_y)),
            size=(mm(TAG_WIDTH_MM), mm(TAG_HEIGHT_MM)),
            fill="none",
            stroke="black",
        )
    )

    # Inner hole for ring on the second rectangle
    dwg.add(
        dwg.circle(
            center=(
                mm(back_rect_x + TAG_WIDTH_MM - HOLE_PADDING - HOLE_RADIUS),
                mm(back_rect_y + HOLE_PADDING + HOLE_RADIUS),
            ),
            r=mm(HOLE_RADIUS),
            fill="none",
            stroke="black",
        )
    )

    # Save the SVG file
    dwg.save()
    print("Wrote", output_filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output-file", default="tag.svg", help="Output file path"
    )
    parser.add_argument("--name", help="Person name")
    parser.add_argument("--mobile-number", help="Person mobile number")
    parser.add_argument("--barcode-number", required=True, help="Person barcode number")
    args = parser.parse_args()

    tag_design = TagDesign(
        name=args.name,
        mobile_number=args.mobile_number,
        barcode_number=args.barcode_number,
    )
    create_tag_svg(args.output_file, tag_design)


if __name__ == "__main__":
    main()
