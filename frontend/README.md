# Frontend – Smart Video Repurposer

This is the **Next.js 14** frontend for the project.  
It provides a clean UI where users can:

- Upload videos
- View extracted frames
- Select frames for repurposing
- Provide prompts for image edits (NanoBanana)
- Trigger agent workflows

---

## ⚡ Tech Stack
- **Next.js 14 (App Router)**
- **TailwindCSS**
- Fetch API for backend communication
- Google OAuth or API key input (optional)

---

## 📂 Folder Structure
frontend/
├── app/
│ ├── upload/
│ ├── frames/
│ ├── edit/
│ └── api/
├── components/
├── lib/
└── public/


## 🚀 Getting Started

### 1. Install dependencies
```bash
npm install

Create .env.local:

NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

npm run dev
