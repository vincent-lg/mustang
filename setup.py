import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mustang",
    version="0.1",
    author="Vincent Le Goff",
    author_email="vincent.legoff.srs@gmail.com",
    description="A lightweight, Sqlite ORM in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vincent-lg/mustang/",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires = [],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points = {
        'console_scripts': ['mustang=mustang.commands.main:main'],
    },
)
