"""Simple caching system for parsed UI files."""
import json
import hashlib
from pathlib import Path
from typing import Any, Optional

CACHE_DIR = Path.home() / ".pygubuai" / "cache"


def _get_file_hash(filepath: Path) -> str:
    """Get MD5 hash of file contents."""
    return hashlib.md5(filepath.read_bytes()).hexdigest()


def get_cached(filepath: Path) -> Optional[dict]:
    """Get cached parsed UI data if valid."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{filepath.stem}_{_get_file_hash(filepath)}.json"
    
    if cache_file.exists():
        return json.loads(cache_file.read_text())
    return None


def set_cached(filepath: Path, data: dict) -> None:
    """Cache parsed UI data."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{filepath.stem}_{_get_file_hash(filepath)}.json"
    cache_file.write_text(json.dumps(data))


def clear_cache(filepath: Optional[Path] = None) -> None:
    """Clear cache for specific file or all."""
    if filepath:
        for f in CACHE_DIR.glob(f"{filepath.stem}_*.json"):
            f.unlink()
    else:
        for f in CACHE_DIR.glob("*.json"):
            f.unlink()
