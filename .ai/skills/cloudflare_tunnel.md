# Skill: Cloudflare Tunnel Deployment

**Objective**: Safely expose the local development environment for external testing or demonstration.

## 🚀 Standard Workflow

### 1. Verification
Ensure the backend is running:
```bash
# Check if port 8000 is active
lsof -i :8000
```

### 2. Tunnel Initiation
Run the pre-installed Cloudflare binary:
```bash
./cloudflared-linux-amd64.deb tunnel --url http://localhost:8000
```

## ⚠️ Important Notes
- **Persistence**: Tunnels created this way are temporary. For a permanent tunnel, refer to the [Local Sharing Guide](file:///mnt/data-disk/ai2cup/AI2CUP/docs/local_sharing_guide.md).
- **Security**: Be aware that once the tunnel is active, anyone with the generated URL can access your local environment.
