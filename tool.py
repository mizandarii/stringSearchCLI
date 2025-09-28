import os
import json
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools



class StringSearchTool:
    def __init__(self):
        # list of ignored file extensions
        self.ignore_extensions = ['.png', '.jpg', '.jpeg', '.svg', '.exe', '.bin', '.gif', '.pdf']

    #creates a list of files to read
    def _collect_files(self, path):
        files_to_search = []

        if os.path.isfile(path):
            ext = os.path.splitext(path)[1].lower()
            if ext not in self.ignore_extensions:
                files_to_search.append(path)
        elif os.path.isdir(path):
            for root, dir, files in os.walk(path):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in self.ignore_extensions:
                        continue
                    files_to_search.append(os.path.join(root, file))
        else:
            raise FileNotFoundError("Provided path does not exist")

        return files_to_search

    #creates a list of indexes
    def _search_in_file(self, file_path, query):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError):
            return None

        positions = []
        start = 0
        while True:
            index = content.find(query, start)
            #if string was not found in file
            if index == -1:
                break
            positions.append(index)
            start = index + 1

        return positions if positions else None

    def search(self, path, query, output="res.json"):
        files_to_search = self._collect_files(path)
        results = {}
        # creates a pool of threads and calls _search_in_file for each file_path
        # itertools.repeat(query) gives a copy of query for each file
        with ThreadPoolExecutor() as executor:
            positions_iter = executor.map(self._search_in_file, files_to_search, itertools.repeat(query))

        #combines file path and positions
        for file_path, positions in zip(files_to_search, positions_iter):
            if positions:
                results[file_path] = positions

        #save to json
        data_to_save = {"query": query, "files": results}
        with open(output, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)

        print(f"Results saved in {output}")

    #show results in different formats
    def show(self, json_file, format):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("file not found")
            return

        query = data["query"]
        files = data["files"]

        for file_path, positions in files.items():
            print(file_path)
            if format == "raw":
                print("  Positions:", positions)
            elif format == "line":
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    for pos in positions:
                        total = 0
                        for i, line in enumerate(lines):
                            total += len(line)
                            if pos < total:
                                print(f"  Line {i+1}: {line.strip()}")
                                break
                except Exception:
                    print("Couldn't read the file")
            elif format == "less":
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    for pos in positions:
                        start = max(0,  pos - 20)
                        end = pos + len(query) + 20
                        context = content[start:end].replace("\n", " ")
                        print(f"  ...{context}...")
                except Exception:
                    print("Could not read the file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="StringSearch",
        description="Looks for input string in provided file/folder"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # searcj
    search_parser = subparsers.add_parser("search", help="find a string in provided file/folder")
    search_parser.add_argument("path", help="path to file/folder")
    search_parser.add_argument("query", help="string")
    search_parser.add_argument("--output", "-o", default="res.json", help="output file")

    # show
    show_parser = subparsers.add_parser("show", help="shows data from JSON file")
    show_parser.add_argument("json_file", help="JSON file with search results")
    show_parser.add_argument("format", choices=["raw", "line", "less"], help="output format")

    args = parser.parse_args()

    tool = StringSearchTool()

    if args.command == "search":
        tool.search(args.path, args.query, args.output)
    elif args.command == "show":
        tool.show(args.json_file, args.format)
