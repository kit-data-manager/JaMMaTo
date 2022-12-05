'''from Cython.Build import cythonize
from setuptools import Extension
from setuptools import setup

CYTHON_EXTENSIONS = [
    Extension(
        name="Cython.cython_fillObject",
        sources=["Cython/cython_fillObject.pyx"]
    )
]

EXT_MODULES = cythonize(CYTHON_EXTENSIONS)

with open("requirements.txt") as fp:
    install_requires = fp.read().strip().split("\n")

metadata = dict(
    install_requires=install_requires,
    ext_modules=EXT_MODULES,
)


def setup_package() -> None:
    setup(**metadata)


if __name__ == "__main__":
    setup_package()'''
