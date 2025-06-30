"""Template loading and validation for brewery automation."""
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

import yaml
import logging

logger = logging.getLogger(__name__)

@dataclass
class BreweryTemplates:
    """Container for brewery simulation templates."""
    organization: Dict[str, Any]
    solution: Dict[str, Any]
    runner: Dict[str, Any]
    workspace: Dict[str, Any]

    @classmethod
    def load_from_directory(cls, template_dir: Path) -> 'BreweryTemplates':
        """Load all required templates from a directory.

        Args:
            template_dir: Directory containing YAML template files

        Returns:
            BreweryTemplates instance with loaded templates

        Raises:
            FileNotFoundError: If template directory or required files are missing
            yaml.YAMLError: If YAML parsing fails
        """
        template_files = {
            'organization': 'Organization.yaml',
            'solution': 'Solution.yaml',
            'runner': 'Runner.yaml',  
            'workspace': 'Workspace.yaml'
        }

        templates = {}
        try:
            for key, filename in template_files.items():
                file_path = template_dir / filename
                if not file_path.exists():
                    raise FileNotFoundError(f"Template file not found: {file_path}")
                
                logger.debug("Loading template", file=str(file_path))
                with open(file_path, 'r') as f:
                    templates[key] = yaml.safe_load(f)
                    
            return cls(
                organization=templates['organization'],
                solution=templates['solution'],
                runner=templates['runner'],
                workspace=templates['workspace']
            )

        except yaml.YAMLError as e:
            logger.error("Failed to parse template", error=str(e))
            raise

    def validate_templates(self) -> None:
        """Validate that all required fields are present in templates.
        
        Raises:
            ValueError: If required fields are missing
        """
        # Check organization template
        if not self.organization.get('name'):
            raise ValueError("Organization template missing 'name' field")

        # Check solution template
        required_solution_fields = ['key', 'name', 'parameters']
        missing = [f for f in required_solution_fields if f not in self.solution]
        if missing:
            raise ValueError(f"Solution template missing fields: {', '.join(missing)}")

        # Check runner template
        required_runner_fields = ['name', 'solutionId', 'runTemplateId']
        missing = [f for f in required_runner_fields if f not in self.runner]
        if missing:
            raise ValueError(f"Runner template missing fields: {', '.join(missing)}")

        # Check workspace template
        required_workspace_fields = ['key', 'name', 'solution']
        missing = [f for f in required_workspace_fields if f not in self.workspace]
        if missing:
            raise ValueError(f"Workspace template missing fields: {', '.join(missing)}")

        logger.info("Template validation successful")