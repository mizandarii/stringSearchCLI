# StringSearchTool  
StringSearchTool is a Python command-line utility for searching strings in files and directories. It supports parallel search using threads, ignores binary files, and can display search results in different formats.

## Features
* Search for a string in a single file or all files in a directory.  
* Ignore files with non-text extensions (images, binaries, PDFs, etc.).  
* Multithreaded search for faster results on large datasets.  
* Save search results to a JSON file.  
* Display search results in multiple formats:  
  * raw — show only positions of matches.  
  * line — show lines where matches occur.  
  * less — show match with 20 characters before and after.  
Works with text files encoded in UTF-8.  

## Requirements

- Python 3.10+ (tested on 3.12)  
- No external dependencies (only Python standard library)   
## Usage
### 1. Search for a string 
Search for all occurencies in a string in a given file or folder.
Results will be saved into a JSON file (default: 'res.json')

```bash
python3 tool.py search <path> <query>
```
Example
```bash
python3 tool.py search testData "Python"
```
This will create a res.json file with the following structure
```
{
    "query": "Python",
    "files": {
        "testData/example.txt": [13, 57, 102]
    }
}
```

### 2. Show results from JSON
Display saved results in different formats
```bash
python3 tool.py show <json_file> <format>
```
Formats: 
* raw - shows only character positions
* line - shows full lines where the query was found
* less - shows query in context (20 characters before and after)

Examples:   
```bash
python3 tool.py show res.json raw
```

```bash
python3 tool.py show res.json raw
```

```bash
python3 tool.py show res.json raw
```
