data = [
    (
        '[![Build Status](https://app.travis-ci.com/NCI-GDC/plaster.svg?token=5s3bZRahNJnkspYEMwZC&branch=master)](https://app.travis-ci.com/NCI-GDC/plaster)\n\n# The Data Commons Model Source Generator Project (Plaster)\n\nGDC internship project for generating data model source code.\n\n<!-- toc -->\n<!-- tocstop -->\n\n# Purpose\n\nThis project is a drop-in replacement to the project\nhttps://github.com/NCI-GDC/gdcdatamodel, without challenges and obscurity associated\nwith using gdcdatamodel. The resulting code will be readable, pass static and linting\nchecks, completely remove delays from dictionary load times.\n\n# Goal\n\nGiven any compliant gdcdictionary, generate source code that can replace the\ngdcdatamodel runtime generated code.\n\n# Data Commons Models\n\nThe data commons are a collection of data structures representing concepts within a\nsubject area. These data structures usually form a graph with edges as relationships to\none another. The data structures and relationships are defined as JSON schema in yaml\nfiles that are distributed via a git repository. These definitions are called\nDictionaries for short. The gdcdictionary is one example of a data commons with a\nprimarily focus on cancer. Dictionaries are updated and released frequently, with each\nrelease adding or removing nodes, edges, or properties.\n\nThese data structures are converted to Python source code at runtime by the gdcdatamodel\nproject. For example, the case yaml file will autogenerate the models.Case Python class\nwith properties and methods matching those defined in the yaml file. The generated\nsource codes are sqlalchemy database entities that map to tables in the database.\n\nThe psqlgraph project makes querying using these entities more uniform across different\nuse cases, by exposing common modules, classes and functions that are useful for\nmanipulating data stored using sqlalchemy.\n\n## Problems:\n\n- Runtime generated code cannot be peer reviewed or inspected. This forces developers to\n  switch between dictionary definitions and code to understand what a particular piece\n  of code is doing. Most projects within the center have this problem since they all\n  rely on gdcdatamodel for the database entities.\n- Runtime generated code also means no type checking, linting and little chance of\n  running static analysis tools like flake8\n- Runtime model code generation takes a few seconds (might be a few minutes - Qiao) to\n  complete. This means that any project that makes use of gdcdatamodel must pay for this\n  in one way or another. The most common is usually start up time.\n\nIn summary, most projects within the center suffer just because they rely on\ngdcdatamodel for database entities. The major goal of this project is to eliminate the\nruntime code generation feature on gdcdatamodel, thereby eliminating the above-mentioned\nproblems.\n\n# Project Details\n\n## Requirements\n\n- Python >= 3.8\n- No direct dependency on any dictionary versions\n- Must expose scripts that can be invoked to generate source code\n- Must include unit and integration tests with over 80% code coverage\n- Must provide typings and pass mypy checks\n\n## Features\n\n- Dictionary selection and loading\n- Template management\n- Code generation\n- Scripts\n\n## Dictionary selection and loading\n\nThis module will be responsible for loading a dictionary given necessary parameters.\nThese parameters will include:\n\n- A git URL\n- A target version, tag, commit or branch name\n- A label used for referencing the dictionary later\n\n## Template Management\n\nThis module will be responsible for the templates used to generate the final source code\n\n# How to use\n\n## Install plaster\n\n```bash\npip install .\n```\n\n## Generate gdcdictionary\n\n```bash\nplaster generate -p gdcdictionary -o "example/gdcdictionary"\n```\n\n## Generate biodictionary\n\n```bash\nplaster generate -p biodictionary -o "example/biodictionary"\n```\n\n# Associated Projects\n\n- biodictionary: https://github.com/NCI-GDC/biodictionary\n- gdcdatamodel: https://github.com/gdcdatamodel\n- gdcdictionary: https://github.com/NCI-GDC/gdcdictionary\n- psqlgml: https://github.com/NCI-GDC/psqlgml\n- psqlgraph: https://github.com/NCI-GDC/psqlgraph\n\n# Repo Visualizer\n\n![Visualization of this repo](images/diagram.svg)\n',
        [
            "# Table of Contents",
            "",
            "- [Purpose](#Purpose)",
            "- [Goal](#Goal)",
            "- [Data Commons Models](#Data-Commons-Models)",
            "  - [Problems:](#Problems:)",
            "- [Project Details](#Project-Details)",
            "  - [Requirements](#Requirements)",
            "  - [Features](#Features)",
            "  - [Dictionary selection and loading](#Dictionary-selection-and-loading)",
            "  - [Template Management](#Template-Management)",
            "- [How to use](#How-to-use)",
            "  - [Install plaster](#Install-plaster)",
            "  - [Generate gdcdictionary](#Generate-gdcdictionary)",
            "  - [Generate biodictionary](#Generate-biodictionary)",
            "- [Associated Projects](#Associated-Projects)",
            "- [Repo Visualizer](#Repo-Visualizer)",
        ],
    )
]