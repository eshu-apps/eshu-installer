"""LLM engine for intelligent package search and installation guidance"""

import json
from typing import List, Dict, Optional, Tuple
from .config import ESHUConfig
from .system_profiler import SystemProfile
from .package_search import PackageResult


class LLMEngine:
    """LLM-powered intelligence for package management"""
    
    def __init__(self, config: ESHUConfig):
        self.config = config
        self.client = None
        self._initialize_client()
        
        # Lazy load optional modules
        self.community_checker = None
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client"""
        if self.config.llm_provider == "anthropic":
            if not self.config.anthropic_api_key:
                raise ValueError("Anthropic API key not configured")
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.config.anthropic_api_key)
        
        elif self.config.llm_provider == "openai":
            if not self.config.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            import openai
            self.client = openai.OpenAI(api_key=self.config.openai_api_key)
        
        elif self.config.llm_provider == "ollama":
            import openai
            self.client = openai.OpenAI(
                base_url=self.config.ollama_endpoint,
                api_key="ollama"  # Ollama doesn't need a real key
            )
    
    def _get_community_checker(self):
        """Lazy load community checker"""
        if self.community_checker is None:
            from .community_checker import CommunityChecker
            self.community_checker = CommunityChecker()
        return self.community_checker
    
    def interpret_query(self, query: str, system_profile: SystemProfile) -> Dict[str, any]:
        """
        Interpret user's natural language query and extract:
        - Package name(s) to search for
        - Preferred package manager (if specified)
        - Installation preferences
        - Any special requirements
        """
        
        system_prompt = f"""You are an expert Linux package manager assistant. The user is running {system_profile.distro} {system_profile.distro_version}.

Available package managers: {', '.join(system_profile.available_managers)}

Your task is to interpret the user's package installation request and return a JSON object with:
- "search_terms": list of package names to search for
- "preferred_manager": preferred package manager if specified (or null)
- "intent": what the user wants to do (install, search, info, etc.)
- "requirements": any special requirements mentioned

Be concise and accurate. Return ONLY valid JSON."""

        user_message = f"User query: {query}"
        
        try:
            if self.config.llm_provider == "anthropic":
                response = self.client.messages.create(
                    model=self.config.model_name,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_message}]
                )
                content = response.content[0].text
            
            elif self.config.llm_provider in ["openai", "ollama"]:
                model = self.config.model_name if self.config.llm_provider == "openai" else self.config.ollama_model
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
                content = response.choices[0].message.content
            
            # Parse JSON response
            # Remove markdown code blocks if present
            content = content.strip()
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1])
            
            return json.loads(content)
        
        except Exception as e:
            print(f"LLM interpretation error: {e}")
            # Fallback: simple parsing
            return {
                "search_terms": [query],
                "preferred_manager": None,
                "intent": "install",
                "requirements": []
            }
    
    def rank_and_recommend(
        self,
        query: str,
        results: List[PackageResult],
        system_profile: SystemProfile,
        check_community: bool = True
    ) -> List[Tuple[PackageResult, str]]:
        """
        Use LLM to intelligently rank results and provide recommendations.
        Returns list of (PackageResult, recommendation_text) tuples.
        """
        
        if not results:
            return []
        
        # Check for community warnings if enabled
        community_warnings = {}
        if check_community:
            checker = self._get_community_checker()
            for i, result in enumerate(results[:15]):
                warnings = checker.check_package(result.name, result.version, result.manager)
                if warnings:
                    community_warnings[i] = warnings
        
        # Prepare results summary for LLM
        results_summary = []
        for i, result in enumerate(results[:15]):  # Limit to top 15
            result_data = {
                "index": i,
                "name": result.name,
                "manager": result.manager,
                "repository": result.repository,
                "version": result.version,
                "description": result.description[:100] if result.description else "",
                "installed": result.installed
            }
            
            # Add community warnings if any
            if i in community_warnings:
                result_data["community_warnings"] = [
                    {
                        "severity": w.severity,
                        "title": w.title,
                        "description": w.description
                    }
                    for w in community_warnings[i]
                ]
            
            results_summary.append(result_data)
        
        # Get hardware info for context
        hardware_info = self._get_community_checker().get_hardware_info()
        
        system_prompt = f"""You are an expert Linux package manager assistant for {system_profile.distro}.

User's hardware: GPU={hardware_info['gpu']}, CPU={hardware_info['cpu']}

The user searched for: "{query}"

Available package managers (in priority order): {', '.join(self.config.package_manager_priority)}

Analyze the search results and provide:
1. Recommended package index (the best match)
2. Brief explanation of why it's the best choice
3. Any warnings or considerations (especially hardware compatibility)

Return JSON with:
{{
  "recommended_index": <index>,
  "explanation": "<brief explanation>",
  "alternatives": [<list of alternative indices>],
  "warnings": ["<any warnings>"]
}}"""

        user_message = f"Search results:\n{json.dumps(results_summary, indent=2)}"
        
        try:
            if self.config.llm_provider == "anthropic":
                response = self.client.messages.create(
                    model=self.config.model_name,
                    max_tokens=1024,
                    temperature=self.config.temperature,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_message}]
                )
                content = response.content[0].text
            
            elif self.config.llm_provider in ["openai", "ollama"]:
                model = self.config.model_name if self.config.llm_provider == "openai" else self.config.ollama_model
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=self.config.temperature,
                    max_tokens=1024
                )
                content = response.choices[0].message.content
            
            # Parse response
            content = content.strip()
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1])
            
            recommendation = json.loads(content)
            
            # Reorder results based on recommendation
            recommended_idx = recommendation.get("recommended_index", 0)
            alternatives = recommendation.get("alternatives", [])
            explanation = recommendation.get("explanation", "")
            warnings = recommendation.get("warnings", [])
            
            # Add community warnings to the explanation
            if recommended_idx in community_warnings:
                for warning in community_warnings[recommended_idx]:
                    if warning.severity == "critical":
                        warnings.insert(0, f"🔴 {warning.title}: {warning.description}")
                    elif warning.severity == "warning":
                        warnings.append(f"⚠️  {warning.title}: {warning.description}")
            
            # Build ordered results with recommendations
            ordered_results = []
            
            # Add recommended package first
            if 0 <= recommended_idx < len(results):
                rec_text = f"✓ RECOMMENDED: {explanation}"
                if warnings:
                    rec_text += f"\n" + "\n".join(warnings)
                ordered_results.append((results[recommended_idx], rec_text))
            
            # Add alternatives
            for alt_idx in alternatives:
                if 0 <= alt_idx < len(results) and alt_idx != recommended_idx:
                    alt_text = "Alternative option"
                    if alt_idx in community_warnings:
                        alt_warnings = [w for w in community_warnings[alt_idx] if w.severity in ["critical", "warning"]]
                        if alt_warnings:
                            alt_text += f"\n⚠️  {alt_warnings[0].title}"
                    ordered_results.append((results[alt_idx], alt_text))
            
            # Add remaining results
            for i, result in enumerate(results):
                if i not in [recommended_idx] + alternatives:
                    ordered_results.append((result, ""))
            
            return ordered_results
        
        except Exception as e:
            print(f"LLM ranking error: {e}")
            # Fallback: return results as-is with empty recommendations
            return [(r, "") for r in results]
    
    def suggest_lightweight_alternative(
        self,
        package_name: str,
        system_profile: SystemProfile
    ) -> Optional[Dict[str, str]]:
        """Suggest lightweight alternative if system has limited resources"""
        
        # Check system resources
        try:
            import psutil
            
            # Get RAM
            ram_gb = psutil.virtual_memory().total / (1024**3)
            
            # If system has less than 4GB RAM, suggest lightweight alternatives
            if ram_gb < 4:
                checker = self._get_community_checker()
                alternatives = checker.suggest_alternatives(package_name, reason="lightweight")
                
                if alternatives:
                    return alternatives[0]  # Return first alternative
        except Exception:
            pass
        
        return None
    
    def generate_install_plan(
        self,
        package: PackageResult,
        system_profile: SystemProfile
    ) -> Dict[str, any]:
        """
        Generate an installation plan for a package, including:
        - Installation commands
        - Dependency handling
        - Build instructions if needed
        - Post-install steps
        """
        
        system_prompt = f"""You are an expert Linux system administrator for {system_profile.distro}.

Generate a detailed installation plan for the following package:
- Name: {package.name}
- Manager: {package.manager}
- Repository: {package.repository}
- Version: {package.version}

Return JSON with:
{{
  "commands": ["<list of commands to execute>"],
  "requires_build": <true/false>,
  "build_system": "<make/cmake/cargo/meson/etc or null>",
  "dependencies": ["<list of dependencies>"],
  "post_install": ["<post-install commands>"],
  "notes": "<any important notes>"
}}"""

        try:
            if self.config.llm_provider == "anthropic":
                response = self.client.messages.create(
                    model=self.config.model_name,
                    max_tokens=2048,
                    temperature=self.config.temperature,
                    system=system_prompt,
                    messages=[{"role": "user", "content": "Generate installation plan"}]
                )
                content = response.content[0].text
            
            elif self.config.llm_provider in ["openai", "ollama"]:
                model = self.config.model_name if self.config.llm_provider == "openai" else self.config.ollama_model
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": "Generate installation plan"}
                    ],
                    temperature=self.config.temperature,
                    max_tokens=2048
                )
                content = response.choices[0].message.content
            
            content = content.strip()
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1])
            
            return json.loads(content)
        
        except Exception as e:
            print(f"Install plan generation error: {e}")
            # Fallback: basic installation plan
            return self._generate_basic_install_plan(package)
    
    def _generate_basic_install_plan(self, package: PackageResult) -> Dict[str, any]:
        """Generate a basic installation plan without LLM"""
        
        commands = []
        requires_build = False
        build_system = None
        
        if package.manager == "pacman":
            commands = [f"sudo pacman -S {package.name}"]
        elif package.manager in ["yay", "paru"]:
            commands = [f"{package.manager} -S {package.name}"]
            requires_build = True
        elif package.manager == "apt":
            commands = [f"sudo apt install {package.name}"]
        elif package.manager == "flatpak":
            commands = [f"flatpak install {package.name}"]
        elif package.manager == "snap":
            commands = [f"sudo snap install {package.name}"]
        elif package.manager == "cargo":
            commands = [f"cargo install {package.name}"]
            requires_build = True
            build_system = "cargo"
        elif package.manager == "npm":
            commands = [f"npm install -g {package.name}"]
        elif package.manager == "pip":
            commands = [f"pip install --user {package.name}"]
        
        return {
            "commands": commands,
            "requires_build": requires_build,
            "build_system": build_system,
            "dependencies": [],
            "post_install": [],
            "notes": f"Standard installation for {package.manager}"
        }
    
    def handle_error(
        self,
        error_output: str,
        package: PackageResult,
        system_profile: SystemProfile
    ) -> Dict[str, any]:
        """
        Analyze installation error and suggest fixes
        """
        
        system_prompt = f"""You are an expert Linux troubleshooter for {system_profile.distro}.

An error occurred while installing {package.name} via {package.manager}.

Analyze the error and provide:
{{
  "error_type": "<dependency/permission/build/network/etc>",
  "diagnosis": "<brief explanation>",
  "solutions": ["<list of potential solutions>"],
  "commands": ["<commands to try>"]
}}"""

        user_message = f"Error output:\n{error_output[:2000]}"  # Limit error output
        
        try:
            if self.config.llm_provider == "anthropic":
                response = self.client.messages.create(
                    model=self.config.model_name,
                    max_tokens=1024,
                    temperature=self.config.temperature,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_message}]
                )
                content = response.content[0].text
            
            elif self.config.llm_provider in ["openai", "ollama"]:
                model = self.config.model_name if self.config.llm_provider == "openai" else self.config.ollama_model
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=self.config.temperature,
                    max_tokens=1024
                )
                content = response.choices[0].message.content
            
            content = content.strip()
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1])
            
            return json.loads(content)
        
        except Exception as e:
            print(f"Error analysis failed: {e}")
            return {
                "error_type": "unknown",
                "diagnosis": "Unable to analyze error",
                "solutions": ["Check the error output manually"],
                "commands": []
            }
