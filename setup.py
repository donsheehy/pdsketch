import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdsketch",
    version="0.0.1",
    author="Donald R. Sheehy and Siddharth Sheth",
    author_email="don.r.sheehy@gmail.com",
    description="A Python package for computing sketches of persistence diagrams.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/donsheehy/pdsketch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['greedypermutation',
                      'metricspaces',
                      'Click',
                     ],
    entry_points='''
        [console_scripts]
        pdsketch=pdsketch.cli:cli
    ''',

)
