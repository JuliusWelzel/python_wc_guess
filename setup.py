from setuptools import setup, find_packages

setup(
    name='womens-world-cup-prediction',
    version='0.1.0',
    author='Julius Welzel',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.6'
        'pandas>=1.3.0',
        'scikit-learn>=1.2.2'
        'statsmodels>=0.13.0',
        'rapidfuzz>=1.5.1',
        'scikit-learn>=1.3',
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.0',
        ]
    },
    python_requires='>=3.9',
)
