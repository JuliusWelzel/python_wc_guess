from setuptools import setup, find_packages

setup(
    name='womens-world-cup-prediction',
    version='0.1.0',
    author='Julius Welzel',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.3.0',
        'statsmodels>=0.13.0',
        'rapidfuzz>=1.5.1',
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.0',
        ]
    },
    python_requires='>=3.9',
)
