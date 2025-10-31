"""Simple caching system for parsed UI files."""
import json
import hashlib
import time
import logging
from pathlib import Path
from typing import Optional

CACHE_DIR = Path.home() / ".pygubuai" / "cache"
logger = logging.getLogger(__name__)



def _get_file_hash(filepath: Path) -> str:
    """Get SHA-256 hash of file contents."""
    return hashlib.sha256(filepath.read_bytes()).hexdigest()



def get_cached(filepath: Path) -> Optional[dict]:
    """Get cached parsed UI data if valid."""
    from .utils import validate_path
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        safe_filepath = validate_path(str(filepath), must_exist=True)
        cache_file = CACHE_DIR / f"{safe_filepath.stem}_{_get_file_hash(safe_filepath)}.json"

        if cache_file.exists():
            return json.loads(cache_file.read_text())
    except (ValueError, OSError) as e:
        logger.debug(f"Cache lookup failed for {filepath}: {e}")
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



def cleanup_old_cache(max_age_days: int = 30, max_files: int = 100) -> None:
    """Remove old or excess cache files to prevent bloat."""
    if not CACHE_DIR.exists():
        return

    try:
        files = sorted(CACHE_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime)
        cutoff = time.time() - (max_age_days * 86400)

        for f in files:
            if f.stat().st_mtime < cutoff or len(files) > max_files:
                f.unlink()
                files.remove(f)
                logger.debug(f"Cleaned up cache file: {f.name}")
    except (OSError, PermissionError) as e:
        logger.warning(f"Cache cleanup failed: {e}")


# Auto-cleanup on module import
try:
    cleanup_old_cache()
except (OSError, PermissionError):
    pass  # Silent fail on cleanup
