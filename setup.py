from setuptools import setup, find_packages
setup(
    name="intcodeutils",
    version="0.1",
    packages=find_packages('src'),
    author="Max Sikström",
    author_email="max@pengi.se",
    description="A toolchain for Advent of Code 2019 intcode",

    package_dir={'': 'src'},

    entry_points={
        'console_scripts': [
            'intcode-asm = intcodeutils.exec.asm.main:main',
            'intcode-ld = intcodeutils.exec.ld.main:main',
            'intcode-objcopy = intcodeutils.exec.objcopy.main:main'
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
