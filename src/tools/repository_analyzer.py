"""
Repository Analyzer - Analyzes repositories and generates optimization strategies.

Uses UnifiedAIClient for AI-powered analysis with model-size-based fallback.
Aligned with AGENTS.md Dec 2025 specification.
"""

import json
import logging
from typing import Any

logger = logging.getLogger("RepositoryAnalyzer")


class RepositoryAnalyzer:
    """
    Analyzes repositories and generates optimization strategies using AI.
    Now uses UnifiedAIClient with automatic model fallback.
    """

    def __init__(self, ai_client, fallback_client=None) -> None:
        """Initialize with UnifiedAIClient (fallback param ignored for compatibility)."""
        self.ai = ai_client
        # fallback_client ignored - UnifiedAIClient handles fallback internally

    def detect_repo_type(self, files: list[str]) -> str:
        """Detect repository type from file structure."""
        files_lower = [f.lower() for f in files]

        if any("manifest.json" in f for f in files_lower):
            return "browser_extension"
        if any(f.endswith("index.html") for f in files_lower):
            return "website"
        if any(f in files_lower for f in ["pyproject.toml", "setup.py", "requirements.txt"]):
            return "python"
        if any(f in files_lower for f in ["package.json", "tsconfig.json"]):
            return "typescript"
        if "cargo.toml" in files_lower:
            return "rust"
        if "go.mod" in files_lower:
            return "go"
        return "generic"

    def analyze_repository(
        self,
        repo: str,
        files: list[str],
        readme: str,
        language: str
    ) -> dict:
        """
        Analyze repository and generate optimization strategy using UnifiedAI.

        Uses APEX Naming Convention: <Product>-<Function>-<Platform>-<Type>

        Returns:
            {
                "action": "UPDATE" | "ARCHIVE",
                "new_name": "Professional-Apex-Name-Here",
                "description": "Description under 300 chars",
                "topics": ["keyword1", "keyword2"],
                "reason": "Explanation"
            }
        """
        prompt = self._build_analysis_prompt(repo, files, readme, language)

        # Use UnifiedAIClient - handles fallback automatically
        try:
            result = self.ai.generate_json(
                prompt=prompt,
                system_prompt="You are a GitHub repository optimization expert. Respond with valid JSON only.",
                max_tokens=500,
                min_model_size=32,  # 32B+ for quality analysis
            )

            if result.success and result.json_content:
                if self._is_valid_result(result.json_content):
                    logger.info(f"   Analysis succeeded via {result.model_used}")
                    return result.json_content
                else:
                    logger.warning("   AI returned invalid result format")

        except Exception as e:
            logger.warning(f"   AI analysis failed: {e}")

        # Final fallback - basic strategy
        logger.warning("   Using basic fallback strategy")
        return self._fallback_strategy(repo, language)

    def _build_analysis_prompt(
        self,
        repo: str,
        files: list[str],
        readme: str,
        language: str
    ) -> str:
        """Build analysis prompt aligned with AGENTS.md Dec 2025."""
        file_sample = files[:50] if len(files) > 50 else files
        readme_sample = readme[:3000] if len(readme) > 3000 else readme

        return f"""
<repository_audit>
Name: "{repo}"
Language: "{language}"
File Count: {len(files)}
Files: {file_sample}

<readme_content>
{readme_sample}
</readme_content>
</repository_audit>

**TASK:** Analyze this repository and generate the optimal transformation strategy.

**APEX NAMING CONVENTION (Dec 2025):**
A high-performing name must instantly communicate Product, Function, Platform, and Type.

**Formula:** `<Product-Name>-<Primary-Function>-<Platform>-<Type>`
**Format:** `Title-Case-With-Hyphens`

**Rules:**
1. Length: 3 to 10 words
2. Keywords: MUST include high-volume search terms
3. Forbidden: NO numbers, NO emojis, NO underscores, NO generic words without qualifiers
4. Archival: If archiving, still generate a professional name

**EXAMPLES of excellent names:**
- Wryt-AI-Grammar-And-Writing-Assistant-Browser-Extension
- ChronoLens-Visual-History-Browser-Extension
- FluentPDF-AI-PDF-To-Audio-Web-App
- CogniSearch-AI-Powered-Semantic-Search-Engine
- TaskMaster-Workflow-Automation-Engine-Python-Lib
- CloudOps-Multi-Cloud-Infrastructure-CLI-Tool
- VideoSum-AI-Powered-Video-Summarization-Mobile-App
- StreamPulse-Real-Time-Analytics-Dashboard-React-App

**DESCRIPTION RULES:**
1. MUST be under 300 characters
2. Start with action verb or key feature
3. Include main technology/purpose
4. Be compelling and SEO-friendly

**OUTPUT FORMAT (JSON only):**
{{
  "action": "UPDATE" or "ARCHIVE",
  "new_name": "Professional-Apex-Name-Following-Formula",
  "description": "Concise compelling description under 300 chars",
  "topics": ["keyword1", "keyword2", "keyword3", ...],
  "reason": "Brief explanation of why this name and strategy"
}}
"""

    def _is_valid_result(self, result: dict) -> bool:
        """Validate analysis result."""
        if not isinstance(result, dict):
            return False

        required_keys = ["action", "new_name", "description", "topics"]
        if not all(key in result for key in required_keys):
            return False

        # Validate new_name follows Apex convention
        new_name = result.get("new_name", "")
        if not new_name or len(new_name) < 10:
            return False

        # Check for Title-Case-With-Hyphens format
        if " " in new_name or "_" in new_name:
            return False

        # Description must be under 300 chars
        description = result.get("description", "")
        if not description or len(description) > 300:
            return False

        return True

    def _fallback_strategy(self, repo: str, language: str) -> dict:
        """Generate basic fallback strategy when AI fails."""
        # Generate a basic Apex-style name
        words = repo.replace("-", " ").replace("_", " ").title().split()
        if language:
            words.append(language.title())
        words.append("Project")

        apex_name = "-".join(words)

        return {
            "action": "UPDATE",
            "new_name": apex_name,
            "description": f"Professional {language or 'software'} project with modern architecture",
            "topics": [language.lower()] if language else ["software"],
            "reason": "Fallback strategy - LLM analysis unavailable"
        }