from setuptools import setup, find_packages

setup(
    name="pinelands-wildfire-app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.68.0',
        'uvicorn>=0.15.0',
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'geopandas>=0.9.0',
        'shapely>=1.7.0',
        'rasterio>=1.2.0',
        'scikit-learn>=0.24.0',
        'torch>=1.9.0',
        'requests>=2.26.0',
        'python-dotenv>=0.19.0',
        'pytest>=6.2.0',
        'httpx>=0.18.0',
        'fiona>=1.8.0',
    ],
    python_requires='>=3.8',
)
