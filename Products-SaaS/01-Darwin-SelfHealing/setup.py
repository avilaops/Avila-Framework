"""
Setup configuration for Darwin Self-Healing Library
"""

from setuptools import setup, find_packages
import pathlib

# Read README
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="darwin-healing",
    version="1.0.0",
    description="Self-healing Python library that learns from errors and auto-fixes them",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/avila/darwin",
    author="Nicolas Ávila",
    author_email="nicolas@avila.inc",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="self-healing automation error-handling devops reliability",
    packages=find_packages(exclude=["tests", "docs"]),
    python_requires=">=3.8",
    install_requires=[
        "psutil>=5.9.0",  # Para detectar portas/processos
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "pro": [
            "slack-sdk>=3.19.0",
            "discord-py>=2.1.0",
            "boto3>=1.26.0",  # AWS integrations
            "azure-mgmt>=4.0.0",  # Azure integrations
        ],
    },
    entry_points={
        "console_scripts": [
            "darwin=darwin.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/avila/darwin/issues",
        "Documentation": "https://docs.darwin-healing.com",
        "Source": "https://github.com/avila/darwin",
        "Discord": "https://discord.gg/darwin",
    },
)
