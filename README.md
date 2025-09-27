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
