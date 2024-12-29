from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
import subprocess
import os
import pathlib
import time

def readme():
    with open('README.md') as f:
        return f.read()

def rootcmd(flag):
    return [subprocess.check_output(["root-config", flag]).decode("utf-8").rstrip("\n")]

def rootinc():
    return rootcmd("--incdir")

def rootlib():
    return rootcmd("--libdir")

def numpyinc():
    import numpy
    return [numpy.get_include()]

def usrinc(): 
    dirs = [
        "/usr/local/include/",
        "/opt/homebrew/include"
    ]
    return [d for d in dirs if os.path.exists(d)]

CMAKE_INSTALL = ""

def localinc():
    dirs = [
	'install/include',
	'install/include/eigen3',
    ]
    return [CMAKE_INSTALL + d for d in dirs]

def locallib():
    dirs = [
        "install/lib"
    ]
    return [CMAKE_INSTALL + d for d in dirs]


# From: https://stackoverflow.com/questions/42585210/extending-setuptools-extension-to-use-cmake-in-setup-py
class CMakeExtension(Extension):
    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[])

class build_ext_wcmake(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        cwd = pathlib.Path().absolute()

        # these dirs will be created in build_py, so if you don't have
        # any python sources to bundle, the dirs will be missing
        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = pathlib.Path(self.get_ext_fullpath(ext.name))
        extdir.mkdir(parents=True, exist_ok=True)

        # example of cmake args
        config = 'Debug' if self.debug else 'Release'
        cmake_args = [
            '-DCMAKE_INSTALL_PREFIX=' + str(extdir.parent.absolute()),
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + str(extdir.parent.absolute()),
            '-DCMAKE_BUILD_TYPE=' + config
        ]

        # Tell pybind where we are installing everything
        # global CMAKE_INSTALL
        # CMAKE_INSTALL = str(extdir.parent.absolute()) + "/"

        # example of build args
        build_args = [
            '--config', config,
            '-j', '4'
        ]

        os.chdir(str(build_temp))
        self.spawn(['cmake', str(cwd)] + cmake_args)
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'] + build_args)
            self.spawn(['cmake', '--install', '.'] + build_args)

        # self.announce("SLEEPINGGGG", level=3)
        # time.sleep(100)

        # Troubleshooting: if fail on line above then delete all possible 
        # temporary CMake files including "CMakeCache.txt" in top level dir.
        os.chdir(str(cwd))

ext_modules = [
    Pybind11Extension(
        '_profit',
        ['pylib/profit.cxx'],
        include_dirs=usrinc() + localinc() + rootinc() + numpyinc(),
        library_dirs=locallib() + rootlib(),
        libraries=["Core", "PROfitLib", "tinyxml2", "TreePlayer"],
        language='c++',
        cxx_std=17
    ),

    CMakeExtension('profit/PROfit')
]

setup(
    name='profit',
    ext_modules=ext_modules,
    version='0.1',
    description='Python library for PROfit fitting package.',
    url='https://github.com/gputnam/Elephant_Vanishes/',
    author='Gray Putnam',
    author_email='gputnam@fnal.gov',
    license='MIT',
    packages=['profit'],
    cmdclass={'build_ext': build_ext_wcmake},
    install_requires=[
        'pandas',
        'uproot'
    ],
    zip_safe=False)
