from setuptools import setup, find_packages

setup(
    name="hello-world",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "flask>=1.0",
        "requests>=2.19.1",
        "Flask-Session>=0.3.1",
        "flask-login>=0.4.1",
        "attr",
    ],
)
