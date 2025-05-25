from setuptools import setup, find_packages

setup(
    name="zero_food_bot",
    version="0.1",
    packages=find_packages(),
    extras_require={
        'dev': [
            'pytest>=7.0',
            'pytest-cov>=4.0',
        ],
    }
)