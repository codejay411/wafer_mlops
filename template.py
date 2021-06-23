import os

dirs = [
    "data",
    "notebooks",
    "src"
]

for dir_ in dirs:
    os.makedirs(dir_, exist_ok=True)
    with open(os.path.join(dir_, ".gitkeep"), "w") as f:
        pass

file_= [
    "dvc.yaml",
    ".gitignore",
    os.path.join("src","__init__.py"),
    "README.md"
]

for file in file_:
    with open(file, "w") as f:
        pass