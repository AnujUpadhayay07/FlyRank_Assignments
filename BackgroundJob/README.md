# Background Job API

A simple **FastAPI + Inngest** application that demonstrates how to execute background jobs using event-driven workflows.

The application exposes a FastAPI server and uses the Inngest Development Server to register, trigger, and monitor background functions.

---

## 🚀 Features

* FastAPI REST API
* Health check endpoint
* Inngest integration
* Event-driven background jobs
* Inngest Development Server for local testing
* Background function execution monitoring
* Simple and easy-to-understand project structure

---

## 🛠️ Tech Stack

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Programming language            |
| FastAPI       | Web API framework               |
| Uvicorn       | ASGI server                     |
| Inngest       | Background jobs and workflows   |
| python-dotenv | Environment variable management |

---

## 📁 Project Structure

```text
BackgroundJob/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── inngest_client.py
│   └── background_functions.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔄 How It Works

The application follows this flow:

```text
Client
   │
   ▼
FastAPI Application
   │
   ▼
Inngest Event
   │
   │  app/background-job
   ▼
hello-background-job
   │
   ▼
Background Job Executes
   │
   ▼
Job Completed
```

The background function is triggered when the following Inngest event is received:

```text
app/background-job
```

---

## ⚙️ Inngest Function

The project contains the following background function:

```text
hello-background-job
```

It is triggered by:

```text
app/background-job
```

The function logs:

```text
Background job started
```

and returns:

```text
Background job completed successfully
```

---

## 🔌 API Endpoints

### Health Check

**Endpoint:**

```http
GET /health
```

**URL:**

```text
http://127.0.0.1:8000/health
```

**Response:**

```json
{
  "status": "ok"
}
```

---

### Inngest Endpoint

The Inngest handler is available at:

```text
http://127.0.0.1:8000/api/inngest
```

This endpoint is used by the Inngest Development Server to communicate with the FastAPI application.

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd BackgroundJob
```

---

### 2. Create Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
```

---

### 3. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

After activation, the terminal should show:

```text
(venv)
```

---

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```text
BackgroundJob/
├── .env
├── README.md
└── app/
```

Add the required Inngest signing key:

```env
INNGEST_SIGNING_KEY=<your-valid-inngest-signing-key>
```

> **Important:** Never commit real secret keys or `.env` files containing secrets to GitHub.

Make sure `.env` is included in `.gitignore`.

---

# ▶️ Running the Application

The project requires **two terminals**.

You need to run:

1. FastAPI server
2. Inngest Development Server

Keep both terminals running while testing the application.

---

## Terminal 1 — Start FastAPI

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Start the FastAPI server:

```powershell
uvicorn app.main:app --reload --port 8000
```

You should see:

```text
Uvicorn running on http://127.0.0.1:8000
Application startup complete.
```

The FastAPI application is now running at:

```text
http://127.0.0.1:8000
```

---

## Terminal 2 — Start Inngest

Open another PowerShell terminal.

Go to the project directory:

```powershell
cd C:\Users\ANKITA UPADHAYAY\Desktop\TaskAPI\BackgroundJob
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Start the Inngest Development Server:

```powershell
npx --ignore-scripts=false inngest-cli@latest dev -u http://127.0.0.1:8000/api/inngest --no-discovery
```

You should see:

```text
Inngest Dev Server online
```

The Inngest Development Server will be available at:

```text
http://127.0.0.1:8288
```

---

# 🖥️ Inngest Dashboard

Open the following URL in your browser:

```text
http://127.0.0.1:8288
```

The Inngest Development Server provides a dashboard where you can view:

* Applications
* Functions
* Runs
* Events

---

## 📋 Registered Function

After starting both servers, the Inngest dashboard should display:

```text
hello-background-job
```

The application should be registered as:

```text
background-job-api
```

The App URL is:

```text
http://localhost:8000/api/inngest
```

---

# 📤 Triggering an Event

The background function listens for the following event:

```text
app/background-job
```

An Inngest event payload must contain a `name` field.

Example:

```json
{
  "name": "app/background-job"
}
```

When this event is received, Inngest starts the:

```text
hello-background-job
```

function.

---

# ✅ Verifying the Background Job

After triggering the event:

1. Open the Inngest dashboard.
2. Go to **Runs**.
3. Find the `hello-background-job` function.
4. Open the corresponding run.
5. Check the status.

A successful execution should show:

```text
COMPLETED
```

Example:

```text
Status:     COMPLETED
Function:   hello-background-job
Trigger:    app/background-job
```

This confirms that the background job was successfully executed.

---

# 🧪 Testing Health Endpoint

You can test the FastAPI health endpoint from your browser:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

You can also open the automatically generated FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 📊 Current Setup

| Component           | URL                                 | Status    |
| ------------------- | ----------------------------------- | --------- |
| FastAPI             | `http://127.0.0.1:8000`             | Running   |
| Health Check        | `http://127.0.0.1:8000/health`      | Available |
| Inngest API         | `http://127.0.0.1:8000/api/inngest` | Connected |
| Inngest Dashboard   | `http://127.0.0.1:8288`             | Running   |
| Background Function | `hello-background-job`              | Working   |

---

# 📝 Important Notes

* Both FastAPI and Inngest servers must be running during local testing.
* The FastAPI server runs on port `8000`.
* The Inngest Development Server runs on port `8288`.
* The Inngest endpoint is `/api/inngest`.
* Every Inngest event must contain a `name`.
* Keep sensitive environment variables out of GitHub.
* Use `.gitignore` to prevent `.env` from being committed.

---

# 🎯 Project Status

The project has been successfully tested locally.

The `hello-background-job` function successfully executes when the `app/background-job` event is triggered.

Example successful run:

```text
Status: COMPLETED
Function: hello-background-job
Trigger: app/background-job
```

---

## 👨‍💻 Author

**Anuj Upadhayay**

---

## 📄 License

This project is created for learning and development purposes.
