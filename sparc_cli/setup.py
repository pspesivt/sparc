from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='sparc',
    version='0.87.6',  # Updated for improved math evaluation
    packages=find_packages(),
    install_requires=[
        'twine',
        'setuptools',
        'wheel',
        'flake8',
        'black',
        'pytest',
        'pip-upgrader',
        'httpx',
        'beautifulsoup4',
        'pypandoc',
        'playwright>=1.39.0',
        'langchain>=0.1.0',
        'langchain-anthropic>=0.3.1',
        'langchain-openai>=0.3.3',
        'langchain-aws>=0.2.12',  # Required for AWS Bedrock support
        'langgraph>=0.2.60',
        'langgraph-checkpoint>=2.0.9',
        'langgraph-sdk>=0.1.48',
        'langchain-core>=0.3.28',
        'rich>=13.0.0',
        'GitPython>=3.1',
        'fuzzywuzzy==0.18.0',
        'python-Levenshtein==0.23.0',
        'pathspec>=0.11.0',
        'aider-chat>=0.69.1',
        'ripgrepy>=0.1.0',
        'boto3>=1.36.13',
        'botocore>=1.36.13',
        'numpy',
        'sympy'  # Required for symbolic math
    ],
    author='rUv',
    author_email='ruv@ruv.net',
    description='SPARC CLI is a powerful command-line interface that implements the SPARC Framework methodology for AI-assisted software development. Combining autonomous research capabilities with guided implementation, it provides a comprehensive toolkit for analyzing codebases, planning changes, and executing development tasks with advanced AI assistance.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ruvnet/sparc',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [
            'sparc=sparc_cli.__main__:main',
        ],
    },
)
