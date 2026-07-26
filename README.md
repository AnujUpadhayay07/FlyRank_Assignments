# 🚀 RESTful Task API with SQLite

A lightweight and easy-to-use **Task Management REST API** built with **FastAPI** and **SQLite**. This project demonstrates complete **CRUD (Create, Read, Update, Delete)** operations with persistent data storage using SQLModel.

---

## ✨ Features

- 📋 View all tasks
- 🔍 Retrieve a task by ID
- ➕ Create new tasks
- ✏️ Update existing tasks
- 🗑️ Delete tasks
- 💾 Persistent SQLite database
- 🗄️ Automatic database and table creation
- 🌱 Inserts sample tasks only on the first run
- ❤️ Health Check endpoint
- 📖 Interactive Swagger Documentation

---

## 🛠️ Tech Stack

- Python 3.12
- FastAPI
- SQLModel
- SQLite
- Uvicorn
- Pydantic

---

## 📂 Project Structure

```text
TaskAPI/
│── main.py
│── database.py
│── models.py
│── requirements.txt
│── README.md
│── .gitignore
│── tasks.db          # Created automatically
└── venv/             # Local virtual environment (not uploaded)
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/TaskAPI.git
cd TaskAPI
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

Windows (CMD)

```cmd
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Server

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
    "title": "Learn SQLite"
}
```

**Response**

```json
{
    "id": 4,
    "title": "Learn SQLite",
    "done": false
}
```

---

## 💾 Database

This project uses **SQLite** for persistent storage.

- Database file: `tasks.db`
- The database is automatically created on the first run.
- The `tasks` table is automatically created if it does not exist.
- Three sample tasks are inserted only when the database is empty.
- Data persists even after restarting the server.

---

## 🗃️ Example SQL Query

```sql
SELECT * FROM tasks;
```

---

## ▶️ Run the Project

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

After starting the server, open:

```
http://127.0.0.1:8000/docs

```

---

## 📷 Sample Response
<img width="389" height="63" alt="image" src="https://github.com/user-attachments/assets/46e6083a-07dd-4731-b4ce-31e188367e35" />

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

## 📌 Notes

- Uses SQLite for persistent storage.
- CRUD operations are performed using SQLModel.
- The API endpoints remain unchanged from the in-memory version.
- Data survives server restarts.

---

## 👩‍💻 Author

**Anuj Upadhayay**
