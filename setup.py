from setuptools import setup

setup(
    name="renogymodbus",
    version="0.0.8",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rosswarren/renogymodbus",
    author="Ross Warren",
    author_email="rosswarren4@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["renogymodbus"],
    include_package_data=True,
    install_requires=["minimalmodbus", "retrying"],
    test_suite="test",
    entry_points={
        "console_scripts": [
            "renogymodbus = renogymodbus.command_line:main",
        ],
    },
)
