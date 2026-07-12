# CST8917-lab2



**Student Name**: Bryan Edler  
**Student ID**: 041016930  
**Course**: 26S_CST8917_300 Serverless Applications
**Semester**: Summer 2026  



## Demo Video

🎥 [Watch Demo Video](https://youtu.be/c_IP-gAaRXI)

---

```markdown
# 🖼️ Smart Image Analyzer with Durable Functions

Lab 2 for CST8917 - Serverless Applications | Spring/Summer 2026

## 📋 Overview

This project implements a **Smart Image Analyzer** using Azure Durable Functions with the **Fan-Out/Fan-In pattern**. When an image is uploaded to Azure Blob Storage, it automatically triggers four analyses in parallel:

- 🎨 **Color Analysis** - Extracts dominant colors from the image
- 🏗️ **Object Detection** - Identifies objects/content in the image (mock)
- 📝 **Text/OCR Analysis** - Extracts text from images (mock)
- 📊 **Metadata Analysis** - Extracts image dimensions, format, and EXIF data

The results are combined into a single report and stored in Azure Table Storage, accessible via an HTTP endpoint.

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────────────────┐
│  Blob Storage   │     │     Durable Function         │
│   (images/)     │────▶│   (Fan-Out/Fan-In)          │
└─────────────────┘     └──────────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────────┐
                        │   4 Parallel Activities      │
                        │  ┌────────────────────────┐  │
                        │  │ analyze_colors         │  │
                        │  │ analyze_objects        │  │
                        │  │ analyze_text           │  │
                        │  │ analyze_metadata       │  │
                        │  └────────────────────────┘  │
                        └──────────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────────┐
                        │    Table Storage             │
                        │    (ImageAnalysisResults)    │
                        └──────────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────────┐
                        │    HTTP Endpoint             │
                        │    /api/results              │
                        └──────────────────────────────┘
```

## 📦 Prerequisites

- **Python 3.11 or 3.12** installed
- **VS Code** with the following extensions:
  - Azure Functions
  - Azure Storage
  - REST Client (optional)
- **Azure Functions Core Tools** (v4)
- **Node.js** (for Azurite)
- **Azurite** (local storage emulator)

## 🚀 Running Locally

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ImageAnalyzerLab
```

### 2. Create a Virtual Environment

**Mac/Linux/WSL:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Local Settings

Create a `local.settings.json` file:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "ImageStorageConnection": "UseDevelopmentStorage=true"
  },
  "Host": {
    "CORS": "*"
  }
}
```

### 5. Start Azurite (Local Storage Emulator)

**Using VS Code:**
1. Press `F1`
2. Select `Azurite: Start`

**Using Command Line:**
```bash
azurite --silent --location ~/azurite_data --skipApiVersionCheck
```

### 6. Create the `images` Container

**Using Python:**
```bash
python -c "
from azure.storage.blob import BlobServiceClient
conn_str = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'
client = BlobServiceClient.from_connection_string(conn_str)
client.create_container('images')
print('✅ Container images created!')
"
```

### 7. Start the Function App

**In VS Code:** Press `F5`

**In Terminal:**
```bash
func start
```

You should see all 9 functions loaded:
```
Functions:
        analyze_colors: activityTrigger
        analyze_metadata: activityTrigger
        analyze_objects: activityTrigger
        analyze_text: activityTrigger
        blob_trigger: blobTrigger
        generate_report: activityTrigger
        get_results: [GET] http://localhost:7071/api/results/{id?}
        image_analyzer_orchestrator: orchestrationTrigger
        store_results: activityTrigger
```

### 8. Upload a Test Image

**Using Python:**
```python
from azure.storage.blob import BlobServiceClient
from PIL import Image, ImageDraw
import io

conn_str = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'

client = BlobServiceClient.from_connection_string(conn_str)
container = client.get_container_client('images')

# Create a test image
img = Image.new('RGB', (600, 400), color='lightblue')
draw = ImageDraw.Draw(img)
draw.rectangle([50, 50, 250, 250], fill='red')
draw.rectangle([300, 50, 500, 200], fill='green')
draw.ellipse([50, 280, 250, 380], fill='yellow')

img_bytes = io.BytesIO()
img.save(img_bytes, format='PNG')
img_bytes.seek(0)

container.upload_blob('test_image.png', img_bytes, overwrite=True)
print('✅ Test image uploaded!')
```

### 9. View Results

**Get all results:**
```bash
curl http://localhost:7071/api/results
```

**Get a specific result** (replace ID):
```bash
curl http://localhost:7071/api/results/<your-id-here>
```

**In your browser:**
```
http://localhost:7071/api/results
```

## 🧪 Testing with the .http File

If you have the **REST Client** extension in VS Code:

1. Open `test-function.http`
2. Click the `Send Request` link above each request

## ☁️ Deploying to Azure

### 1. Create Azure Resources

**Using VS Code:**
1. Press `F1`
2. Select `Azure Functions: Create Function App in Azure... (Advanced)`
3. Choose:
   - Runtime: `Python 3.12`
   - OS: `Linux`
   - Plan: `Consumption` (not Flex Consumption)
   - Storage Account: Create new or use existing

### 2. Configure Application Settings

**In Azure Portal:**
1. Add `ImageStorageConnection` to Environment Variables
2. Value: Connection string from your Storage Account > Access Keys

### 3. Deploy Code

1. Press `F1`
2. Select `Azure Functions: Deploy to Function App...`
3. Choose your Function App

### 4. Test in Azure

1. Upload an image to the `images` container in your Azure Storage Account
2. Wait 30 seconds
3. Visit: `https://<your-app-name>.azurewebsites.net/api/results`

## 📊 Results Format

**Summary Response:**
```json
{
  "count": 1,
  "results": [
    {
      "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "fileName": "test_image.png",
      "analyzedAt": "2026-07-12T14:37:42.306000",
      "summary": {
        "imageSize": "600x400",
        "format": "PNG",
        "dominantColor": "#ADD8E6",
        "objectsDetected": 2,
        "hasText": false,
        "isGrayscale": false
      }
    }
  ]
}
```

**Full Analysis Response:**
Includes `analyses` object with:
- `colors` - Dominant colors with hex codes and percentages
- `objects` - Mock object detection results
- `text` - OCR results (mock)
- `metadata` - Real image metadata (width, height, format, EXIF)

## 🏗️ Code Structure

| File | Description |
|------|-------------|
| `function_app.py` | Main application with all 9 functions |
| `requirements.txt` | Python dependencies |
| `local.settings.json` | Local environment settings |
| `host.json` | Functions host configuration |
| `test-function.http` | HTTP endpoint tests for VS Code REST Client |

## 🔑 Key Functions

| Function | Type | Role |
|----------|------|------|
| `blob_trigger` | Blob Trigger | Detects image uploads, starts orchestrator |
| `image_analyzer_orchestrator` | Orchestrator | Manages workflow: fan-out, fan-in, chain |
| `analyze_colors` | Activity | Extracts dominant colors (REAL) |
| `analyze_objects` | Activity | Detects objects (MOCK) |
| `analyze_text` | Activity | OCR text extraction (MOCK) |
| `analyze_metadata` | Activity | Extracts image metadata (REAL) |
| `generate_report` | Activity | Combines all analyses into a report |
| `store_results` | Activity | Saves report to Table Storage |
| `get_results` | HTTP | Retrieves stored results |

## ⚠️ Troubleshooting

### Issue: "No module named 'azure.storage.blob'"
```bash
pip install azure-storage-blob
```

### Issue: "ContainerNotFound" error
```bash
# Create the images container
python -c "from azure.storage.blob import BlobServiceClient; ..."
```

### Issue: Azurite port already in use
```bash
pkill -f azurite
azurite --silent --location ~/azurite_data &
```

### Issue: Flex Consumption plan error
- Delete the Function App and recreate with **Consumption** plan
- Or update the trigger to use Event Grid

## 📚 Learning Outcomes

- ✅ Implemented **Fan-Out/Fan-In pattern** with Durable Functions
- ✅ Used **Blob Storage trigger** to start orchestrations automatically
- ✅ Ran multiple activities in parallel using `context.task_all()`
- ✅ Stored structured results in **Azure Table Storage**
- ✅ Retrieved results via an **HTTP endpoint**
- ✅ Deployed to Azure and tested in the cloud

## 🔗 Resources

- [Durable Functions Fan-Out/Fan-In Pattern](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview)
- [Azure Blob Storage Trigger](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-blob-trigger)
- [Pillow (PIL) Documentation](https://python-pillow.org/)
- [Azure Computer Vision API](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/)

---

**Author:** [Your Name]  
**Course:** CST8917 - Serverless Applications  
**Date:** July 2026
```

---

### 📝 How to Add This README

1. In VS Code, create a new file in your project root: `README.md`
2. Copy and paste the entire template above
3. Replace `[Your Name]` with your actual name
4. Replace `<your-repo-url>` with your GitHub repository URL
5. Save the file

---

### 🚀 Next Steps for Submission

Now that you have your README:

1. **Commit and push** to GitHub:
   ```bash
   git add README.md
   git commit -m "Add README with local setup instructions"
   git push
   ```

2. **Create your demo video** (max 5 minutes) showing:
   - Uploading an image locally
   - Orchestration logs showing parallel execution
   - Retrieving results via HTTP endpoint
   - Uploading to Azure and retrieving cloud results

3. **Submit your GitHub URL** to Brightspace

