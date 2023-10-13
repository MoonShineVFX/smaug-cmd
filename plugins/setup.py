from PySide6.QtCore import QLibraryInfo
from setuptools import setup, Extension

setup(
    name='MyCustomWidgets',
    version='0.1',
    packages=[''],
    package_dir={'': 'src'},
    ext_modules=[
        Extension(
            'MyCustomWidgets',
            sources=['src/plugin.cpp'],
            include_dirs=[QLibraryInfo.location(QLibraryInfo.LibraryPath.HeadersPath)],
            library_dirs=[QLibraryInfo.location(QLibraryInfo.LibraryPath.LibrariesPath)],
            libraries=['Qt6Core', 'Qt6Gui', 'Qt6Widgets'],
        )
    ],
)