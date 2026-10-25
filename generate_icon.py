import os
from PIL import Image

def process_logo():
    logo_path = "wrongl/resources/logo.png"
    if not os.path.exists(logo_path):
        print("Error: Please save your custom logo as 'logo.png' inside 'wrongl/resources/' first.")
        return

    print("Processing custom logo...")
    img = Image.open(logo_path).convert("RGBA")
    
    size = 512
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    
    img.thumbnail((400, 400), Image.Resampling.LANCZOS)
    
    x = (size - img.width) // 2
    y = (size - img.height) // 2
    canvas.paste(img, (x, y), img)
    
    canvas.save("wrongl/resources/icon.png")
    
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    canvas.save("wrongl/resources/icon.ico", format="ICO", sizes=icon_sizes)
    
    print("Success! High-quality icons generated in wrongl/resources/")

if __name__ == "__main__":
    process_logo()