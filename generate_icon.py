# generate_icon.py
import os
from PIL import Image, ImageDraw, ImageFont

def create_icon():
    size = 256
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    white = (255, 255, 255, 255)
    orange = (255, 120, 0, 255)
    text_color = (30, 30, 30, 255)

    padding = 8
    draw.ellipse([(padding, padding), (size-padding, size-padding)], fill=orange)

    border_width = 16
    draw.ellipse(
        [(padding+border_width, padding+border_width), 
         (size-padding-border_width, size-padding-border_width)], 
        fill=white
    )

    try:
        font = ImageFont.truetype("arialbd.ttf", 65)
    except IOError:
        try:
            font = ImageFont.truetype("arial.ttf", 65)
        except IOError:
            font = ImageFont.load_default()

    text = "WGL"
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) / 2
    y = (size - text_height) / 2 - bbox[1]
    
    draw.text((x, y), text, fill=text_color, font=font)

    os.makedirs("wrongl/resources", exist_ok=True)
    
    image.save("wrongl/resources/icon.png")
    
    image.save("wrongl/resources/icon.ico", format="ICO", sizes=[(256, 256)])
    
    print("✅ The creation of the WGL logo was successful (wrongl/resources/)")

if __name__ == "__main__":
    create_icon()