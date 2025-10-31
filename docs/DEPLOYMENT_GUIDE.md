# Deployment Guide

Complete guide for deploying PygubuAI in production environments.

## Table of Contents

- [Installation Methods](#installation-methods)
- [System Requirements](#system-requirements)
- [Production Setup](#production-setup)
- [Configuration](#configuration)
- [Multi-User Setup](#multi-user-setup)
- [CI/CD Integration](#cicd-integration)
- [Docker Deployment](#docker-deployment)
- [Monitoring](#monitoring)

---

## Installation Methods

### Method 1: pip install (Recommended)

Best for production environments and team deployments.

```bash
# Clone repository
git clone https://github.com/Teycir/PygubuAI.git
cd PygubuAI

# Install in production mode
pip install .

# Or install in development mode
pip install -e ".[dev]"

# Verify installation
pygubu-create --version
pygubu-register list
```

### Method 2: System-Wide Installation

For shared systems with multiple users.

```bash
# Install system-wide (requires sudo)
sudo pip install .

# Verify all users can access
pygubu-create --version
```

### Method 3: Virtual Environment (Isolated)

For isolated project environments.

```bash
# Create virtual environment
python3 -m venv pygubuai-env
source pygubuai-env/bin/activate  # Linux/Mac
# pygubuai-env\Scripts\activate  # Windows

# Install
pip install /path/to/PygubuAI

# Verify
pygubu-create --version
```

---

## System Requirements

### Minimum Requirements

- Python 3.9 or higher
- 100 MB disk space
- 256 MB RAM
- Linux, macOS, or Windows

### Recommended Requirements

- Python 3.11 or higher
- 500 MB disk space
- 512 MB RAM
- Git installed
- Tkinter support

### Dependencies

**Runtime:**
```
pygubu >= 0.39
pygubu-designer >= 0.42
rich >= 13.0
pydantic >= 2.0
```

**Development:**
```
coverage >= 7.0
pytest >= 7.0
```

### Verify Dependencies

```bash
# Check Python version
python3 --version

# Check pip
pip --version

# Check tkinter
python3 -c "import tkinter; print('Tkinter OK')"

# Check Git
git --version
```

---

## Production Setup

### Step 1: Install PygubuAI

```bash
cd /opt
sudo git clone https://github.com/Teycir/PygubuAI.git
cd PygubuAI
sudo pip install .
```

### Step 2: Configure System Paths

```bash
# Add to system PATH (if needed)
export PATH="$PATH:/usr/local/bin"

# Make permanent (add to /etc/profile or ~/.bashrc)
echo 'export PATH="$PATH:/usr/local/bin"' >> ~/.bashrc
```

### Step 3: Set Up Project Directory

```bash
# Create projects directory
mkdir -p /var/pygubuai/projects
chmod 755 /var/pygubuai/projects

# Set ownership (if multi-user)
sudo chown -R pygubuai:pygubuai /var/pygubuai
```

### Step 4: Initialize Registry

```bash
# Create registry directory
mkdir -p ~/.pygubu
touch ~/.pygubu-registry.json

# Set permissions
chmod 600 ~/.pygubu-registry.json
```

### Step 5: Enable Trigger Word (Optional)

```bash
# Scan for existing projects
bash scripts/setup-trigger.sh scan /var/pygubuai/projects

# Or mark specific directory
bash scripts/setup-trigger.sh mark /path/to/project
```

### Step 6: Verify Installation

```bash
# Test commands
pygubu-create --version
pygubu-register list
pygubu-status

# Create test project
cd /tmp
pygubu-create test 'test application'
cd test
python3 test.py
```

---

## Configuration

### Registry Configuration

Location: `~/.pygubu-registry.json`

```json
{
  "projects": {
    "myapp": {
      "path": "/var/pygubuai/projects/myapp",
      "description": "My application",
      "tags": ["production"],
      "created": "2024-01-01T00:00:00",
      "modified": "2024-01-01T00:00:00"
    }
  },
  "active_project": "myapp",
  "settings": {
    "auto_git": true,
    "default_theme": "clam"
  }
}
```

### Environment Variables

```bash
# Set registry location
export PYGUBU_REGISTRY_PATH="~/.pygubu-registry.json"

# Set projects directory
export PYGUBU_PROJECTS_DIR="/var/pygubuai/projects"

# Enable debug mode
export PYGUBU_DEBUG=1

# Set default theme
export PYGUBU_DEFAULT_THEME="clam"
```

### Amazon Q Integration

Location: `~/.amazonq/prompts/pygubu-context.md`

Automatically created by setup script. Contains PygubuAI context for AI assistance.

---

## Multi-User Setup

### Shared System Configuration

```bash
# Create shared group
sudo groupadd pygubuai

# Add users to group
sudo usermod -a -G pygubuai user1
sudo usermod -a -G pygubuai user2

# Create shared projects directory
sudo mkdir -p /var/pygubuai/projects
sudo chown root:pygubuai /var/pygubuai/projects
sudo chmod 2775 /var/pygubuai/projects

# Set default permissions for new files
sudo chmod g+s /var/pygubuai/projects
```

### Per-User Registry

Each user maintains their own registry:

```bash
# User 1
~/.pygubu-registry.json

# User 2
~/.pygubu-registry.json
```

### Shared Projects

```bash
# Create shared project
cd /var/pygubuai/projects
pygubu-create shared_app 'shared application'

# Set permissions
chmod -R g+rw shared_app
```

---

## CI/CD Integration

### GitHub Actions

`.github/workflows/pygubuai.yml`:

```yaml
name: PygubuAI CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      
      - name: Run tests
        run: |
          python -m pytest tests/ -v --cov=src/pygubuai
      
      - name: Validate projects
        run: |
          pygubu-validate myproject
```

### GitLab CI

`.gitlab-ci.yml`:

```yaml
stages:
  - test
  - validate

test:
  stage: test
  image: python:3.11
  script:
    - pip install -e ".[dev]"
    - pytest tests/ -v --cov=src/pygubuai
  coverage: '/TOTAL.*\s+(\d+%)$/'

validate:
  stage: validate
  image: python:3.11
  script:
    - pip install .
    - pygubu-validate myproject
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    stages {
        stage('Install') {
            steps {
                sh 'pip install -e ".[dev]"'
            }
        }
        
        stage('Test') {
            steps {
                sh 'pytest tests/ -v --cov=src/pygubuai'
            }
        }
        
        stage('Validate') {
            steps {
                sh 'pygubu-validate myproject'
            }
        }
    }
}
```

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    tk \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy PygubuAI
COPY . /app/PygubuAI

# Install PygubuAI
RUN pip install --no-cache-dir /app/PygubuAI

# Create projects directory
RUN mkdir -p /var/pygubuai/projects

# Set environment
ENV PYGUBU_PROJECTS_DIR=/var/pygubuai/projects

# Expose volume for projects
VOLUME ["/var/pygubuai/projects"]

# Default command
CMD ["bash"]
```

### Build and Run

```bash
# Build image
docker build -t pygubuai:latest .

# Run container
docker run -it --rm \
  -v $(pwd)/projects:/var/pygubuai/projects \
  pygubuai:latest

# Create project in container
docker run -it --rm \
  -v $(pwd)/projects:/var/pygubuai/projects \
  pygubuai:latest \
  pygubu-create myapp 'my application'
```

### Docker Compose

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  pygubuai:
    build: .
    volumes:
      - ./projects:/var/pygubuai/projects
      - ./registry:/root/.pygubu
    environment:
      - PYGUBU_PROJECTS_DIR=/var/pygubuai/projects
    command: tail -f /dev/null
```

---

## Monitoring

### Health Checks

```bash
#!/bin/bash
# health-check.sh

# Check if commands are available
command -v pygubu-create >/dev/null 2>&1 || exit 1
command -v pygubu-register >/dev/null 2>&1 || exit 1

# Check registry is readable
test -r ~/.pygubu-registry.json || exit 1

# Check projects directory
test -d /var/pygubuai/projects || exit 1

echo "Health check passed"
exit 0
```

### Logging

```bash
# Enable debug logging
export PYGUBU_DEBUG=1

# Log to file
pygubu-create myapp 'test' 2>&1 | tee pygubu.log

# Monitor logs
tail -f pygubu.log
```

### Metrics

```bash
# Count projects
pygubu-register list | wc -l

# Check disk usage
du -sh /var/pygubuai/projects

# Check registry size
ls -lh ~/.pygubu-registry.json
```

---

## Backup and Recovery

### Backup Registry

```bash
# Backup registry
cp ~/.pygubu-registry.json ~/.pygubu-registry.json.backup

# Automated backup
0 0 * * * cp ~/.pygubu-registry.json ~/.pygubu-registry.json.$(date +\%Y\%m\%d)
```

### Backup Projects

```bash
# Backup all projects
tar -czf pygubu-projects-$(date +%Y%m%d).tar.gz /var/pygubuai/projects

# Restore projects
tar -xzf pygubu-projects-20240101.tar.gz -C /
```

### Recovery

```bash
# Restore registry
cp ~/.pygubu-registry.json.backup ~/.pygubu-registry.json

# Rebuild registry from projects
pygubu-register scan /var/pygubuai/projects
```

---

## Upgrade Procedure

### Upgrade PygubuAI

```bash
# Backup first
cp ~/.pygubu-registry.json ~/.pygubu-registry.json.backup

# Pull latest version
cd /opt/PygubuAI
git pull origin main

# Reinstall
pip install --upgrade .

# Verify
pygubu-create --version

# Test
pygubu-register list
```

### Rollback

```bash
# Uninstall current version
pip uninstall pygubuai

# Install specific version
cd /opt/PygubuAI
git checkout v0.7.0
pip install .

# Restore registry if needed
cp ~/.pygubu-registry.json.backup ~/.pygubu-registry.json
```

---

## Security Considerations

See [Security Guide](SECURITY_GUIDE.md) for detailed security information.

**Quick Checklist:**
- [ ] Install from trusted source
- [ ] Verify file permissions (600 for registry)
- [ ] Use virtual environments for isolation
- [ ] Keep dependencies updated
- [ ] Enable Git for version control
- [ ] Regular backups
- [ ] Monitor logs for suspicious activity

---

## Troubleshooting

See [Troubleshooting Guide](TROUBLESHOOTING.md) for detailed troubleshooting.

**Common Issues:**
- Command not found: Check PATH
- Permission denied: Check file permissions
- Registry corrupted: Restore from backup
- Import errors: Reinstall dependencies

---

## Support

- GitHub Issues: https://github.com/Teycir/PygubuAI/issues
- Documentation: https://github.com/Teycir/PygubuAI/docs
- Pygubu: https://github.com/alejandroautalan/pygubu

---

**Version:** 0.8.0  
**Last Updated:** 2024
