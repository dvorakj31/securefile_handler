Secure File Handler
===================

This module provides secure removing files and folders with content.

Module was created as school project for MI-PYT class at FIT CTU.


Task description
----------------

See file https://github.com/dvorakj31/securefile_handler/blob/master/TASK.rst


Documentation
=============

https://securefile-handler.readthedocs.io/en/latest/index.html


Installation
============

This module works on Python 3.6+.

Unix-like system users
----------------------

1.  Ensure you have installed c compiler on your device

2.  Ensure you have installed python version >= 3.6

3.  You can install this module manually via github:

    - Click on clone or download on this page and download ZIP

    - Dowload this repository on your drive

    - Unzip downloaded file

    - Run command-line and change directory to unzipped directory

    - Run ``python setup.py install``

4.  Another way is installing this module via pip.

    - Run command-line

    - Run command ``python -m pip install securefile-handler``

Windows system users
--------------------

1.  Ensure you have correctly set and installed C Windows Compiler (you can follow https://wiki.python.org/moin/WindowsCompilers)

2.  Ensure you have installed python version >= 3.6

3.  You can install this module manually via github:

    - Click on clone or download on this page and download ZIP

    - Dowload this repository on your drive

    - Unzip downloaded file

    - Run command-line and change directory to unzipped directory

    - Run ``py -3 setup.py install``

4.  Another way is installing this module via pip.

    - Run command-line

    - Run command ``py -3 -m pip install securefile-handler``


Examples
========

Example of shredding file::

    import securefile_handler
    securefile_handler.shred('/path/to/file')
    securefile_handler.shred(Path('/path/to/another/file'))
    securefile_handler.shred('/path/to/device')

You can change shred function arguments or whole erase function::

    import securefile_handler
    securefile_handler.shred('/path/to/file',
     erase_function=lambda path: securefile_handler.erase_helpers.shred(path, chunk_size=1024 * 2))
    securefile_handler.shred('/path/to/file', erase_function=my_better_function)

Module can securely remove files using shred function::

    import securefile_handler
    securefile_handler.remove_file('/path/to/file')
    securefile_handler.remove_file('/symlink/is/destroyed/with/file/that/points/to')

There is possibility of removing non-empty directory trees aswell::

    import securefile_handler
    securefile_handler.remove_dirtree('/path/to/dirtree')
    securefile_handler.remove_dirtree('/symlinks/in/dir/are/only/removed')

Moving files or directories is possible only between different devices::

    import securefile_handler
    securefile_handler.move_file('/file/on/disk1', '/destination/on/disk2')
    securefile_handler.move_folder('/folder/on/disk1', '/destination_folder/on/disk2')

