from azure.storage.blob import BlobServiceClient
from PIL import Image, ImageDraw
import io

conn_str = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'

client = BlobServiceClient.from_connection_string(conn_str)
container = client.get_container_client('images')

# Create a colorful "photograph" with gradient
print('📸 Creating color photograph simulation...')
img = Image.new('RGB', (800, 600), color='skyblue')
draw = ImageDraw.Draw(img)

# Sky gradient (top to bottom)
for y in range(300):
    r = 135 - int(y * 0.1)
    g = 206 - int(y * 0.2)
    b = 235 - int(y * 0.3)
    draw.rectangle([0, y, 800, y+1], fill=(r, g, b))

# Green ground
draw.rectangle([0, 300, 800, 600], fill='forestgreen')

# Sun
draw.ellipse([50, 50, 150, 150], fill='yellow')

# Clouds
draw.ellipse([200, 80, 280, 130], fill='white')
draw.ellipse([230, 60, 310, 110], fill='white')
draw.ellipse([400, 100, 480, 150], fill='white')

# House
draw.rectangle([350, 350, 550, 500], fill='sienna')
draw.rectangle([400, 280, 460, 380], fill='red')
draw.polygon([(330, 350), (450, 280), (570, 350)], fill='darkred')

# Trees
draw.rectangle([650, 350, 670, 500], fill='saddlebrown')
draw.ellipse([610, 280, 710, 380], fill='darkgreen')
draw.rectangle([150, 400, 170, 520], fill='saddlebrown')
draw.ellipse([110, 330, 210, 430], fill='darkgreen')

img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG', quality=85)
img_bytes.seek(0)

container.upload_blob('color_photo.jpg', img_bytes, overwrite=True)
print('✅ Color photograph uploaded as JPEG!')
