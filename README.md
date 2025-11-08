# auth-service

A FastAPI-based authentication service with JWT token support and RSA key pair encryption.

## Features

- User registration and authentication
- JWT access and refresh tokens with RSA encryption
- Email verification system
- Password management
- User profile management
- Admin functionality
- Project-specific RSA key pairs (external to Docker image)

## RSA Keys Configuration

This service uses RSA key pairs for JWT token signing. Keys are stored **outside** the Docker image to allow each deployment/project to have its own unique key pair.

### Default Behavior

- Keys are stored in a `keys/` directory at the project root (same level as `src/`)
- If keys don't exist, they are automatically generated on first run
- Keys are git-ignored and not included in version control

### Custom Keys Location

You can override the default keys directory using the `RSA_KEYS_DIR` environment variable:

```bash
export RSA_KEYS_DIR=/path/to/your/keys
```

Or in docker-compose:
```yaml
environment:
  - RSA_KEYS_DIR=/custom/path/keys
```

## Running with Docker Compose

The `docker-compose.yml` file includes a volume mount for the keys directory:

```bash
docker-compose up -d
```

This will:
1. Build the Docker image
2. Mount `./keys` from your host to `/app/keys` in the container
3. Generate keys on first run if they don't exist
4. Persist keys across container restarts

## Multiple Projects

To use this service for multiple projects with separate key pairs:

1. Clone or deploy the service to different directories/environments
2. Each deployment will have its own `keys/` directory
3. Keys remain external to the Docker image, ensuring isolation

Example structure:
```
/projects/
  ├── project-a/
  │   ├── auth-service/
  │   │   ├── keys/          # Project A's keys
  │   │   ├── src/
  │   │   └── docker-compose.yml
  │
  └── project-b/
      └── auth-service/
          ├── keys/          # Project B's keys
          ├── src/
          └── docker-compose.yml
```

## Environment Variables

- `FASTAPI_HOST` - Host to bind to (default: 0.0.0.0)
- `FASTAPI_PORT` - Port to bind to (default: 8000)
- `CURRENT_ENV` - Set to "development" for debug mode
- `RSA_KEYS_DIR` - Custom path for RSA keys (optional)

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py
```

Keys will be automatically generated in `./keys/` on first run.