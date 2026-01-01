"""GitHub repository search for finding packages"""

import requests
from typing import List, Optional
from dataclasses import dataclass
from .package_search import PackageResult


@dataclass
class GitHubRepo:
    """Represents a GitHub repository"""
    name: str
    full_name: str
    description: str
    stars: int
    language: str
    clone_url: str
    homepage: str
    topics: List[str]


class GitHubSearcher:
    """Search GitHub for relevant package repositories"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ESHU/0.3.0',
            'Accept': 'application/vnd.github.v3+json'
        })
        self.api_base = "https://api.github.com"

    def search_repos(self, query: str, max_results: int = 5) -> List[PackageResult]:
        """
        Search GitHub for repositories matching the query

        Focuses on:
        - High star count (quality indicator)
        - Active maintenance (recent activity)
        - Clear installation instructions
        - Relevant topics/tags
        """

        try:
            # Build search query with quality filters
            search_query = f"{query} stars:>50"  # At least 50 stars for quality

            params = {
                'q': search_query,
                'sort': 'stars',
                'order': 'desc',
                'per_page': max_results
            }

            response = self.session.get(
                f"{self.api_base}/search/repositories",
                params=params,
                timeout=5
            )

            if response.status_code != 200:
                return []

            data = response.json()
            results = []

            for item in data.get('items', []):
                # Skip forks - focus on original repos
                if item.get('fork', False):
                    continue

                # Check if it's actually installable (has releases or clear build instructions)
                if self._is_installable(item):
                    result = self._convert_to_package_result(item)
                    if result:
                        results.append(result)

            return results

        except Exception as e:
            # Silently fail - GitHub search is optional
            return []

    def _is_installable(self, repo_data: dict) -> bool:
        """Check if repository is likely installable"""

        # Check for common installable indicators
        topics = repo_data.get('topics', [])
        language = repo_data.get('language', '').lower()

        # Common installable languages/frameworks
        installable_languages = ['python', 'rust', 'go', 'c', 'c++', 'javascript', 'typescript']
        installable_topics = ['cli', 'tool', 'utility', 'application', 'package', 'installer']

        # Must have decent stars (already filtered, but double-check)
        if repo_data.get('stargazers_count', 0) < 30:
            return False

        # Check language
        if language and language in installable_languages:
            return True

        # Check topics
        if any(topic in installable_topics for topic in topics):
            return True

        return False

    def _convert_to_package_result(self, repo_data: dict) -> Optional[PackageResult]:
        """Convert GitHub repo data to PackageResult"""

        try:
            # Determine likely installation method based on language
            language = repo_data.get('language', '').lower()
            manager = self._guess_package_manager(language, repo_data)

            # Build description with metadata
            desc = repo_data.get('description', 'No description')
            stars = repo_data.get('stargazers_count', 0)
            desc_with_meta = f"{desc} ⭐ {stars}"

            return PackageResult(
                name=repo_data['name'],
                version=f"git:{repo_data.get('default_branch', 'main')}",
                manager=manager,
                repository=f"github:{repo_data['full_name']}",
                description=desc_with_meta,
                installed=False,
                score=0.0,
                size_mb=0.0,
                os_optimized="universal"
            )

        except Exception:
            return None

    def _guess_package_manager(self, language: str, repo_data: dict) -> str:
        """Guess best installation method based on language"""

        # Check for package manager files in repo
        # This would require additional API calls, so we'll use heuristics

        language_to_manager = {
            'python': 'pip',
            'rust': 'cargo',
            'javascript': 'npm',
            'typescript': 'npm',
            'go': 'go-get',
            'ruby': 'gem',
        }

        # Default to git/build
        return language_to_manager.get(language, 'git')


def search_github_packages(query: str, max_results: int = 5) -> List[PackageResult]:
    """
    Convenience function to search GitHub for packages

    Args:
        query: Search query
        max_results: Maximum number of results to return

    Returns:
        List of PackageResult objects from GitHub
    """
    searcher = GitHubSearcher()
    return searcher.search_repos(query, max_results)
