
from setuptools import setup

with open("requirements.txt") as fp:
    install_requires = fp.read().strip().split("\n")

metadata = dict(
    install_requires=install_requires,
)

def setup_package() -> None:
    setup(**metadata)

if __name__ == "__main__":
    setup_package()
