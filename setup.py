from setuptools import setup, find_packages
setup(
    name="intutils",
    version="0.1",
    packages=find_packages('src'),
    author="Max Sikström",
    author_email="max@pengi.se",
    description="A toolchain for Advent of Code 2019 intcode",

    package_dir={'': 'src'},

    entry_points={
        'console_scripts': [
            'intcode-asm = intutils.exec.asm.main:main',
            'intcode-ld = intutils.exec.ld.main:main',
            'intcode-objcopy = intutils.exec.objcopy.main:main'
        ]
    },

    install_requires=[
        'argparse>=1.4'
    ],

    extras_require={
        'dev': [
            "pytest>=5.3"
        ]
    },
)
