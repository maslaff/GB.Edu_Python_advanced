import os
from random import randint, choice, choices
from string import ascii_letters as letters, digits, printable
from shutil import rmtree


class InvalidValueError(Exception):
    """Custom exception"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = args[0]

    def __str__(self) -> str:
        return self.msg


class Count:
    """Custom descriptor"""

    def __init__(self, vmin: int = 0, vmax: int = 30):
        self.vmax = vmax
        self.vmin = vmin

    def __set_name__(self, owner, pname):
        self.param_name = "_" + pname

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.param_name, value)

    def __delete__(self, instance):
        raise AttributeError(f'Свойство "{self.param_name}" нельзя удалять')

    def validate(self, value):
        if not isinstance(value, int) or not self.vmin < value <= self.vmax:
            raise InvalidValueError(
                f"Invalid value: {value}. Value should be a positive integer."
            )


class Fishdir:
    """Class creating fish directory/file structure
    with random or given deep level and other parameters

            Args:
            destination (str, optional): _description_. Defaults to None.
            dirname (str, optional): _description_. Defaults to None.

        Parameters setting up by method configuration
        or by assigning values directly to attributes

    Class atributes:
        random_dir_count (int, optional): Randomize count dir per deep level. Defaults to True.
        random_file_count (int, optional): Randomize count file per deep level. Defaults to True.
        min_file_count (int, optional): Min files count for randomizer. Defaults to 1.
        max_file_count (int, optional): Max files count for randomizer. Defaults to 8.
        min_dir_count (int, optional): Min dirs count for randomizer. Defaults to 1.
        max_dir_count (int, optional): Max dirs count for randomizer. Defaults to 5.
        file_count (int, optional): Static files count for creating (Without randomize). Defaults to 5.
        dir_count (int, optional): Static dir count for creating (Without randomize). Defaults to 5.
        file_prefix (str, optional): Prefix for creating files. Defaults to "file_".
        folder_prefix (str, optional): Prefix for creating folders. Defaults to "dir_".
        deep (int, optional): Deep of folder structure. Defaults to 3.
        exts (list[str], optional): File extensions for creating files. Defaults to ["txt", "tmp", "md", "log"].
    """

    directory: str
    random_dir_count: int = True
    random_file_count: int = True
    min_file_count: int = Count()
    max_file_count: int = Count()
    min_dir_count: int = Count()
    max_dir_count: int = Count()
    file_count: int = Count()
    dir_count: int = Count()
    file_prefix: str
    folder_prefix: str
    deep: int = Count()
    exts: list[str] = []

    def __init__(self, destination: str = None, dirname: str = None):
        """Class creating fish directory/file structure with random or given deep level and other parameters

        Args:
            destination (str, optional): _description_. Defaults to None.
            dirname (str, optional): _description_. Defaults to None.
        """
        self.directory = self.__validate_init(destination, dirname)
        self.configuration()
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)

    # ################################
    def __validate_init(
        self, destination, dirname, default_dirname: str = "test_folder"
    ):
        if dirname:
            if not isinstance(dirname, str):
                raise TypeError("dirname can only be string")
            if os.path.isabs(dirname):
                raise ValueError("dirname can only be foldername string, not path")

        if destination:
            if not isinstance(destination, str):
                raise TypeError("destination can only be string")
            if dirname:
                if not os.path.isabs(destination):
                    raise ValueError(
                        "if dirname is given, destination can only be abspath or None"
                    )
                return os.path.join(destination, dirname)
            if os.path.isabs(destination):
                return os.path.join(destination, default_dirname)
            return os.path.abspath(destination)
        if dirname:
            return os.path.abspath(dirname)
        return os.path.abspath(default_dirname)

    # ################################
    def __validate_init2(
        self, destination, dirname, default_dirname: str = "test_folder"
    ):
        if destination:
            if not isinstance(destination, str):
                raise TypeError("destination can only be string")

        if dirname:
            if not isinstance(dirname, str):
                raise TypeError("dirname can only be string")
            if os.path.isabs(dirname):
                raise ValueError("dirname can only be foldername string, not path")
            if destination:
                if not os.path.isabs(destination):
                    raise ValueError(
                        "if dirname is given, destination can only be abspath or None"
                    )
                return os.path.join(destination, dirname)
            return os.path.abspath(dirname)
        if destination:
            if os.path.isabs(destination):
                return os.path.join(destination, default_dirname)
            return os.path.abspath(destination)
        return os.path.abspath(default_dirname)

    def configuration(
        self,
        random_dir_count: int = True,
        random_file_count: int = True,
        min_file_count: int = 1,
        max_file_count: int = 8,
        min_dir_count: int = 1,
        max_dir_count: int = 5,
        file_count: int = 5,
        dir_count: int = 5,
        file_prefix: str = "file_",
        folder_prefix: str = "dir_",
        deep: int = 3,
        exts: list[str] = ["txt", "tmp", "md", "log"],
    ):
        """Configurate class parameters

        Args:
            random_dir_count (int, optional): Randomize count dir per deep level. Defaults to True.
            random_file_count (int, optional): Randomize count file per deep level. Defaults to True.
            min_file_count (int, optional): Min files count for randomizer. Defaults to 1.
            max_file_count (int, optional): Max files count for randomizer. Defaults to 8.
            min_dir_count (int, optional): Min dirs count for randomizer. Defaults to 1.
            max_dir_count (int, optional): Max dirs count for randomizer. Defaults to 5.
            file_count (int, optional): Static files count for creating (Without randomize). Defaults to 5.
            dir_count (int, optional): Static dir count for creating (Without randomize). Defaults to 5.
            file_prefix (str, optional): Prefix for creating files. Defaults to "file_".
            folder_prefix (str, optional): Prefix for creating folders. Defaults to "dir_".
            deep (int, optional): Deep of folder structure. Defaults to 3.
            exts (list[str], optional): File extensions for creating files. Defaults to ["txt", "tmp", "md", "log"].
        """
        self.random_dir_count = random_dir_count
        self.random_file_count = random_file_count
        self.min_file_count = min_file_count
        self.max_file_count = max_file_count
        self.min_dir_count = min_dir_count
        self.max_dir_count = max_dir_count
        self.file_count = file_count
        self.dir_count = dir_count
        self.file_prefix = file_prefix
        self.folder_prefix = folder_prefix
        self.deep = deep
        self.exts = exts

    def __randname(self):
        return "".join(choices(letters + digits, k=randint(2, 4)))

    def create_fish_folders(self, direc: str):
        """Created fish folders (one level, without files)

        Args:
            direc (str): Destination directory

        Returns:
            list: List created directories
        """
        drs = [
            f"{self.folder_prefix}{self.__randname()}"
            for _ in range(
                randint(self.min_dir_count, self.max_dir_count)
                if self.random_dir_count
                else self.dir_count
            )
        ]
        for d in drs:
            os.mkdir(os.path.join(direc, d))
        return drs

    def create_fish_files(self, direc: str):
        """Created fish files with content in directory

        Args:
            direc (str): Destination directory
        """
        for n in range(
            randint(self.min_file_count, self.max_file_count)
            if self.random_file_count
            else self.file_count
        ):
            with open(
                os.path.join(
                    # direc if direc else os.getcwd(),
                    direc,
                    f"{self.file_prefix}{self.__randname()}{n}.{choice(self.exts)}",
                ),
                "w",
                encoding="utf-8",
            ) as f:
                f.write("".join(choices(printable, k=randint(2, 150))))

    def __create_test_folder(self, cdir, deep, level):
        # print(f"{level}\t{dir}")
        self.create_fish_files(cdir)
        if level == deep:
            return
        for direc in self.create_fish_folders(cdir):
            self.__create_test_folder(os.path.join(cdir, direc), deep, level + 1)

    def create_test_folder(self):
        """Creating fish folder structure, with a given, in a class, parameters"""
        self.__create_test_folder(self.directory, self.deep, 0)

    def remove_test_folder(self):
        """Remove fish folder structure"""
        rmtree(self.directory)

    def __enter__(self):
        self.create_test_folder()
        return self.directory

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remove_test_folder()

    def __repr__(self):
        return f"Fishdir({self.directory})"

    def __str__(self):
        return (
            f"random_dir_count = {self.random_dir_count}\n"
            f"random_file_count = {self.random_file_count}\n"
            f"min_file_count = {self.min_file_count}\n"
            f"max_file_count = {self.max_file_count}\n"
            f"min_dir_count = {self.min_dir_count}\n"
            f"max_dir_count = {self.max_dir_count}\n"
            f"file_count = {self.file_count}\n"
            f"dir_count = {self.dir_count}\n"
            f"file_prefix = {self.file_prefix}\n"
            f"folder_prefix = {self.folder_prefix}\n"
            f"deep = {self.deep}\n"
            f"exts = {self.exts}\n"
        )


def __main():
    fsh = Fishdir("test_fld_1")
    fsh.create_test_folder()


if __name__ == "__main__":
    __main()
