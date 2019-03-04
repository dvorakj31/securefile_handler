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

