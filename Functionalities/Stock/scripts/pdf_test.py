import random
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import red, black
from pathlib import Path

# Define the number of items
num_items = 60
items_per_page = 30  # Number of items per page

# Define the path for the PDF
pdf_path = Path(__file__).resolve().parents[1] / "data" / "random_items.pdf"

# Create a canvas object
canvas = Canvas(str(pdf_path))

# Set the starting position for drawing text
y_position = 800  # Starting Y position from the top
item_width = 150  # X position for the random number

# Loop to create lines of text
for i in range(1, num_items + 1):
    n = random.randint(0, 10)  # Generate a random number from 0 to 10
    
    # Draw the item text in black
    canvas.setFillColor(black)
    canvas.drawString(100, y_position, f"item {i}: ")
    
    # Change the color of the random number if it's less than 5
    if n < 5:
        canvas.setFillColor(red)
    else:
        canvas.setFillColor(black)
        
    # Draw the random number
    canvas.drawString(item_width, y_position, str(n))
    
    # Move down for the next line
    y_position -= 20  # Decrease Y position for the next line
    
    # Check if we need to create a new page
    if i % items_per_page == 0 and i < num_items:
        canvas.showPage()  # Create a new page
        y_position = 800  # Reset Y position for the new page

# Save the canvas to create the PDF
canvas.save()