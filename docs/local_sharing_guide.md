# Local Development and Sharing Guide

This document outlines how to run the AI2CUP platform locally for development and how to securely share your local instance with external collaborators via Cloudflare. It includes both a "Native" (non-Docker) setup and a Docker-based setup.

## Table of Contents
1. [Native Setup (Without Docker)](#native-setup-without-docker)
2. [Docker Setup](#docker-setup)
3. [Sharing via Cloudflare Tunnel](#sharing-via-cloudflare-tunnel)

---

## Native Setup (Without Docker)

Use this method if you do not have Docker installed. It assumes you have **Python 3.9+** and **Node.js (with npm)** installed.

### 1. Set up the Backend (Terminal 1)
Open a terminal and configure the FastAPI backend server:

**Note:** For quick works, please go to [Makefile](../Makefile) to see the shortcuts or just run `make dev-backend` to start the backend server and `make dev-frontend` to start the frontend server and `make dev` to start both servers. 
If you are using Docker, you can run `make dev-docker` to start both services. You will have a new frontend at port 3000 and a new backend at port 8000.

```bash
cd apps/backend

# Copy the environment configuration
cp .env.example .env

# Create and activate a virtual environment (keeps things clean)
python3 -m venv venv
source venv/bin/activate

# Install the required Python dependencies
# pip install -r requirements.txt

# Start the backend server (runs on port 8000)
uvicorn app.main:app --reload --port 8000
```


*Note: This isolates backend dependencies and runs the API locally on port 8000.*

### 2. Set up the Frontend (Terminal 2)
Open a second terminal window and configure the Vue.js frontend:

```bash
cd apps/frontend 

# Copy the environment configuration
cp .env.example .env

# Install Node.js dependencies
npm install

# Start the Vite development server (runs on port 5173)
npm run dev
```
*Note: Vite handles proxying any `/api` requests automatically to `localhost:8000` so no CORS issues occur. You can visit `http://localhost:5173` to test it.*

---

## Docker Setup

Use this method if you have **Docker** and **Docker Compose** installed. This runs the app in isolated containers.

### 1. Set up Environment Variables
```bash
cd apps/backend
cp .env.example .env
```

### 2. Build and Start the Application
From the root of the repository, use the provided `Makefile`:

```bash
# Builds the Docker images for frontend and backend
make build

# Spins up the containers in the background
make up
```

*(Alternatively, run `cd infrastructure && docker-compose up -d --build` if you do not have `make` installed)*

*Note: The Frontend container uses Nginx and runs on port `3000`. It proxies `/api` calls directly to the Backend container internally. You can visit `http://localhost:3000` to test it.*

---

## Sharing via Cloudflare Tunnel

Whether you ran the app natively or via Docker, you can securely share it with external users using Cloudflare's Quick Tunnels without needing a Cloudflare account. You also do not need to alter router or firewall settings.

### 1. Install Cloudflared
If `cloudflared` is not installed on your Linux machine, run:
```bash
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```
*(For macOS, run `brew install cloudflared`)*

### 2. Expose the Application
Open a fresh terminal window. Depending on how you started the app, run the tunnel command for the corresponding port.

**If using the Native Setup (Port 5173):**
```bash
cloudflared tunnel --url http://localhost:5173
```

**If using the Docker Setup (Port 3000):**
```bash
cloudflared tunnel --url http://localhost:3000
```

### 3. Share the Link
Once the command is running, Cloudflare will output a temporary URL (e.g., `https://random-words.trycloudflare.com`). Share this exact URL with your collaborators! They will be securely routed straight into your locally running application.

### Safely Stopping
- Stop the Cloudflare tunnel by pressing `Ctrl + C` in its terminal.
- **Native:** Stop the frontend and backend servers with `Ctrl + C` in their respective terminals.
- **Docker:** Run `make down` from the repository root to gracefully tear down your docker containers.
