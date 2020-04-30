from setuptools import setup, find_packages

setup(
    name="ideal_spork",
    version="0.1",
    author="zignig",
    description="Boneless v3 , and peripherals",
    packages=find_packages(),
    project_urls={
        "Source Code": "https://github.com/zignig/ideal_spork",
        "Bug Tracker": "https://github.com/zignig/ideal_spork/issues",
    },
    entry_points={
        "console_scripts": [
            "spork = ideal_spork.cli:as_main",
        ]
    }
)
