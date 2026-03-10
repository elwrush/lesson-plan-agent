import os
from pathlib import Path

class PresentationConfig:
    def __init__(self, md_path_str):
        self.md_path = Path(md_path_str).resolve()
        
        # Core Architecture Paths
        self.lesson_dir = self.md_path.parent
        self.lesson_name = self.lesson_dir.name
        self.project_root = Path(os.path.abspath("."))
        
        # Generation Outputs (Local GitHub Pages Structure)
        self.published_dir = self.lesson_dir / "published"
        self.output_html = self.published_dir / "index.html"
        
        # Intermediate/Internal Files
        self.internal_json = self.lesson_dir / "presentation.json"
        
        # Source of Truth
        self.source_text_md = self.lesson_dir / "SOURCE_TEXT.md"
        self.visual_plan_md = self.lesson_dir / "visual_plan.md"
        
        # Asset Directories
        self.source_images = self.lesson_dir / "images"
        self.published_images = self.published_dir / "images"
        
        # Skill & Template Paths
        self.skill_dir = self.project_root / "skills" / "06-creating-html-presentation"
        self.scripts_dir = self.skill_dir / "scripts"
        self.templates_dir = self.skill_dir / "templates"
        
    def ensure_directories(self):
        """Creates necessary output directories if they don't exist."""
        self.published_dir.mkdir(exist_ok=True)
        self.published_images.mkdir(exist_ok=True)
        
    def get_dict(self):
        """Returns paths as a dictionary for easy inspection or passing to templates."""
        return {
            "lesson_name": self.lesson_name,
            "lesson_dir": str(self.lesson_dir),
            "project_root": str(self.project_root),
            "published_dir": str(self.published_dir),
            "output_html": str(self.output_html),
            "internal_json": str(self.internal_json),
            "source_images": str(self.source_images),
            "published_images": str(self.published_images)
        }
