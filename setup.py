from setuptools import setup, find_packages

setup(
    name="hello-world",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "flask>=1.0",
    ],
)
