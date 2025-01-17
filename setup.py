from setuptools import find_packages, setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="markdowntoc",
    setup_requires=["setuptools_scm<7"],
    use_scm_version=True,
    description="Autogenerated Table of Contents for Github Markdown or Bear Notes",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/qiaouchicago/markdown-toc",
    author="Qiao Qiao",
    author_email="qiaoq@uchicago.edu",
    license="LICENSE",
    keywords="markdown md github bear table of contents toc",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[],
    extras_require={
        "dev": [
            "pytest~=6.2",
        ]
    },
    scripts=["bin/markdown-toc"],
)
