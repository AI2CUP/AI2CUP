# AI2CUP Deployment Guide

This document covers deployment of AI2CUP using Docker Compose and the always-on production path with systemd + Cloudflare Tunnel.

If your host has tight Docker storage (common when `/var` is small), use the native path in `deploy/install_native_stack.sh`.

## Prerequisites
- Docker Engine & Docker Compose installed on the host machine.
- Git (to check out the repository).
- Target host has ports `8000` and `80` (or `3000`) available.

## Deployment Steps

1. **Clone the Source Code**
   ```bash
   git clone <repository_url>
   cd AI2CUP
   ```

2. **Configure Environment Variables**
   The backend relies on the `.env` file to function.
   ```bash
   cd apps/backend
   cp .env.example .env
   # Edit .env with your production values (e.g., set AI2CUP_DEBUG=false)
   ```

3. **Start the Infrastructure**
   We provide a Makefile for convenience. From the root directory:
   ```bash
   make up
   ```
   If you don't have `make` installed:
   ```bash
   cd infrastructure
   docker-compose up -d --build
   ```

4. **Verify Deployment**
   - Frontend is mapped to `http://localhost:3000` by default.
   - Backend API is mapped to `http://localhost:8000/api/v1/health`.
   - The Nginx reverse proxy running inside the frontend container also maps `/api` to the backend.

   ## Always-On Production Path (Recommended)

   Use the deployment artifacts under `deploy/` for persistent startup and public reachability.

   1. **Run one-time host setup**
      ```bash
      chmod +x deploy/install_host_stack.sh deploy/compose-stack.sh
      bash deploy/install_host_stack.sh
      ```

   2. **Configure backend env for production**
      ```bash
      cd apps/backend
      cp .env.example .env
      # Set AI2CUP_DEBUG=false
      # Set AI2CUP_CORS_ORIGINS to your public frontend origin(s)
      ```

   3. **Start stack and enable systemd service**
      ```bash
      cd /mnt/data-disk/ai2cup/AI2CUP
      bash deploy/compose-stack.sh up-detached
      sudo systemctl enable --now ai2cup-stack.service
      ```

   4. **Create and run a named Cloudflare Tunnel**
      ```bash
      cloudflared tunnel login
      cloudflared tunnel create ai2cup
      cloudflared tunnel route dns ai2cup app.example.com
      cloudflared tunnel route dns ai2cup api.example.com
      sudo systemctl enable --now cloudflared-ai2cup.service
      ```

   5. **Verify from outside network**
      - Open `https://app.example.com`
      - Check API through your public route

   ## Native Always-On Path (Recommended for Small `/var`)

   1. **Run native installer**
      ```bash
      chmod +x deploy/install_native_stack.sh
      bash deploy/install_native_stack.sh
      ```

   2. **Set up Cloudflare named tunnel**
      ```bash
      cloudflared tunnel login
      cloudflared tunnel create ai2cup
      cloudflared tunnel route dns ai2cup app.example.com
      sudo cp deploy/ai2cup-config.example.yml /etc/cloudflared/ai2cup-config.yml
      # Edit tunnel UUID + hostname in /etc/cloudflared/ai2cup-config.yml
      sudo systemctl enable --now cloudflared-ai2cup.service
      ```

   3. **Validate always-on services**
      ```bash
      sudo systemctl status ai2cup-backend.service
      sudo systemctl status nginx
      sudo systemctl status cloudflared-ai2cup.service
      ```

### Shutting Down
To gracefully stop the deployment:
```bash
make down
# or from infrastructure/ directory: docker-compose down
```

## Production Security Notes
- Re-configure `AI2CUP_CORS_ORIGINS` to accept only the production frontend domain(s).
- Ensure backend debug mode is disabled: `AI2CUP_DEBUG=false`.
- Use a named Cloudflare tunnel instead of quick tunnel URLs for stable always-on access.
- Keep service logs monitored with `journalctl` and container logs via compose.
