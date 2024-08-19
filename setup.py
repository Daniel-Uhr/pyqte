from setuptools import setup, find_packages

setup(
    name="pyqte",
    version="1.0.0",
    author="Daniel de Abreu Pereira Uhr",
    author_email="daniel.uhr@gmail.com",
    description="A Python package for estimating Quantile Treatment Effects (QTE) using R's qte package via rpy2.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Daniel-Uhr/pyqte",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
        "statsmodels",
        "rpy2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
