import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fw_ddsm",
    version="0.2.25",
    author="Shan Dora He",
    author_email="dora.shan.he@gmail.com",
    description="Frank-Wolfe-based distributed demand scheduling method package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dorahee/FW-DDSM.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)