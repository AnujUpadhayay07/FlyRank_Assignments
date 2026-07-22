# 🚀 RESTful Task API

A lightweight and easy-to-use **Task Management REST API** built with **FastAPI**. This project demonstrates the implementation of complete **CRUD (Create, Read, Update, Delete)** operations using an in-memory data store.

---

## ✨ Features

- 📋 View all tasks
- 🔍 Retrieve a task by ID
- ➕ Create new tasks
- ✏️ Update existing tasks
- 🗑️ Delete tasks
- ❤️ Health Check endpoint
- 📖 Interactive Swagger Documentation
- ⚡ Fast and lightweight FastAPI application

---

## 🛠️ Tech Stack

- **Python 3.12**
- **FastAPI**
- **Uvicorn**
- **Pydantic**

---

## 📂 Project Structure

```text
TaskAPI/
│── main.py
│── requirements.txt
│── README.md
│── .gitignore
└── venv/        # Local virtual environment (not uploaded)
```

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/TaskAPI.git
cd TaskAPI
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Virtual Environment

**Windows (PowerShell)**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD)**

```cmd
venv\Scripts\activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run the Server

```bash
uvicorn main:app --reload
```

---

## 🌐 API URLs

| Service | URL |
|---------|-----|
| API Root | http://127.0.0.1:8000/ |
| Health Check | http://127.0.0.1:8000/health |
| Swagger UI | http://127.0.0.1:8000/docs |

---

## 📌 API Endpoints

| Method | Endpoint | Description |
|:------:|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Check API status |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

---

## 📥 Example Request

### Create a Task

**Request**

```http
POST /tasks
```

```json
{
    "title": "Learn FastAPI"
}
```

**Response**

```json
{
    "id": 4,
    "title": "Learn FastAPI",
    "done": false
}
```

---

## 💻 Run the Project

```bash
python -m venv venv
```

```bash
.\venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
```

```bash
uvicorn main:app --reload
```

---

## 📖 Interactive Documentation

After running the server, visit:

**Swagger UI**

```
http://127.0.0.1:8000/docs
```

---

## 📷 Sample Output

### GET /tasks

```json
[
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": false
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": false
    },
    {
        "id": 3,
        "title": "Push to GitHub",
        "done": true
    }
]
```

---

## ⚠️ Note

- This project uses an **in-memory list** as the data store.
- Data will be reset whenever the server restarts.
- This project is designed for learning FastAPI and REST API development.

---

## 👩‍💻 Author

**Anuj Upadhayay**

---

⭐ If you found this project useful, consider giving it a star.
