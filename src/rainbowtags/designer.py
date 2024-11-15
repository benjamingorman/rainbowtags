import svgwrite


def generate_svg(filename):
    # Create an SVG drawing
    dwg = svgwrite.Drawing(filename, size=("50mm", "30mm"))

    # Add a rectangle with no fill
    dwg.add(dwg.rect(insert=(0, 0), size=("50mm", "30mm"), fill="none", stroke="black"))

    # Add a circle inside the rectangle with no fill
    dwg.add(dwg.circle(center=("25mm", "15mm"), r="10mm", fill="none", stroke="black"))

    # Save the SVG file
    dwg.save()


if __name__ == "__main__":
    generate_svg("output.svg")
