# 🎬 Text-to-Video Generation Project

## 🚀 Overview

The **Text-to-Video Generator** is an AI-powered tool that converts a simple **college name** input into a fully generated **narrated video** using real content from the college’s official website. It automatically:

* Visits the college website
* Extracts useful text and images
* Summarizes the content
* Generates audio narration using text-to-speech
* Combines images and audio to produce a video

This project is ideal for educational platforms, virtual campus tours, and informational content automation.

---

## 🧠 Features

* 🖥️ Web scraping to extract real-time content
* 🧾 Summarization of long content into simple highlights
* 🎤 Audio narration using text-to-speech (TTS)
* 🖼️ Downloading and filtering relevant images
* 🎞️ Slideshow video generation with narration
* 🔁 Modular and customizable structure

---

## ⚙️ Tools & Technologies Used

| Component           | Tool/Library                    | Purpose                              |
| ------------------- | ------------------------------- | ------------------------------------ |
| Backend Framework   | `Django`, `FastAPI`             | REST API and backend logic           |
| Web Scraping        | `BeautifulSoup`, `requests`     | Extract data and media from websites |
| Text Summarization  | `transformers`, `BART`, `T5`    | NLP for text simplification          |
| Text-to-Speech      | `gTTS`, `pyttsx3`, `ElevenLabs` | Generate narration audio             |
| Video Creation      | `moviepy`, `OpenCV`             | Combine images and audio into MP4    |
| Frontend (optional) | `Streamlit`, `HTML-CSS`         | User input interface                 |
| Deployment          | `Render.com`                    | Cloud hosting and deployment         |
| Version Control     | `Git`, `GitHub`                 | Source control and collaboration     |

---

## 📂 Project Structure

```
text-to-video-project/
│
├── backend/               # Backend logic
│   ├── scraper.py         # Scrapes website content
│   ├── summarizer.py      # NLP-based summarization
│   ├── tts_generator.py   # Converts text to audio
│   ├── video_creator.py   # Creates video from media
│   └── api.py             # Backend API endpoints
│
├── media/                 # Stores images/audio
├── static/                # CSS, JS (optional)
├── templates/             # HTML templates (optional)
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## 🛠️ How to Run the Project Locally

### 🔹 1. Clone the Repository

```bash
git clone https://github.com/your-username/text-to-video-project.git
cd text-to-video-project
```

### 🔹 2. Create a Python Virtual Environment

#### For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 🔹 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔹 4. Run the Backend Server

#### If using FastAPI:

```bash
uvicorn backend.api:app --reload
```

#### If using Django:

```bash
python manage.py runserver
```

> The backend server will start at `http://localhost:8000` or your configured port.

---

## 💡 Use Cases

* 🎓 Virtual campus tours for colleges and universities
* 📹 Automated video creation for educational platforms
* 🛍️ E-commerce product showcase generator
* 📚 Text-to-video converters for e-learning
* 📰 News summarization and video generation
* 📢 Marketing videos for institutions and organizations

---

## 🌐 Deployment Information

The project is cloud-ready and can be deployed to platforms such as:

| Platform          | Purpose                     | Example URL                                  |
| ----------------- | --------------------------- | -------------------------------------------- |
| **Render**        | Full-stack deployment       | `https://blueplanettexttovideo.onrender.com` |
| **GitHub Pages**  | Frontend hosting (optional) | For static UIs only                          |
| **Heroku**        | Python backend (deprecated) | Alternative to Render                        |
| **AWS/GCP/Azure** | Scalable production hosting | Enterprise-level deployments                 |

> You can containerize the project using Docker for better portability.

---

## 🙌 Contributors

* 👨‍💻 **Sanjay Kumar S** – AI Developer & Backend Engineer
* 🧪 Internship Project under Python AI

---

## 📃 License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute it with proper attribution.

---

## 📬 Contact

**Sanjay Kumar S**
📧 [kumar185694@gmail.com](mailto:kumar185694@gmail.com)
📍 Chennai, India
🎓 B.Tech Artificial Intelligence and Data Science, Panimalar Engineering College Chennai
