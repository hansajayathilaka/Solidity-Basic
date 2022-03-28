import os
import shutil
from distutils.dir_util import copy_tree


def delete_build_folder():
    shutil.rmtree('./build')


def copy_build_folder():
    copy_tree("../build/", "./build")


def main():
    delete_build_folder()
    copy_build_folder()


if __name__ == '__main__':
    main()
