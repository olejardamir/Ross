# Project Setup

## Python Version

Ensure you are using **Python 3.10** to run this project.

---

## Requirements

Install the following Python packages (e.g., using `pip install -r requirements.txt`):

| Package               | Version  | License                           |
|-----------------------|----------|---------------------------------|
| duckduckgo_search     | 8.0.1    | MIT License                     |
| fastapi               | 0.115.12 | MIT License                     |
| gTTS                  | 2.5.4    | MIT License                     |
| jellyfish             | 1.2.0    | MIT License                     |
| langchain             | 0.3.25   | MIT License                     |
| langchain_community   | 0.3.24   | MIT License                     |
| mutagen               | 1.46.0   | GPL v2 or later                 |
| Pillow                | 11.2.1   | MIT-CMU License                 |
| pydub                 | 0.25.1   | MIT License                     |
| python-dotenv         | 1.1.0    | BSD 3-Clause License            |
| requests              | 2.32.3   | Apache 2.0 License              |
| spacy                 | 3.8.5    | MIT License                     |
| torch                 | 2.7.0    | BSD-style License               |
| transformers          | 4.51.3   | Apache 2.0 License              |
| uvicorn               | 0.34.2   | BSD 3-Clause License            |

> **Note:** The `mutagen` package is licensed under **GPL v2 or later**, which may impose certain restrictions on distribution and usage. Ensure compatibility with your project's licensing requirements.

---

## Additional Dependencies

These are often installed automatically but may need to be installed or pinned explicitly:

| Package               | License                           |
|-----------------------|---------------------------------|
| numpy                 | BSD License                     |
| tqdm                  | MPL 2.0 License                 |
| sentence-transformers | Apache 2.0 License              |
| scikit-learn          | BSD License                     |
| regex                 | Python Software Foundation License |
| six                   | MIT License                     |
| chardet               | LGPL License                    |
| typing-extensions     | PSF License                     |
| h11                   | MIT License                     |
| starlette             | BSD License                     |

---

## Optional NLP/ML Runtime Helpers

| Package     | License               |
|-------------|-----------------------|
| protobuf    | BSD License           |
| accelerate  | Apache 2.0 License    |
| datasets    | Apache 2.0 License    |

---



## Running the Project

After installing the requirements in your Python 3.10 environment:

- Run the main application:

```bash
python Ross_git/src/main.py
```

Or open it in your IDE and run `main.py`.

- Configuration files (such as `.env` for FastAPI settings) are located in:

```
Ross_git/src/app/config/.env
```

We use **HTTPS** with **PEM keys** generated for testing, also stored in the same `config` folder.

---

## User Interface

To launch the UI, simply open the following file in your web browser:

```
Ross_git/src/index.html
```


## Browser Configuration for HTTPS and Localhost

Since this demo uses **insecure PEM keys**, your browser must be configured to accept the connection to `localhost` over HTTPS.

1. Navigate to one of the following URLs in your browser:
   - [https://127.0.0.1:8000](https://127.0.0.1:8000)
   - [https://localhost:8000](https://localhost:8000)

2. When prompted, **accept all security warnings or certificates**.

This step is required to enable REST API communication between the frontend and backend via JavaScript over HTTPS.

---

## CORS Configuration

The backend includes a **CORS (Cross-Origin Resource Sharing)** filter.  
Currently, it is configured to **allow requests from all origins** (`*`) for development and testing purposes.

## Demo Video : The working app

<a href="https://www.youtube.com/watch?v=lXctSHUOig8&vq=hd1080&speed=2" target="_blank">
  <img src="https://img.youtube.com/vi/lXctSHUOig8/hqdefault.jpg" alt="Watch the demo">
</a>

Click the thumbnail above to watch the demo on YouTube.  
> Tip: Use YouTube's settings gear icon to manually increase playback speed if needed.

---

## App Output Demo 1 : Topic - Importance of cute animals on Internet
### Text corrected with GPT

<a href="https://www.youtube.com/watch?v=zAtOlhL_vns&vq=hd1080" target="_blank">
  <img src="https://img.youtube.com/vi/zAtOlhL_vns/hqdefault.jpg" alt="Watch the output demo">
</a>

Click the thumbnail above to see the output result from running the app.  

## App Output Demo 2  : Topic - The Role of Memes in Modern Communication
### No text correction applied

<a href="https://www.youtube.com/watch?v=_6XA5CDZCj4&vq=hd1080" target="_blank">
  <img src="https://img.youtube.com/vi/_6XA5CDZCj4/hqdefault.jpg" alt="Watch the additional feature demo">
</a>

Click the thumbnail above to see the output result from running the app.  


## App Output Demo 3  : Topic - The fake fun facts
### No text correction applied

<a href="https://www.youtube.com/watch?v=14wHuWSF8ss&vq=hd1080" target="_blank">
  <img src="https://img.youtube.com/vi/14wHuWSF8ss/hqdefault.jpg" alt="Watch the testing walkthrough">
</a>

Click the thumbnail above to see the output result from running the app.  






## Deeper Technical Dive

### The Framework Structure:

```
├── data/                  # Sample datasets, config data, non-code resources
├── dist/                  # Build/distribution artifacts
├── docs/                  # Framework documentation and API usage
├── examples/              # Example apps showcasing framework usage
├── logs/                  # Log files (if logging to file is needed)
├── migrations/            # (Optional) If DB migration tools ever added
├── plugins/               # Optional plugin system support
├── scripts/               # Setup/deployment/automation scripts
├── tests/                 # Test suite
│   ├── unit/
│   ├── integration/
│   ├── functional/
│   └── resources/
└── src/                   # Main framework source code
    ├── app/              # Application layer
    │   ├── config/        # Configuration and settings
    │   ├── controllers/   # HTTP request handlers (controllers in MVC)
    │   ├── dao/           # Data access layer (e.g., file, API, cache access)
    │   ├── models/        # Data models (plain classes/schemas, no ORM)
    │   ├── routing.py     # Route definitions
    │   ├── services/      # Business logic layer
    │   └── utils/         # Utility functions
    └── resources/         # Static resources or test/app resource files
```

## Project Structure Overview

Ross_git/src/main.py
    This is the main entry point that runs the FastAPI application as a microservice,
    exposing REST API endpoints. It includes common security protections such as:
    - CORS filtering
    - HTTPS protocol

Ross_git/src/index.html
    This is a demo UI serving as a proof of concept. In a real-world application,
    the frontend would be handled by a separate framework to maintain separation of concerns.
    For the sake of demonstration, this version uses basic HTML, CSS, and JavaScript.
    The corresponding CSS and JS files are located in:
    - Ross_git/src/app/view/

Ross_git/src/app/routing.py
    Contains production-ready FastAPI route definitions with proper dependency injection.

Ross_git/logs/log_manager.py
    A log manager module to view logs via UI or persist them for debugging and development.
    This module should ideally store logs in a dedicated logging system (e.g., via Kafka).
    It reads configurations from a `.config` file to determine logging behavior.
    Note: The log manager is not integrated across all modules due to time constraints.
    It is considered a work-in-progress and serves as an example of how logging can be structured.

tmp/ and output/ folders
    Used temporarily for quick data offload during development.
    In production, files should not be saved within the microservice itself.
    Instead, use memory buffers or upload files directly to cloud storage (e.g., S3 bucket).

controllers/ and services/ folders
    These directories support a maintainable MVC architecture and promote best practices.

### Ross_git/src/app/utils/websearch/duck_go.py

This module retrieves all image search results from the DuckDuckGo search engine. It does **not** use any API keys, and as such, **should not be abused with frequent requests**.

Due to the limited availability of freely distributable images, we have **removed filtering by specific websites**. The search retrieves images for the **main topic**, relying on the engine’s ability to provide the **best 100 matches**. 

Images are **reordered** to match the video’s spoken text using **Jaro distance** and parsed sentences. This is a time-saving heuristic; ideally, each sentence should be searched individually and mapped temporally via TTS duration. 

Note:
- Jaro is fast and serves as a **weak classifier**.
- It does **not capture semantic meaning**, so results may lack relevance, especially when sourcing from limited datasets like free image collections.

---

### Ross_git/src/app/utils/NLP/speech_generator.py

This module uses `TinyLlama/TinyLlama-1.1B-Chat-v0.3` (via **LangChain**) for fast LLM text generation. It operates with a **general prompt** and attempts output generation **up to 3 times** per request (as configured in `.config`).

Key points:
- The model is **open-source** and requires **no login**.
- If output fails after 3 attempts, the user is advised to retry or change the model.
- The model tends to generate **short outputs**, so we **chain prompts**, feeding back previous text until we reach ~900 words (takes ~4–7 minutes of read time).

---

### Ross_git/src/app/utils/NLP/parser.py

This file:
- Parses speech into **individual sentences**.
- Extracts **grammatical root words** (nouns, verbs, pronouns), excluding stopwords.

Originally, the idea was to:
- Perform a search-engine query per sentence using its root words for more relevant image results.
- Apply TTS per sentence for:
  - Accurate subtitles with **nanosecond timing**.
  - Precise **image-to-sentence alignment**.

Due to time constraints, a simplified method using **title sorting and Jaro distance** was adopted.

---

### Ross_git/src/app/utils/images/downloader.py

Downloads and processes images:
- Resizes images using **bicubic resampling** (to avoid artifacts).
- Crops the **center of each image** to 720p resolution.

Caveats:
- This method can **cut off key elements** (e.g., faces).
- A simpler method would be to fill edges with **blur**.
- More advanced solutions could include **focus detection**, **clustering**, or **face recognition**.

---

### /home/coka/Desktop/Ross/Ross_git/src/app/utils/audio/tts.py

Converts text to speech and returns the **audio duration in nanoseconds**.

---

### Ross_git/src/app/utils/audio/remixer.py

Mixes generated speech with background music:
- Adds a **1-second fade-in** at the start and a **1-second fade-out** at the end of the music.
- Future enhancements could include:
  - **Dynamic music selection** based on sentiment.
  - **Automatic volume ducking** for better speech clarity.

---

### Ross_git/src/app/utils/video/combiner.py

Creates a slideshow by combining the processed images into a video.  
**Note:** Transitions are currently not applied due to `moviepy` installation issues and time constraints.

---

### Ross_git/src/app/utils/core/text2video.py

This is the **core orchestrator module**. It integrates all the components above and outputs the final video.  
It is called by the **Controller** in the MVC architecture.

```
+-------------------+     +--------------------------+     +--------------------------+
| User Provides     | --> | Clean Temp &             | --> | ImageSearcher            |
| - Topic           |     | Output Directories       |     | - Search images          |
| - Speech Text     |     |                          |     |   using DuckDuckGo       |
+-------------------+     +--------------------------+     +--------------------------+
        | -------------------------------------------------------------------                                                                        
        v                                                      
+--------------------------+     +--------------------------+     +--------------------------+
| TextParser               | --> | ImageOrderer             | --> | ImageDownloader          |
| - NLP parse speech       |     | - Match sentences        |     | - Extract image URLs     |
|                          |     |   to images              |     | - Download images        |
+--------------------------+     +--------------------------+     +--------------------------+
        | ------------------------------------------------------------------------                                                                        
        v                                                      
+--------------------------+     +--------------------------+     +--------------------------+
| download_images_         | --> | TextToSpeech             | --> | AudioMixer               |
| sequentially()           |     | - Convert speech to audio|     | - Mix TTS audio          |
| (resize, crop images)    |     |                          |     |   with music             |
+--------------------------+     +--------------------------+     +--------------------------+
        | ------------------------------------------------------------------------                                                                        
        v                                                      
+--------------------------+     +--------------------------+   
| VideoMaker               | --> | Final Video Output       |                              
| - Generate final video   |     |                          |                              
+--------------------------+     +--------------------------+  
```



# AI-Powered Multimedia Generation Pipeline (Production Stack)

This repository outlines a full-stack architecture for generating AI-powered speech-to-video content. It combines natural language generation, speech synthesis, multimedia search, and video rendering into a modular and production-ready system.

---

## Architecture Overview

### 1. Frontend (Optional for UI or Demos)

| Component       | Technology         |
|----------------|--------------------|
| UI Framework   | React / Next.js    |
| Styling        | Tailwind CSS       |
| Charts         | Recharts / D3.js   |
| Auth           | Firebase Auth / Auth0 / Clerk |
| Hosting        | Vercel / Netlify   |

---

### 2. Backend API Layer

| Component        | Technology        |
|-----------------|-------------------|
| Web API         | FastAPI           |
| Async Tasks     | Celery + Redis    |
| Containerization| Docker            |
| API Gateway     | NGINX / AWS API Gateway |
| Auth            | OAuth2 / JWT      |

---

### 3. AI Services Layer

| Task                  | Technology                                     |
|-----------------------|------------------------------------------------|
| Text-to-Speech        | Coqui TTS / OpenAI TTS / Azure TTS             |
| Text Generation       | Hugging Face Transformers (quantized)          |
| Model Serving         | Triton Inference Server / ONNX Runtime         |
| Audio Processing      | ffmpeg-python                                  |
| Image Search          | Bing Image Search API / Unsplash API           |
| Image Processing      | Pillow / OpenCV                                |
| Video Composition     | ffmpeg (Python-wrapped)                        |

---

### 4. Data Management

| Component         | Technology                     |
|------------------|--------------------------------|
| Object Storage    | Amazon S3 / Google Cloud Storage |
| Metadata Database | PostgreSQL                     |
| Task Queue        | Redis                          |
| Caching (Optional)| Redis / Cloudflare             |

---

### 5. DevOps / CI-CD

| Function           | Tool                          |
|--------------------|-------------------------------|
| Version Control    | GitHub / GitLab               |
| CI/CD Pipelines    | GitHub Actions / GitLab CI    |
| Docker Registry    | GitHub Container Registry / Docker Hub |
| IaC (Infrastructure as Code) | Terraform / Pulumi  |
| Secrets Management | HashiCorp Vault / AWS Secrets Manager |

---

### 6. Deployment & Orchestration

| Component          | Technology                   |
|--------------------|------------------------------|
| Orchestration      | Kubernetes (EKS/GKE) / Docker Compose |
| Auto-scaling       | Kubernetes HPA               |
| Load Balancing     | NGINX Ingress / AWS ALB      |
| Monitoring         | Prometheus + Grafana         |
| Error Reporting    | Sentry                        |

---

### 7. Observability & Logging

| Component       | Technology                      |
|----------------|----------------------------------|
| Central Logging | ELK Stack / Loki + Grafana      |
| Metrics         | Prometheus + Grafana            |
| Tracing         | OpenTelemetry / Jaeger          |
| Alerts          | PagerDuty / Grafana Alerts      |

---

### 8. Security & Compliance

| Layer            | Measures                                  |
|------------------|-------------------------------------------|
| Network          | TLS/SSL everywhere                        |
| Access Control   | Role-Based Access (OAuth2, SSO)           |
| File Safety      | Antivirus scanning (ClamAV or similar)    |
| Media Licensing  | License metadata tracking                 |
| Data Compliance  | GDPR / CCPA readiness                     |

---

# Advanced Techniques & Tools for Multimedia AI Systems

This section outlines key techniques, APIs, and models useful for building advanced, production-ready multimedia AI pipelines.

---

## Text-to-Speech (TTS) with Metadata Support

Use high-quality TTS services that support:
- **Speech metadata** (e.g., timing, subtitles, phoneme tags)
- **Voice selection and tuning**

**Recommended Services:**
- **Azure Cognitive Services TTS**
- **Amazon Polly**

---

## Keyframe Extraction from Video

Extract meaningful frames using frame sampling, scene detection, or semantic cues.

### 1. Frame Sampling
- Extract 1 frame every _N_ frames (naive approach)

### 2. Scene Detection (Content-Aware Sampling)
- **Tool:** `scenedetect`
- **Method:** Histogram comparison of luma (brightness) to detect cuts

### 3. Keyframe Extraction (Semantic-Aware)
- **Object Detection:** YOLO, Detectron2, OpenCV DNN
- **Face Detection:** Haar Cascades, dlib, OpenCV

---

## Hashtag or Label Generation from Visual Content

Generate tags for videos or images using vision-language models or labeling APIs.

### Options:
- **Clarifai** (general and custom models)
- **Hugging Face Transformers**:
  - `CLIP` (image-text embeddings)
  - `BLIP`, `BLIP-2` (image captioning and understanding)
- **Google AutoML Vision**
- **Amazon Rekognition**:
  - Use with `ffmpeg`, `PySceneDetect`, or `scenedetect` for scene-aware labeling

---

## Image Cropping & Region of Interest Detection

Automatically crop or center on meaningful parts of an image.

### Techniques:

**1. Clustering-Based:**
- **DBSCAN**: Detect and crop around the densest region (e.g., main subject group)

**2. Object/Face Detection:**
- **OpenCV**, **YOLO**, **MediaPipe**

**3. Saliency Detection (Human Attention):**
- **OpenCV saliency module**
- **U^2-Net**
- **DeepLab**

---

## Text Embeddings for Semantic Similarity

Generate dense vector representations for text to enable similarity search, clustering, or ranking.

### Recommended Models & APIs:

- **sentence-transformers**:
  - `all-MiniLM-L6-v2` (lightweight, performant)
- **OpenAI Embeddings**:
  - `text-embedding-3-small`
- **Cohere Embeddings API**
- **Google Universal Sentence Encoder**

---

## License Comparison

| License         | Notes                                                                 |
|----------------|-----------------------------------------------------------------------|
| **MIT**         | Very permissive, minimal requirements. Widely used in Python OSS.     |
| **BSD 3-Clause**| Like MIT, but prevents misuse of contributor names.                   |
| **MIT-CMU**     | Identical to MIT License.                                             |
| **Apache 2.0**  | Like MIT, but includes patent grants and stronger liability protection.|

---


