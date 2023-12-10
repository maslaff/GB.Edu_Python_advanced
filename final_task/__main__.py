from pkg.Fishdir import Fishdir
import Dir


def example_with(direc):
    """Example show as fish-directory structure created by context manager

    Context manager create fish folder structure in test_folder,
    inside him running travers_directory, result printing by specified form.
    After completion, context manager removing test_folder.
    """
    with Fishdir(direc) as testdir:
        Dir.print_list(Dir.traverse_directory(testdir))


def example_fish_settings(direc):
    """Example show as fish-directory structure setting and created by instance init"""
    # Create instance
    fdir = Fishdir(direc)

    # This action will raise an exception
    # fdir.file_count = -3

    # Configure some parameters with configuration method
    fdir.configuration(dir_count=4, file_count=6)

    # Configure parameter individually by direct assignment to an attribute
    fdir.max_file_count = 7

    # Direct remove ext from exts list
    fdir.exts.remove("tmp")

    # Direct add ext to exts list
    fdir.exts.append("res")

    # Call __str__ dander
    print(fdir)

    # Creation procedure fish file/folder structure
    fdir.create_test_folder()

    # Remove a created test folder
    fdir.remove_test_folder()


if __name__ == "__main__":
    # Given dirname from console args and initialize logger
    directory = Dir.init()

    # Simply traverse test by call from comandline
    dirlist = Dir.traverse_directory(directory)
    Dir.print_list(dirlist)

    # Test Fishdir module with context manager
    # example_with(directory)

    # Test Fishdir module with settings up
    # example_fish_settings(directory)
