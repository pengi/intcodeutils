from setuptools import setup, find_packages
setup(
    name="inttools",
    version="0.1",
    packages=find_packages(),
    author="Max Sikström",
    author_email="max@pengi.se",
    description="A toolchain for Advent of Code 2019 intcode",
    
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'intcode-ld = exec.ld.main:main',
            'intcode-objcopy = exec.objcopy.main:main'
        ]
    },
    
    install_requires=[
        "pyyaml>=5.3"
    ],
)