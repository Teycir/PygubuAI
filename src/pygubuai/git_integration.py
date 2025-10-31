"""Git integration for project management"""
import subprocess
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)



def is_git_available() -> bool:
    """Check if git is installed"""
    try:
        subprocess.run(['git', '--version'], shell=False, capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False



def init_git_repo(project_path: Path, initial_commit: bool = True) -> bool:
    """Initialize git repository in project directory"""
    if not is_git_available():
        logger.warning("Git not available, skipping repository initialization")
        return False

    try:
        subprocess.run(['git', 'init'], shell=False, cwd=str(project_path), capture_output=True, check=True)
        logger.info(f"Initialized git repository in {project_path}")

        # Create .gitignore
        gitignore = project_path / ".gitignore"
        gitignore.write_text(generate_gitignore())

        if initial_commit:
            subprocess.run(['git', 'add', '.'], shell=False, cwd=str(project_path), capture_output=True, check=True)
            subprocess.run(
                ['git', 'commit', '-m', 'Initial commit: PygubuAI project'],
                shell=False,
                cwd=str(project_path),
                capture_output=True,
                check=True
            )
            logger.info("Created initial commit")

        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Git initialization failed: {e}")
        return False



def generate_gitignore() -> str:
    """Generate .gitignore content for Python/Tkinter projects"""
    return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PygubuAI
.pygubu-workflow.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
"""



def git_commit(project_path: Path, message: str, files: Optional[list] = None) -> bool:
    """Commit changes to git repository"""
    if not is_git_available():
        return False

    try:
        if files:
            subprocess.run(['git', 'add'] + files, shell=False, cwd=str(project_path), capture_output=True, check=True)
        else:
            subprocess.run(['git', 'add', '.'], shell=False, cwd=str(project_path), capture_output=True, check=True)

        subprocess.run(
            ['git', 'commit', '-m', message],
            shell=False,
            cwd=str(project_path),
            capture_output=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False
