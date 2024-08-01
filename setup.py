from setuptools import setup, find_packages

setup(
    name="quickfix_trading_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "quickfix",
    ],
    extras_require={
        "dev": [
            "pytest",
            "python-dotenv",
        ]
    },
    entry_points={
        "console_scripts": [
            "start-trading-app=quickfix_trading_app.main:main",
        ],
    },
)
