from setuptools import setup, find_packages

setup(
    name='pyqte',
    version='0.1.0',
    author='Daniel de Abreu Pereira Uhr',
    author_email='daniel.uhr@gmail.com',
    description='A Python package for estimating Quantile Treatment Effects (QTE) and related estimators for causal inference.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/pyqte',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'statsmodels',
        'matplotlib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
)