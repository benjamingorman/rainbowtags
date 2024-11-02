import argparse
import os
import barcode
import tempfile
import svgwrite
from xml.etree import ElementTree as ET


def reformat_svg(filepath, line_thickness=0.2):
    print("Reformatting svg...")
    dwg = svgwrite.Drawing("barcode_reformatted.svg", profile="tiny")
    tree = ET.parse(filepath)
    root = tree.getroot()
    # print(ET.tostring(root))

    # Find the 'barcode_group' element by id
    barcode_group = root.find(".//*[@id='barcode_group']")
    if barcode_group is None:
        raise ValueError("Barcode group not found in SVG.")

    # Find all rect elements within the barcode_group and replace them with lines
    for rect in barcode_group.findall("{http://www.w3.org/2000/svg}rect"):
        # Skip the border outline
        if not rect.attrib.get("x"):
            continue

        x = float(rect.attrib["x"].replace("mm", ""))
        y = float(rect.attrib["y"].replace("mm", ""))
        width = float(rect.attrib["width"].replace("mm", ""))
        height = float(rect.attrib["height"].replace("mm", ""))
        print("rect", x, y, width, height)

        # Calculate the number of lines to draw
        num_lines = round(width / line_thickness)

        # Create line elements
        for i in range(num_lines):
            line = dwg.line(
                start=(x + i * line_thickness, y),
                end=(x + i * line_thickness, y + height),
                stroke=svgwrite.rgb(0, 0, 0, "%"),
            )
            dwg.add(line)

    # Save the modified SVG to a new file
    print("Saved output")
    dwg.save()


def main():
    parser = argparse.ArgumentParser(description="Generate a barcode from text.")
    parser.add_argument("text", type=str, help="The text to encode in the barcode")
    args = parser.parse_args()

    code39 = barcode.Code39
    barcode_instance = code39(args.text, add_checksum=False)

    barcode_instance.save("barcode-tmp", options={"write_text": False})
    reformat_svg("barcode-tmp.svg")


if __name__ == "__main__":
    main()
