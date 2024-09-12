from setuptools import setup, find_packages

setup(
    name="Stream-Processing-Simulator-NTUA-Thesis",
    version="0.1.0",
    packages=find_packages(where="src"),  # Automatically find all packages in 'src'
    package_dir={"": "src"},  # Tell setuptools to look in the 'src' folder for packages
    install_requires=[
        # Add any external dependencies here (e.g., "requests", "pandas")
    ],
    entry_points={
        "console_scripts": [
            # Define CLI commands here if needed
        ],
    },
)
