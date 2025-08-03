from setuptools import setup, find_packages

# Read the content of the README.md file
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Live_image_data_collection",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=2.2.6",
        "opencv-python>=4.12.0.88",
    ],

    # Metadata for package
    author="Shashwat dev Hans",
    author_email="shashwatdevhans@gmail.com",
    description="A camera live module to collect data for image predictions.",
    download_url="https://github.com/ShashwatDev-26/imageDataCollection.git",
    long_description=long_description,
    long_description_content_type="text/markdown",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # Assuming you will use an MIT license
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha", # Indicate the development status
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    # Python version compatibility
    python_requires=">=3.6",
)
