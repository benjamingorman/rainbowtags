"""
Script to generate barcode SVG as a bunch of straight lines, for a laser
cutter to use. Cutting multiple straight lines close together rather than engraving
gives us better barcode quality.
"""

import argparse
import os
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET

import barcode
import svgwrite


def reformat_svg(
    input_svg: str | os.PathLike,
    output_svg_path: str | os.PathLike,
    width_mm=45,
    height_mm=16,
    padding_x=5,
    padding_y=5,
):
    """Reformat an existing barcode SVG to make it a bunch of straight lines."""
    print("Reformatting svg...")
    total_width = width_mm + 2 * padding_x
    total_height = height_mm + 2 * padding_y

    dwg = svgwrite.Drawing(
        str(output_svg_path),
        profile="tiny",
        size=(f"{total_width}mm", f"{total_height}mm"),
        viewBox=(f"0 0 {total_width} {total_height}"),
    )

    tree = ET.parse(input_svg)
    root = tree.getroot()

    # Find the 'barcode_group' element by id
    barcode_group = root.find(".//*[@id='barcode_group']")
    if barcode_group is None:
        raise ValueError("Barcode group not found in SVG.")

    rects = barcode_group.findall("{http://www.w3.org/2000/svg}rect")

    # Find the min/max x value so we can scale the barcode size
    min_x = None
    for rect in rects:
        # Skip the border outline
        if not rect.attrib.get("x"):
            continue
        min_x = float(rect.attrib["x"].replace("mm", ""))
        break

    max_x = None
    for rect in reversed(rects):
        # Skip the border outline
        if not rect.attrib.get("x"):
            continue
        max_x = float(rect.attrib["x"].replace("mm", "")) + float(
            rect.attrib["width"].replace("mm", "")
        )
        break

    assert min_x, max_x

    x_scale = width_mm / (max_x - min_x)
    print("min_x", min_x, "max_x", max_x, "x_scale", x_scale)

    # Find all rect elements within the barcode_group and replace them with lines
    for rect in rects:
        # Skip the border outline
        if not rect.attrib.get("x"):
            continue

        x = float(rect.attrib["x"].replace("mm", ""))
        y = float(rect.attrib["y"].replace("mm", ""))

        # Ensure origin is 0,0
        x = (x - min_x) * x_scale + padding_x
        y = padding_y

        width = float(rect.attrib["width"].replace("mm", ""))
        height = height_mm
        print("rect", x, y, width, height)

        if width == 0.2:
            # Thin line
            num_lines = 1
        else:
            # Thick line
            num_lines = 4

        line_thickness = (width * x_scale) / num_lines

        # Create line elements
        for i in range(num_lines):
            line = dwg.line(
                start=(x + (i + 0.5) * line_thickness, y),
                end=(x + (i + 0.5) * line_thickness, y + height),
                stroke=svgwrite.rgb(0, 0, 0, "%"),
                stroke_width="0.1px",
            )
            dwg.add(line)

    # Save the modified SVG to a new file
    print("Saved output")
    dwg.save()


def create_barcode_svg(text: str, output_svg_path: str | os.PathLike):
    """Create a barcode SVG file."""

    # First we use python-barcode to get an SVG.
    barcode_instance = barcode.Code39(text, add_checksum=False)

    with TemporaryDirectory() as tmp_dir:
        tmp_barcode_path = os.path.join(tmp_dir, "barcode")
        barcode_instance.save(tmp_barcode_path, options={"write_text": False})

        # Then we modify the SVG to be suitable to cut on a laser cutter.
        reformat_svg(tmp_barcode_path + ".svg", output_svg_path)


def main():
    parser = argparse.ArgumentParser(description="Generate a barcode from text.")
    parser.add_argument("text", type=str, help="The text to encode in the barcode.")
    parser.add_argument(
        "-o",
        "--output-file",
        default="barcode.svg",
        type=str,
        help="Path to output SVG file.",
    )
    args = parser.parse_args()

    create_barcode_svg(args.text, output_svg_path=args.output_file)


if __name__ == "__main__":
    main()
