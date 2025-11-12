# VLR API Project
## Cloning the repository

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/vlrapi.git
cd vlrapi
```

## Running with docker:
### 1. Build the Docker image

From the root of your project, run:

```bash
docker build -t vlrapi .
```

### 2. Run the container and map port 8000
```bash
docker run -p 8000:8000 vlrapi
```