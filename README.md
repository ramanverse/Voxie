# Voxie AI — Deepfake Authentication & Forensic Suite

**Voxie** is an advanced audio authenticity tool designed to detect AI-generated speech, verify spectral watermarks, and perform biological forensic analysis on voice recordings. 

Built for high-stakes environments where audio integrity is paramount, Voxie provides a multi-layered security approach to expose even the most sophisticated "Synthetic Perfection" in modern deepfakes.

[🚀 **Live Demo: voxieai.streamlit.app**](https://voxieai.streamlit.app/)

---

## 🛡️ Features

### 1. Multi-Layer AI Detection
Powered by the **Wav2Vec2-L-v2 Deepfake Detector**, Voxie analyzes the neural patterns of audio to identify synthetic signatures. It provides a real-time confidence score and classification (Real vs. Fake) for any uploaded WAV or MP3 file.

### 2. Biological Forensic Analysis (Layer 3)
Beyond simple AI models, Voxie extracts raw biological signal markers:
- **Pitch Jitter**: Detects the "Unnatural Stability" found in AI voices.
- **Spectral Flux**: Measures the rate of change in the power spectrum to identify synthetic synthesis.
- **Harmonics-to-Noise Ratio (HNR)**: Detects "Synthetic Perfection" where the voice is too clean to be human.

### 3. Spectral Watermarking
A secure FFT-based watermarking system that allows you to "Sign" your audio. 
- **Embed**: Inject a hidden, high-frequency spectral signature into any audio file.
- **Verify**: Instantly detect if a file carries a valid Voxie signature, ensuring it originated from a trusted source.

### 4. Neo-Brutalist Dashboard
An immersive, interactive "Bento-style" dashboard designed with a raw, high-contrast aesthetic:
- **Dotted Grid Background**: A technical, blueprint-style workspace.
- **Interactive Interactivity**: Cards lift and shift shadows on hover for a tactile experience.
- **Typography**: Powered by **Bricolage Grotesque** for a modern, aggressive tech feel.

### 5. Historical Analytics
All analyses are faithfully persisted to a local **SQLite** database, allowing for long-term trend visualization, risk distribution charts, and forensic history tracking.

---

## 🏗️ Architecture

- **Frontend (Streamlit)**: Custom-built UI using CSS-in-Python for Neo-Brutalist styling. Implements responsive "Bento" layouts and interactive glassmorphism components.
- **Backend (Python/PyTorch)**: Utilizes `transformers` for AI inference and `librosa` / `scipy` for deep signal processing and forensic feature extraction.
- **Signal Pipeline**: Raw binary audio is resampled to 16kHz, processed through an FFT spectral analyzer, and passed to the Wav2Vec2 transformer network.
- **Database (SQLite)**: A lightweight, persistent storage engine for tracking every forensic operation performed.

---

## ⚙️ Setup & Installation

### Prerequisites
- **Python**: v3.9 or higher.
- **FFmpeg**: Required for audio resampling (Install via `brew install ffmpeg` or `apt install ffmpeg`).

### 1. Clone & Environment
```bash
git clone https://github.com/ramanverse/Voxie.git
cd Voxie
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
streamlit run app.py
```

---

## 🚀 Usage Guide

1. **Dashboard**: View your system health, total threats detected, and average risk scores.
2. **Verify Audio**: 
    - Upload an audio file or use the provided samples.
    - **Forensic Breakdown**: Expand the metrics to see raw Jitter and HNR values.
    - **Verdict**: View the final risk level (Low, Medium, or High).
3. **Embed Watermark**: Upload a raw file to inject a secure spectral signature for future authentication.
4. **History & Analytics**: Track your past detections and visualize risk trends over time.

---

## 🛠️ Troubleshooting

- **First Run Delay?**: The app downloads a ~1.2GB AI model from Hugging Face on the first run. Please ensure a stable internet connection.
- **Audio Error?**: Ensure `ffmpeg` is installed on your system path.
- **Database Locked?**: Ensure only one instance of the app is running if you are performing heavy database operations.

---

**Voxie AI** — *Authenticating the world's voice, one signal at a time.*
