# Person Detector System

## 📌 Introduction
Person Detector System is a web application that allows users to upload an image and automatically detects the number of people in it. The system highlights detected people with bounding boxes and returns the processed image along with the count. Additionally, the results are stored in a database for future reference.

## 🛠 Tech Stack
- **Backend**: Python, FastAPI, API data validation
- **Frontend**: Next.js
- **Database**: PostgreSQL + SQLAlchemy
- **Deployment**: Docker, Docker Compose

## 📂 Project Structure
```
├── backend/                 # Backend (FastAPI)
├── frontend/                 # Frontend (Next.js)
├── docker-compose.yml  # Docker Compose configuration
```

## 🚀 Getting Started
### 1️⃣ Prerequisites
Make sure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 2️⃣ Run the Application
Clone this repository and navigate into the project folder:
```sh
git clone https://github.com/ntdat02092002/person-detection-system
cd person-detection-system
```

Start the system using Docker Compose:
```sh
docker-compose up --build
```

This will:
1. Set up the backend (FastAPI) to handle image uploads and person detection.
2. Set up the frontend (Next.js) to provide a user-friendly interface.
3. Initialize a PostgreSQL database to store detection results.

### 3️⃣ Access the Application
Once running, you can access the frontend at:
```
http://localhost:3000
```
And the FastAPI backend at:
```
http://localhost:8000/docs
```

## 📦 Features
✔ Upload an image via web UI  
✔ Detect and count people in the image  
✔ Display results with bounding boxes  
✔ Store results (time, count, image path) in PostgreSQL  
✔ Easy deployment with Docker  

## 📝 License
This project is licensed under the MIT License.

---

Feel free to contribute and improve the system! 🚀

