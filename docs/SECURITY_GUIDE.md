# Security Guide

Comprehensive security guide for PygubuAI v0.8.0.

## Table of Contents

- [Security Overview](#security-overview)
- [Threat Model](#threat-model)
- [Security Features](#security-features)
- [Secure Configuration](#secure-configuration)
- [Best Practices](#best-practices)
- [Vulnerability Reporting](#vulnerability-reporting)
- [Security Fixes](#security-fixes)

---

## Security Overview

PygubuAI v0.8.0 includes comprehensive security fixes addressing critical vulnerabilities:

- Path Traversal Prevention (CWE-22)
- Command Injection Prevention (CWE-77/78/88)
- XSS Prevention (CWE-79/80)
- Code Execution Prevention (CWE-94)
- Secure Hashing (CWE-327/328)

**Security Score:** 8/10 (Production Ready)

---

## Threat Model

### Assets

1. **Project Files**: .ui XML files, Python code, configuration
2. **Registry Data**: Project metadata, paths, settings
3. **User Data**: File paths, project names, descriptions
4. **System Access**: File system, Git repositories

### Threats

1. **Path Traversal**: Malicious paths accessing sensitive files
2. **Command Injection**: Shell commands executing arbitrary code
3. **XSS Attacks**: Malicious content in generated files
4. **Code Execution**: Dynamic code execution vulnerabilities
5. **Data Tampering**: Registry or project file modification
6. **Information Disclosure**: Sensitive data exposure

### Mitigations

All critical threats are mitigated in v0.8.0. See [Security Fixes](#security-fixes).

---

## Security Features

### 1. Path Traversal Prevention

**Protection:** All paths validated to prevent ".." traversal.

**Implementation:**
```python
from pygubuai.utils import validate_safe_path

# Validates path is safe
safe_path = validate_safe_path("myproject/ui.xml")

# Raises ValueError for malicious paths
validate_safe_path("../../../etc/passwd")  # BLOCKED
```

**Protected Operations:**
- File creation
- File reading
- Directory operations
- Project registration

### 2. Command Injection Prevention

**Protection:** All subprocess calls use `shell=False` with list arguments.

**Implementation:**
```python
# SECURE: List arguments, no shell
subprocess.run(["git", "init"], cwd=project_path, shell=False)

# INSECURE: String command with shell (NOT USED)
# subprocess.run("git init", shell=True)  # VULNERABLE
```

**Protected Operations:**
- Git initialization
- Git commits
- External tool execution

### 3. XSS Prevention

**Protection:** All user input escaped before XML/HTML generation.

**Implementation:**
```python
from pygubuai.utils import safe_xml_text
import html

# XML escaping
safe_text = safe_xml_text("<script>alert('xss')</script>")
# Returns: "&lt;script&gt;alert('xss')&lt;/script&gt;"

# HTML escaping
safe_html = html.escape("<img src=x onerror=alert(1)>")
```

**Protected Operations:**
- UI XML generation
- README generation
- Error messages
- User-provided text

### 4. Secure Hashing

**Protection:** SHA-256 used for all file hashing (not MD5).

**Implementation:**
```python
from pygubuai.utils import get_file_hash

# Returns 64-char SHA-256 hash
hash_value = get_file_hash(Path("file.txt"))
```

**Use Cases:**
- File integrity checking
- Cache keys
- Change detection

### 5. Input Validation

**Protection:** All user input validated before use.

**Implementation:**
```python
from pygubuai.utils import validate_project_name

# Validates project name
validate_project_name("my_project")  # OK
validate_project_name("my<>project")  # Raises ValidationError
```

**Validated Inputs:**
- Project names
- File paths
- XML content
- User descriptions

---

## Secure Configuration

### File Permissions

```bash
# Registry file (user-only access)
chmod 600 ~/.pygubu-registry.json

# Project directories (user and group)
chmod 750 /var/pygubuai/projects

# Generated files (readable by group)
chmod 640 project/*.ui
chmod 640 project/*.py
```

### Environment Variables

```bash
# Set secure defaults
export PYGUBU_REGISTRY_PATH="~/.pygubu-registry.json"
export PYGUBU_PROJECTS_DIR="/var/pygubuai/projects"

# Disable debug in production
unset PYGUBU_DEBUG
```

### Registry Security

```json
{
  "projects": {
    "myapp": {
      "path": "/var/pygubuai/projects/myapp",
      "description": "My application"
    }
  },
  "active_project": "myapp"
}
```

**Security Notes:**
- No credentials stored
- Paths validated on load
- Atomic writes prevent corruption
- Backup before modifications

---

## Best Practices

### 1. Installation Security

```bash
# Install from trusted source
git clone https://github.com/Teycir/PygubuAI.git
cd PygubuAI

# Verify integrity (if available)
git verify-commit HEAD

# Install in virtual environment
python3 -m venv venv
source venv/bin/activate
pip install .
```

### 2. Project Security

```bash
# Use Git for version control
cd myproject
git init
git add .
git commit -m "Initial commit"

# Set proper permissions
chmod 750 myproject
chmod 640 myproject/*.ui
chmod 640 myproject/*.py

# Regular backups
tar -czf myproject-backup.tar.gz myproject/
```

### 3. Input Validation

```python
# Always validate user input
from pygubuai.utils import validate_project_name, validate_safe_path

try:
    validate_project_name(user_input)
    safe_path = validate_safe_path(user_path)
except ValueError as e:
    print(f"Invalid input: {e}")
```

### 4. Error Handling

```python
# Use specific exceptions
from pygubuai.errors import (
    ProjectNotFoundError,
    ValidationError,
    FileOperationError
)

try:
    registry.get_project(name)
except ProjectNotFoundError:
    # Handle missing project
    pass
except ValidationError:
    # Handle invalid input
    pass
```

### 5. Secure Defaults

```python
# Use secure defaults
registry = Registry()  # Uses ~/.pygubu-registry.json
validate_safe_path(path)  # Validates by default
safe_xml_text(text)  # Escapes by default
```

### 6. Least Privilege

```bash
# Run as non-root user
useradd -m pygubuai
su - pygubuai

# Limit file access
chmod 700 ~/.pygubu
chmod 600 ~/.pygubu-registry.json
```

### 7. Regular Updates

```bash
# Check for updates
cd /opt/PygubuAI
git fetch origin

# Review changes
git log HEAD..origin/main

# Update if safe
git pull origin main
pip install --upgrade .
```

---

## Vulnerability Reporting

### Reporting Process

1. **DO NOT** open public GitHub issues for security vulnerabilities
2. Email security concerns to: [security contact]
3. Include:
   - Vulnerability description
   - Steps to reproduce
   - Impact assessment
   - Suggested fix (if any)

### Response Timeline

- **24 hours**: Initial acknowledgment
- **7 days**: Preliminary assessment
- **30 days**: Fix development and testing
- **Release**: Security patch with advisory

### Disclosure Policy

- Coordinated disclosure after fix is available
- Credit given to reporter (if desired)
- Security advisory published on GitHub

---

## Security Fixes

### v0.8.0 Security Fixes

Complete security overhaul addressing 5 critical vulnerabilities.

#### 1. Path Traversal (CWE-22)

**Severity:** Critical  
**Status:** Fixed

**Vulnerability:**
```python
# BEFORE: No validation
project_path = Path(user_input)
```

**Fix:**
```python
# AFTER: Validated
from pygubuai.utils import validate_safe_path
project_path = validate_safe_path(user_input)
```

**Impact:** Prevents access to files outside project directories.

#### 2. Command Injection (CWE-77/78/88)

**Severity:** Critical  
**Status:** Fixed

**Vulnerability:**
```python
# BEFORE: Shell injection possible
subprocess.run(f"git init {path}", shell=True)
```

**Fix:**
```python
# AFTER: Safe list arguments
subprocess.run(["git", "init"], cwd=path, shell=False)
```

**Impact:** Prevents arbitrary command execution.

#### 3. XSS (CWE-79/80)

**Severity:** High  
**Status:** Fixed

**Vulnerability:**
```python
# BEFORE: No escaping
xml = f"<text>{user_input}</text>"
```

**Fix:**
```python
# AFTER: Escaped
from pygubuai.utils import safe_xml_text
xml = f"<text>{safe_xml_text(user_input)}</text>"
```

**Impact:** Prevents malicious content in generated files.

#### 4. Code Execution (CWE-94)

**Severity:** Critical  
**Status:** Fixed

**Vulnerability:**
```python
# BEFORE: Dynamic execution
exec(template_code)
```

**Fix:**
```python
# AFTER: Static templates
template = TEMPLATES[template_name]
```

**Impact:** Prevents arbitrary code execution.

#### 5. Insecure Hashing (CWE-327/328)

**Severity:** Medium  
**Status:** Fixed

**Vulnerability:**
```python
# BEFORE: MD5 (weak)
hashlib.md5(data).hexdigest()
```

**Fix:**
```python
# AFTER: SHA-256 (strong)
hashlib.sha256(data).hexdigest()
```

**Impact:** Stronger integrity checking.

### Testing

All security fixes have comprehensive test coverage:

```bash
# Run security tests
python -m pytest tests/test_security_fixes.py -v

# 16 tests covering:
# - Path traversal prevention
# - Command injection prevention
# - XSS prevention
# - Secure hashing
```

See [SECURITY_FIXES.md](../SECURITY_FIXES.md) for complete details.

---

## Security Checklist

### Installation
- [ ] Install from official repository
- [ ] Verify Git commit signatures (if available)
- [ ] Use virtual environment
- [ ] Install with `pip install .` (not shell script)

### Configuration
- [ ] Set registry permissions to 600
- [ ] Set project directory permissions to 750
- [ ] Use secure environment variables
- [ ] Disable debug mode in production

### Operations
- [ ] Validate all user input
- [ ] Use Git for version control
- [ ] Regular backups
- [ ] Monitor logs for suspicious activity

### Maintenance
- [ ] Keep PygubuAI updated
- [ ] Update dependencies regularly
- [ ] Review security advisories
- [ ] Test security fixes

---

## Security Resources

### Documentation
- [Security Fixes](../SECURITY_FIXES.md) - Detailed fix documentation
- [Test Strategy](../tests/TEST_STRATEGY.md) - Security testing guide
- [API Reference](API_REFERENCE.md) - Secure API usage

### External Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Python Security](https://python.readthedocs.io/en/stable/library/security_warnings.html)

### Tools
- `bandit`: Python security linter
- `safety`: Dependency vulnerability scanner
- `pytest`: Security test runner

---

## Compliance

### Standards

PygubuAI security follows:
- OWASP Secure Coding Practices
- CWE/SANS Top 25 Most Dangerous Software Errors
- Python Security Best Practices

### Certifications

- No formal certifications required
- Suitable for internal enterprise use
- Not certified for regulated industries (finance, healthcare)

---

## Contact

**Security Issues:** [Create private security advisory on GitHub]  
**General Issues:** https://github.com/Teycir/PygubuAI/issues  
**Documentation:** https://github.com/Teycir/PygubuAI/docs

---

**Version:** 0.8.0  
**Security Score:** 8/10 (Production Ready)  
**Last Security Audit:** v0.8.0 release
