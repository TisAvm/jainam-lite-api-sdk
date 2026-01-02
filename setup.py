from setuptools import setup, find_packages

NAME = "jainam-api-client"
VERSION = "1.0.0"

REQUIRES = [
    'requests>=2.28.0',
    'websocket-client>=1.4.0',
    'pandas>=1.5.0',
]

setup(
    name=NAME,
    version=VERSION,
    description="Jainam Lite Trading API Python SDK",
    author="Aviral Anand Mishra",
    author_email="mishraaviralanand@gmail.com",
    url="",
    keywords=["Jainam", "Trading API", "Stock Trading"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests", "inspiration"]),
    include_package_data=True,
    python_requires=">=3.8",
    long_description="""
    Jainam Lite API Python SDK - A lightweight Python wrapper for the Jainam Securities Trading API.
    Supports order management, portfolio tracking, funds/limits, and real-time market data via WebSocket.
    """
)
