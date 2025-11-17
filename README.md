# Build & Blog Marathon – Smart Video Repurposer

This project was built for the **Google Build & Blog Marathon Hackathon**.  
It helps creators **upload a video once and repurpose it automatically** for multiple platforms like **LinkedIn, Instagram, Twitter**, etc.

The system extracts key frames using Gemini, enhances or modifies images using **NanoBanana (Gemini 2.5 Flash Image)**, and generates platform-specific content variations.

---

## 🚀 Features
- Upload a video (stored securely in Cloud Storage)
- Automatic frame extraction using Gemini
- Select frames suggested by the LLM
- Platform-tailored content generation
- Image modification using prompt-based NanoBanana
- Clean frontend for interacting with the system
- Backend APIs for processing & model orchestration
- An agent (Gaia) to coordinate all tasks end-to-end

---

## 🧩 Project Structure
├── frontend/
│ └── Next.js UI for uploads & interactions
│
├── backend/
│ └── FastAPI or Node backend for video → frame extraction,
│ presigned URLs, and calling Gemini/NanoBanana
│
├── agent/
│ └── multimodal orchestration agent
│ that talks to backend + models


---

## 🛠️ Tech Stack
- **Frontend:** Next.js + Tailwind  
- **Backend:** FastAPI / Node  
- **Agents:** ADK
- **Models:** Gemini 2.0 Flash, Gemini 2.5 Flash Image (NanoBanana)  
- **Storage:** Google Cloud Storage (GCS)

---

## 🧪 How It Works (High Level)
1. User uploads a video → stored in GCS via backend presigned URL.  
2. Backend extracts frames using Gemini Video API.  
3. Agent suggests best frames + content variations.  
4. User selects frames; modifies images via NanoBanana if needed.  
5. Agent generates final deliverables for each platform.

---

## 📦 Setup
See setup instructions in each folder:
- **frontend/README.md**
- **backend/README.md**
- **agent/README.md**

---

## 🙌 Credits
Built by Arpita for Google’s Build & Blog Marathon.
