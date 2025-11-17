
---

# **📁 agent/README.md**

```markdown
# Gaia Agent – Smart Video Repurposer

This folder contains the **Gaia-based multimodal agent** that orchestrates the entire workflow.

The agent handles:
- Understanding user intent
- Calling backend APIs
- Summarizing extracted frames
- Recommending best frames
- Generating platform-specific copy
- Triggering NanoBanana edits
- Returning final deliverables

---

## 🧠 Capabilities
- Works as a central brain for the system  
- Parses user instructions  
- Chooses the right model/tool (Gemini / NanoBanana)  
- Coordinates asynchronous tasks  

---

## 📂 Folder Structure
agent/
├── app.py
├── tools/
│ ├── backend_api.py
│ ├── gemini_tools.py
│ └── image_tools.py
└── policies/


---

## 🚀 Running the Agent
```bash
python app.py

curl -X POST http://localhost:5000/agent -d '{"query":"Help me repurpose my video"}'

