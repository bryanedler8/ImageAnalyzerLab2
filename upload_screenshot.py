from azure.storage.blob import BlobServiceClient
from PIL import Image, ImageDraw, ImageFont
import io

conn_str = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'

client = BlobServiceClient.from_connection_string(conn_str)
container = client.get_container_client('images')

# Create a screenshot simulation
print('🖥️ Creating screenshot with text...')
img = Image.new('RGB', (1024, 768), color='#2b2b2b')
draw = ImageDraw.Draw(img)

# Window frame
draw.rectangle([20, 20, 1004, 748], outline='#404040', width=2)
draw.rectangle([20, 20, 1004, 50], fill='#1e1e1e')

# Window title bar
draw.text((40, 28), "📄 Document - Visual Studio Code", fill='#cccccc', size=16)

# Code area
draw.rectangle([30, 55, 994, 738], fill='#1e1e1e')

# Simulated code lines
code_lines = [
    ("def hello_world():", "#d4d4d4"),
    ("    print('Hello, Azure!')", "#d4d4d4"),
    ("    ", "#d4d4d4"),
    ("if __name__ == '__main__':", "#d4d4d4"),
    ("    hello_world()", "#d4d4d4"),
]

y_pos = 80
for line, color in code_lines:
    draw.text((50, y_pos), line, fill=color, size=18)
    y_pos += 35

# Side panel
draw.rectangle([850, 55, 994, 738], fill='#252526')
draw.text([860, 80], "📁 Explorer", fill='#cccccc', size=14)
draw.text([860, 120], "  📄 app.py", fill='#cccccc', size=12)
draw.text([860, 150], "  📄 requirements.txt", fill='#cccccc', size=12)

# Add some "text" that looks like code
draw.text([60, 350], "print('Hello World')", fill='#d4d4d4', size=16)
draw.text([60, 400], "azure.functions", fill='#569cd6', size=16)

img_bytes = io.BytesIO()
img.save(img_bytes, format='PNG')
img_bytes.seek(0)

container.upload_blob('screenshot.png', img_bytes, overwrite=True)
print('✅ Screenshot uploaded as PNG!')
