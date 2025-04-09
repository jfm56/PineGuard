# GitHub Actions Configuration

This directory contains GitHub Actions workflow configurations for CI/CD.

## Required Secrets

The following secrets need to be configured in your GitHub repository settings:

1. `DOCKER_TOKEN`
   - Description: Access token for Docker Hub authentication
   - How to obtain:
     1. Log in to [Docker Hub](https://hub.docker.com)
     2. Go to Account Settings > Security
     3. Create a new access token with appropriate permissions
   - Scope needed: `read`, `write`
   - Add to GitHub:
     1. Go to your repository settings
     2. Navigate to Secrets and variables > Actions
     3. Click "New repository secret"
     4. Name: `DOCKER_TOKEN`
     5. Value: Your Docker Hub access token

## Workflow Overview

### CI/CD Pipeline (`ci-cd.yml`)

This workflow handles:
1. Testing
   - Runs Python tests with pytest
   - Generates coverage reports
   - Performs linting checks
2. Building
   - Builds Docker image
   - Tags with version and latest
3. Publishing
   - Pushes to Docker Hub on release
4. Deployment
   - Handles production deployment

### Usage

The workflow is triggered by:
- Push to main branch
- Pull requests to main branch
- Release creation

No manual intervention is needed for normal operation.
