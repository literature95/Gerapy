# Automatically created by: gerapy
from setuptools import setup, find_packages
setup(
    name='myproject',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings=myproject.settings']},
    install_requires=[
        'scrapy>=2.0.0',  # 示例依赖
        'other-library>=1.0.0',
    ],
)