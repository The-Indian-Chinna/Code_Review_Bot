from setuptools import setup, find_packages

setup(
    name="optimus",
    version="0.0.1",
    description="Bot from the CAM2 Software Engineering Team that helps facilitate code review.",
    author="Cam2",
    packages=find_packages(where="."),  # make the current folder the root src folder
)
