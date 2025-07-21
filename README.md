```markdown
# Medical Imaging and Report Assistant

## 🌟 Project Overview
Clinical support tool that processes radiology images and patient data to generate draft reports using AI-powered segmentation, annotation, and diagnosis suggestions.

## 🚀 Key Features
- **Image Processing**: MONAI-based segmentation of radiology scans
- **AI Analysis**: Gemini Flash 1.5 Vision for multimodal medical reasoning
- **Report Generation**: AI-assisted draft reports with RAG system
- **Secure Access**: JWT authentication with OAuth integration

## 🔗 Key Resources
- [MONAI Medical AI Framework](https://monai.io/)
- [Gemini Flash 1.5 Vision](https://ai.google.dev/gemini-api)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Azure Container Instances](https://azure.microsoft.com/en-us/products/container-instances)

## 🛠️ Tech Stack
| Component          | Technology Used               |
|--------------------|-------------------------------|
| Frontend           | React + Vite                  |
| Backend            | FastAPI                       |
| Database           | PostgreSQL                    |
| Authentication     | JWT + OAuth (Google/GitHub)   |
| AI Vision          | MONAI (NVIDIA)                |
| Multimodal AI      | Gemini Flash 1.5 Pro Vision   |
| Cloud Deployment   | Microsoft Azure               |

## 🌐 API Endpoints

### 🔐 Authentication
| Endpoint                      | Method | Description                  |
|-------------------------------|--------|------------------------------|
| `/api/v1/auth/login/google`   | GET    | Google OAuth login           |
| `/api/v1/auth/login/email`    | POST   | Email/password login         |
| `/api/v1/auth/signup/email`   | POST   | Email registration           |

### 👤 Profile
| Endpoint                   | Method | Description                  |
|----------------------------|--------|------------------------------|
| `/api/v1/auth/me`          | GET    | Get user profile             |
| `/api/v1/auth/me`          | PUT    | Update profile               |
| `/api/v1/auth/last-login`  | GET    | Get last login timestamp     |

### 🏥 Patients
| Endpoint                   | Method | Description                  |
|----------------------------|--------|------------------------------|
| `/api/v1/patients/`        | GET    | List all patients            |
| `/api/v1/patients/`        | POST   | Create new patient           |
| `/api/v1/patients/search/` | GET    | Search patients              |

### 🖼️ Scans
| Endpoint                           | Method | Description                  |
|------------------------------------|--------|------------------------------|
| `/api/v1/scans/`                   | POST   | Upload new scan              |
| `/api/v1/scans/`                   | GET    | List all scans               |
| `/api/v1/scans/{scan_id}/image`    | GET    | Get scan image               |

### 📝 Reports
| Endpoint                                   | Method | Description                          |
|--------------------------------------------|--------|--------------------------------------|
| `/api/v1/reports/`                         | POST   | Create new report                    |
| `/api/v1/reports/{report_id}`              | GET    | Get report details                   |
| `/api/v1/reports/{report_id}`              | PUT    | Update report                        |
| `/api/v1/reports/segment_scan/{scan_id}`   | POST   | Segment scan (MONAI integration)     |
| `/api/v1/reports/analyze_scan/{scan_id}`   | POST   | AI analysis (Gemini integration)     |

## 🤖 AI Integration

### MONAI Segmentation Endpoint
```http
POST http://monai-seg-api-instance.eastus.azurecontainer.io:8000/segment
Content-Type: multipart/form-data

{
  "file": "binary_dicom_data",
  "model": "spleen_ct_segmentation"
}
```

### Gemini Vision Integration
```python
# Sample request to Gemini for analysis
response = generative_model.generate_content([
    "Analyze this medical scan and suggest findings",
    scan_image
])
```

## 🐳 Deployment Setup

### Backend
```bash
uvicorn app.main:app --reload
```

### Frontend
```bash
npm run dev
```

### MONAI on Azure
```bash
docker build -t monai-segmentation -f docker/Dockerfile.monai .
az container create --resource-group yourRG --name monai-seg-api-instance \
  --image yourRegistry.azurecr.io/monai-segmentation:latest \
  --ports 8000 --cpu 4 --memory 8
```

## 📂 Project Structure
```
medical-imaging/
├── backend/
│   ├── app/
│   │   ├── api/           # All API endpoints
│   │   ├── core/          # Auth and config
│   │   └── services/      # Business logic
├── frontend/
│   ├── src/
│   │   ├── api/           # API clients
│   │   └── components/    # UI components
└── docker/
    └── Dockerfile.monai   # MONAI deployment
```"# ai_imaging_assistant" 
