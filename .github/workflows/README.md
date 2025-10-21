# Backend CI/CD Setup Guide

This directory contains GitHub Actions workflow for automated testing and deployment of the EasyBuyDubai backend.

## Workflow Overview

### CI/CD Pipeline (`ci.yml`)

**Triggers on:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**

1. **test**:
   - Sets up Python 3.11
   - Installs dependencies from `requirements.txt`
   - Runs Flake8 linter for code quality
   - Runs pytest with coverage reporting
   - Uploads coverage to Codecov (optional)

2. **build-docker**:
   - Runs only for push events (not PRs)
   - Builds Docker image for the backend
   - Pushes to Docker Hub with multiple tags
   - Uses build cache for faster builds

3. **deploy-staging**:
   - Runs when code is pushed to `develop` branch
   - Deploys to staging environment

4. **deploy-production**:
   - Runs when code is pushed to `main` branch
   - Deploys to production environment
   - Multiple deployment options available (choose and uncomment)

## Required Secrets

Go to your repository → Settings → Secrets and variables → Actions → New repository secret

### Core Secrets (Always Required)

- `OPENAI_API_KEY`: Your OpenAI API key for the chatbot functionality
  - Get it from: https://platform.openai.com/api-keys

### For Docker Hub (Required for Docker Build)

- `DOCKER_USERNAME`: Your Docker Hub username
  - Sign up at: https://hub.docker.com
- `DOCKER_PASSWORD`: Docker Hub password or access token
  - Use access tokens for better security: Account Settings → Security → New Access Token

### For AWS ECS Deployment

- `AWS_ACCESS_KEY_ID`: AWS access key with ECS permissions
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `ECS_CLUSTER`: ECS cluster name (e.g., easybuydubai-cluster)
- `ECS_SERVICE`: ECS service name (e.g., easybuydubai-backend)

### For Railway Deployment

- `RAILWAY_TOKEN`: Railway API token
  - Get it from: Railway Dashboard → Account Settings → Tokens

### For DigitalOcean App Platform

- `DIGITALOCEAN_ACCESS_TOKEN`: DigitalOcean API token
  - Get it from: DigitalOcean → API → Tokens/Keys

### For SSH Deployment (Self-Hosted)

- `SSH_HOST`: Server hostname or IP address
- `SSH_USERNAME`: SSH username
- `SSH_PRIVATE_KEY`: SSH private key content (paste the entire key)

## Setup Instructions

### 1. Set Up Docker Hub

1. Create account at https://hub.docker.com
2. Create a new repository: `easybuydubai-backend`
3. Generate access token: Account Settings → Security → New Access Token
4. Add `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets to GitHub

### 2. Choose Your Deployment Platform

Uncomment one of the deployment options in `ci.yml`:

- **Railway** (lines 38-43): Easiest option, handles everything automatically
- **AWS ECS** (lines 26-35): Production-grade, full control, more complex
- **DigitalOcean** (lines 45-50): Good balance of simplicity and control
- **SSH/Self-Hosted** (lines 52-61): Maximum control, requires server management

### 3. Add Required Secrets

Add all secrets for your chosen deployment platform (see above).

### 4. Configure Environments (Optional but Recommended)

For better control over production deployments:

1. Go to Settings → Environments
2. Create `production` environment
3. Add protection rules:
   - Required reviewers
   - Wait timer (e.g., 5 minutes)
   - Restrict to `main` branch
4. Create `staging` environment (less restrictive)

### 5. Test the Workflow

1. Create a new branch: `git checkout -b test-ci`
2. Make a small change (e.g., update a comment)
3. Push: `git push origin test-ci`
4. Create a pull request
5. Check "Actions" tab - you should see tests running
6. Merge to `develop` to test staging deployment
7. Merge to `main` to trigger production deployment

## Dockerfile

The workflow expects a `Dockerfile` in the repository root. Here's a recommended Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "run.py"]
```

Or using uvicorn directly:

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Environment Variables in Production

Make sure to set these environment variables in your deployment platform:

**Required:**
- `OPENAI_API_KEY`: Your OpenAI API key

**Recommended:**
- `PORT`: 8000 (or your preferred port)
- `HOST`: 0.0.0.0
- `ENVIRONMENT`: production
- `ALLOWED_ORIGINS`: Your frontend domain(s), comma-separated

**Optional:**
- `DATABASE_URL`: If using a database
- `REDIS_URL`: If using Redis for sessions
- `LOG_LEVEL`: INFO or DEBUG

## Customization

### Adding More Tests

Add test files in a `tests/` directory:

```python
# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
```

Tests will automatically run with `pytest`.

### Adding Security Scanning

Add Snyk or another security scanner:

```yaml
- name: Run Snyk to check for vulnerabilities
  uses: snyk/actions/python@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### Adding Database Migrations

If using Alembic for migrations:

```yaml
- name: Run database migrations
  run: alembic upgrade head
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Customizing Docker Build

To use multi-stage builds or BuildKit features, update the docker/build-push-action configuration:

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    context: .
    file: ./Dockerfile
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    build-args: |
      PYTHON_VERSION=3.11
      APP_ENV=production
    platforms: linux/amd64,linux/arm64
```

## Troubleshooting

### Tests Fail

**Problem:** Tests pass locally but fail in CI

**Solutions:**
- Check Python version matches (workflow uses 3.11)
- Ensure all test dependencies are in `requirements.txt`
- Check for environment-specific issues (paths, env vars)
- Look at the detailed test output in Actions logs

### Linter Errors

**Problem:** Flake8 finds issues in CI

**Solutions:**
- Run `flake8 app` locally to see the same errors
- Fix the code style issues
- Or adjust Flake8 config in `setup.cfg` or `.flake8`

### Docker Build Fails

**Problem:** Docker image build fails

**Solutions:**
- Test Docker build locally: `docker build -t test .`
- Check that all dependencies are in `requirements.txt`
- Verify Dockerfile syntax
- Check Docker Hub credentials are correct

### Deployment Fails

**Problem:** Deployment step fails

**Solutions:**
- Verify all required secrets are set correctly
- Check deployment service status
- Ensure credentials have proper permissions
- Review deployment service logs
- For Railway: Check Railway dashboard for error messages
- For AWS ECS: Check CloudWatch logs
- For SSH: Verify server is accessible and credentials are correct

### Docker Hub Push Rejected

**Problem:** Cannot push to Docker Hub

**Solutions:**
- Verify Docker Hub credentials
- Check repository exists and name matches
- Ensure access token has write permissions
- Try logging in manually: `docker login`

## Performance Optimization

### Faster Builds with Caching

The workflow already uses Docker layer caching. To further optimize:

1. Order Dockerfile commands from least to most frequently changing
2. Use `.dockerignore` to exclude unnecessary files
3. Consider using a smaller base image (alpine)

### Faster Tests

- Use pytest-xdist for parallel test execution
- Add `pytest-cov` flags to skip coverage in PR builds

## Security Best Practices

1. **Use secrets, not environment variables** for sensitive data
2. **Rotate secrets regularly**, especially API keys
3. **Use access tokens** instead of passwords (Docker Hub, GitHub)
4. **Enable branch protection** on `main` and `develop`
5. **Require status checks** before merging
6. **Use environment protection rules** for production
7. **Scan for vulnerabilities** with Snyk or Dependabot
8. **Never log secrets** in workflow outputs

## Monitoring After Deployment

1. **Check application logs** in your deployment platform
2. **Set up error tracking** (Sentry, Rollbar)
3. **Monitor API performance** (response times, error rates)
4. **Set up uptime monitoring** (UptimeRobot, Pingdom)
5. **Configure alerts** for critical failures

## Continuous Improvement

Regular maintenance tasks:

- Update GitHub Actions versions monthly
- Keep Python and dependencies up to date
- Review and optimize Docker image size
- Add more comprehensive tests
- Monitor build times and optimize caching

## Platform-Specific Guides

### Railway

1. Connect GitHub repository in Railway dashboard
2. Set environment variables
3. Railway auto-deploys on push to main
4. View logs in Railway dashboard

### AWS ECS

1. Create ECS cluster and task definition
2. Create ECR repository for Docker images
3. Set up load balancer and target group
4. Configure auto-scaling policies
5. Use CloudWatch for monitoring

### DigitalOcean

1. Create app in DigitalOcean App Platform
2. Connect GitHub repository
3. Configure build settings
4. Set environment variables
5. Choose instance size

### Self-Hosted

1. Set up server with Docker and Docker Compose
2. Configure nginx as reverse proxy
3. Set up SSL with Let's Encrypt
4. Use docker-compose for orchestration
5. Set up log rotation and monitoring

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/marketplace/actions/build-and-push-docker-images)
- [Railway Documentation](https://docs.railway.app)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs)
- [DigitalOcean App Platform](https://docs.digitalocean.com/products/app-platform)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Python Docker Best Practices](https://docs.docker.com/language/python/)

## Need Help?

- Check the main `DEPLOYMENT.md` in the repository root
- Review GitHub Actions logs for detailed error messages
- Consult your deployment platform's documentation
- Check FastAPI documentation for framework-specific issues
