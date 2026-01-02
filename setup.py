"""Setup configuration for ESHU"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip() 
        for line in requirements_file.read_text().splitlines() 
        if line.strip() and not line.startswith('#')
    ]

setup(
    name="eshu-installer",
    version="0.4.0",
    author="ESHU Team",
    author_email="support@eshu-installer.com",
    description="AI-Driven Universal Package Installer for Linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eshu-apps/eshu-installer",
    project_urls={
        "Bug Tracker": "https://github.com/eshu-apps/eshu-installer/issues",
        "Documentation": "https://github.com/eshu-apps/eshu-installer/blob/main/README.md",
        "Source Code": "https://github.com/eshu-apps/eshu-installer",
        "Upgrade to Premium": "https://eshu-installer.com/upgrade",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Software Distribution",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "eshu=eshu.cli_enhanced:app",
        ],
    },
    include_package_data=True,
    package_data={
        "eshu": ["*.json", "*.yaml"],
    },
    keywords="package-manager linux installer ai llm arch debian ubuntu",
    license="MIT",
)
