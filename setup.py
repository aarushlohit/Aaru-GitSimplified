"""
AARU CLI - A Clean & Powerful Git Workflow Engine
Setup configuration
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='aarushlohit_git',
    version='2.0.0',
    description='A Clean & Powerful Git Workflow Engine',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='aarushlohit',
    author_email='aarushlohit@users.noreply.github.com',
    url='https://github.com/aarushlohit/GIT_PROTOCOL',
    packages=['aarush', 'aarush.commands'],
    include_package_data=True,
    install_requires=[
        'typer>=0.9.0',
        'click>=8.0.0',
        'rich>=13.0.0',
    ],
    extras_require={
        'build': ['pyinstaller>=6.0.0'],
        'dev': ['pyinstaller>=6.0.0', 'pytest>=7.0.0'],
    },
    entry_points={
        'console_scripts': [
            'aaru=aarush.aaru_cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control :: Git',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Environment :: Console',
    ],
    python_requires='>=3.8',
    keywords='git workflow cli version-control productivity',
    project_urls={
        'Bug Reports': 'https://github.com/aarushlohit/GIT_PROTOCOL/issues',
        'Source': 'https://github.com/aarushlohit/GIT_PROTOCOL',
        'Zairok App': 'https://zairok.web.app',
        'Documentation': 'https://github.com/aarushlohit/GIT_PROTOCOL/blob/main/README.md',
        'Installation Guide': 'https://github.com/aarushlohit/GIT_PROTOCOL/blob/main/INSTALL.md',
    },
)
