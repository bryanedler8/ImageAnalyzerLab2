from azure.storage.blob import BlobServiceClient
from PIL import Image, ImageDraw
import io

# Connection string for Azurite
conn_str = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'

# Connect to Azurite
client = BlobServiceClient.from_connection_string(conn_str)
container = client.get_container_client('images')

# Create a colorful test image with text
print('🎨 Creating colorful test image...')
img = Image.new('RGB', (600, 400), color='lightblue')
draw = ImageDraw.Draw(img)

# Draw some shapes
draw.rectangle([50, 50, 250, 250], fill='red', outline='darkred', width=3)
draw.rectangle([300, 50, 500, 200], fill='green', outline='darkgreen', width=3)
draw.ellipse([50, 280, 250, 380], fill='yellow', outline='gold', width=3)
draw.ellipse([300, 250, 500, 380], fill='purple', outline='darkviolet', width=3)

# Add some "text" (shapes that look like text for OCR mock)
draw.text((120, 120), "AI", fill='white', size=40)
draw.text((380, 100), "Cloud", fill='white', size=40)

# Convert to bytes
img_bytes = io.BytesIO()
img.save(img_bytes, format='PNG')
img_bytes.seek(0)

# Upload to blob storage
blob_name = 'test_image.png'
container.upload_blob(blob_name, img_bytes, overwrite=True)
print(f'✅ Test image "{blob_name}" uploaded successfully!')
print(f'📊 Image size: 600x400 pixels')
print('🔄 Check the function logs - the orchestration should start automatically!')
