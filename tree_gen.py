import sys

import pyperclip
from pathlib import Path


class TreeGenerator:
    space: str = '    '
    branch: str = '│   '
    tee: str = '├── '
    last: str = '└── '

    def __init__(self, exclude_extensions: list[str] = None, exclude_folders: list[str] = None) -> None:
        self.exclude_extensions: list[str] = exclude_extensions
        self.exclude_folders: list[str] = exclude_folders

    def filter(self, contents) -> list[Path]:
        result: list[Path] = []
        for content in contents:
            name: str = str(content.name)
            exclude: bool = False
            if self.exclude_folders is not None:
                for folder in self.exclude_folders:
                    if name.startswith(folder):
                        exclude = True
                        break
            if not exclude and self.exclude_extensions is not None:
                for extension in self.exclude_extensions:
                    if name.endswith(extension):
                        exclude = True
                        break

            if not exclude:
                result.append(content)

        return result

    def generate(self, path: Path, prefix: str = ''):
        contents: list[Path] = list(path.iterdir())
        contents = self.filter(contents)
        pointers: list[str] = [self.tee] * (len(contents) - 1) + [self.last]
        for pointer, path in zip(pointers, contents):
            yield prefix + pointer + path.name
            if path.is_dir():
                extension: str = self.branch if pointer == self.tee else self.space
                yield from self.generate(path, prefix=prefix + extension)

    def print_tree(self, path: str) -> None:
        path: Path = Path(path)
        assert path.exists() and path.is_dir()
        # also print to clipboard
        content: str = 'Directory structure of ' + str(path) + '\n\n'
        for line in self.generate(path):
            content += line + '\n'
        print(content, file=sys.stdout)
        content += '\nList of hidden folders\n\n'
        for folder in self.exclude_folders:
            content += folder + '\n'
        content += '\nList of hidden extensions\n\n'
        for extension in self.exclude_extensions:
            content += extension + '\n'
        pyperclip.copy(content)


if __name__ == '__main__':
    exclude_folders_arg: list[str] = ['vendor', 'public', 'storage', 'tests', 'node_modules', 'config', 'bootstrap',
                                      'lang', '.git', '.idea']
    exclude_extensions_arg: list[str] = ['css', 'json', 'scss']

    tree_gen = TreeGenerator(exclude_folders=exclude_folders_arg, exclude_extensions=exclude_extensions_arg)
    directory: str = input('Enter directory: ')
    if directory == '':
        directory = str(Path.cwd())
    tree_gen.print_tree(directory)
