"""Dynamic template discovery and validation system."""
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from .logging_config import get_logger
from .template_data import TEMPLATES, validate_widget

logger = get_logger(__name__)


class TemplateRegistry:
    """Registry for discovering and managing templates from multiple sources."""

    def __init__(self):
        """Initialize template registry with built-in and user templates."""
        self.templates = TEMPLATES.copy()
        self._discover_user_templates()

    def _discover_user_templates(self) -> None:
        """Discover templates from user template directory.

        Searches ~/.pygubuai/templates/ for JSON template files.
        """
        user_template_dir = Path.home() / ".pygubuai" / "templates"
        if not user_template_dir.exists():
            logger.debug(f"User template directory not found: {user_template_dir}")
            return

        for template_file in user_template_dir.glob("*.json"):
            try:
                template_data = json.loads(template_file.read_text())
                template_name = template_file.stem

                if self._validate_template(template_data):
                    self.templates[template_name] = template_data
                    logger.info(f"Loaded user template: {template_name}")
            except (json.JSONDecodeError, OSError) as e:
                logger.warning(f"Failed to load template {template_file}: {e}")

    def _validate_template(self, template: Dict[str, Any]) -> bool:
        """Validate template structure and content.

        Args:
            template: Template dictionary to validate

        Returns:
            True if template is valid, False otherwise
        """
        required_keys = ["description", "widgets"]

        # Check required keys
        for key in required_keys:
            if key not in template:
                logger.error(f"Template missing required key: {key}")
                return False

        # Validate widgets
        if not isinstance(template["widgets"], list):
            logger.error("Template 'widgets' must be a list")
            return False

        for widget in template["widgets"]:
            try:
                validate_widget(widget)
            except ValueError as e:
                logger.error(f"Invalid widget in template: {e}")
                return False

        # Validate callbacks if present
        if "callbacks" in template:
            if not isinstance(template["callbacks"], list):
                logger.error("Template 'callbacks' must be a list")
                return False

        return True

    def get_template(self, name: str) -> Optional[Dict[str, Any]]:
        """Get template by name.

        Args:
            name: Template name

        Returns:
            Template dictionary or None if not found
        """
        return self.templates.get(name)

    def list_templates(self) -> List[tuple]:
        """List all available templates.

        Returns:
            List of (name, description, source) tuples
        """
        result = []
        for name, tmpl in self.templates.items():
            source = "built-in" if name in TEMPLATES else "user"
            result.append((name, tmpl["description"], source))
        return result

    def register_template(self, name: str, template: Dict[str, Any]) -> bool:
        """Register a new template programmatically.

        Args:
            name: Template name
            template: Template dictionary

        Returns:
            True if registered successfully, False otherwise
        """
        if not self._validate_template(template):
            return False

        self.templates[name] = template
        logger.info(f"Registered template: {name}")
        return True

    def save_user_template(self, name: str, template: Dict[str, Any]) -> bool:
        """Save template to user template directory.

        Args:
            name: Template name
            template: Template dictionary

        Returns:
            True if saved successfully, False otherwise
        """
        if not self._validate_template(template):
            return False

        user_template_dir = Path.home() / ".pygubuai" / "templates"
        user_template_dir.mkdir(parents=True, exist_ok=True)

        template_file = user_template_dir / f"{name}.json"
        try:
            template_file.write_text(json.dumps(template, indent=2))
            self.templates[name] = template
            logger.info(f"Saved user template: {name}")
            return True
        except OSError as e:
            logger.error(f"Failed to save template {name}: {e}")
            return False


# Global registry instance
_registry: Optional[TemplateRegistry] = None


def get_template_registry() -> TemplateRegistry:
    """Get or create global template registry instance.

    Returns:
        Global TemplateRegistry instance
    """
    global _registry
    if _registry is None:
        _registry = TemplateRegistry()
    return _registry
