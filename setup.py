from setuptools import setup, find_packages

setup(
    name="income-tax-calculator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.31.1",
        "pandas>=2.2.0",
    ],
) 