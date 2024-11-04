"""
This module's objective is to contain functions for PDF creation for 
stock reporting.
"""

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import red, black
from datetime import date
from pathlib import Path

from .data_loader import Packing, Material


def create_title(canvas: Canvas, title: str, font: str) -> None:
    """
    Function that creates a title in a PDF report.
    The title is big and in the center of the page.

    Args:
        - canvas (Canvas): Canvas object to draw the title.
        - title (str): Title to include in the report.

    Returns: None
    """

    title_font = "Times-Bold" if font == "Times-Roman" else font
    date_font = "Times-Roman" if font == "Times-Bold" else font

    canvas.setFont(font, 36)  # Set the font size
    text_width = canvas.stringWidth(title, title_font, 36)  # Get the width of the text

    # Calculate the X position to center the text
    x_position = (canvas._pagesize[0] - text_width) / 2

    current_date = date.today().strftime("%d/%m/%Y")

    date_width = canvas.stringWidth(current_date, date_font, 12)

    x_position_date = (canvas._pagesize[0] - date_width) / 2

    # Draw the title in black
    canvas.setFillColor(black)
    canvas.drawString(x_position, 410, title)
    canvas.setFont(date_font, 12)
    canvas.drawString(x_position_date, 390, current_date)


def create_packing_report(
    canvas: Canvas, packing: Packing, line_spacing: int, item_width: int, font: str
) -> None:
    """
    Function that adds the data of a packing to a PDF report.

    Args:
        - canvas (Canvas): Canvas object to draw the packing data.
        - packing (Packing): Packing object to include in the report.
        - line_spacing (int): Spacing between lines in the report.
        - item_width (int): X position for the stock status.

    Returns: None
    """
    canvas.showPage()

    y_position = 800

    font_size = 12
    item_width = max(
        [
            canvas.stringWidth(f"{item.name}: ", font, font_size)
            for item in packing.materials
        ]
    )

    indentation = 120

    # Draw the packing name in black
    canvas.setFillColor(black)
    canvas.drawString(100, y_position, f"Packing: {packing.name}")

    # Move down for the next line
    y_position -= line_spacing  # Decrease Y position for the next line

    for item in packing.materials:
        canvas.setFillColor(black)
        canvas.drawString(indentation, y_position, f"{item.name}: ")

        if not item.enough_stock:
            canvas.setFillColor(red)
        else:
            canvas.setFillColor(black)

        canvas.drawString(
            indentation + item_width + 10,
            y_position,
            f"{item.stock} unidades / {item.minimum_stock} mínimas / {item.order_ammount} máximas",
        )

        y_position -= line_spacing

        if y_position < 50:
            canvas.showPage()
            y_position = 800

        canvas.setFillColor(black)


def create_stock_report(
    pdf_path: Path,
    packings: list[Packing],
    line_spacing: int = 20,
    item_width: int = 200,
) -> None:
    """
    Function that creates a PDF report of the stock.

    Args:
        - pdf_path (Path): Path to save the PDF file.
        - packings (list[Packing]): List of packings to include in the report.
        - line_spacing (int): Spacing between lines in the report.
        - item_width (int): X position for the stock status.

    Returns: None
    """

    # Create a canvas object
    canvas = Canvas(str(pdf_path))

    font = "Times-Roman"

    create_title(canvas, "Stock Report", font)

    for packing in packings:
        packing.round_values()
        create_packing_report(canvas, packing, line_spacing, item_width, font)

    # Save the canvas to create the PDF
    canvas.save()
