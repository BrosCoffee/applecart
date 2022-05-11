# Applecart Technical Exercise
###
Add instructions for running your program taking a Person ID as command-line argument and
print out the list of connected persons (First Last, one per line) to the console, assuming two text
files ‘persons.json’ and ‘contacts.json’ are found in the same directory. The program should
combine the rules from Parts 2 and 3 where two persons can be connected through either rule
or both.
###
Step 1: cd to the directory
```
cd applecart/
```
Step 2: run `connection.py`
```
python3 connection.py
```
Step 3: enter a valid Person ID and it will return connected persons
```
Please enter a Person ID.
0
Connected Persons:
Joe Smith
Mary Jones
```
```
Please enter a Person ID.
3
Connected Persons:
None.
```
if the Person ID doesn't exist or not valid
```
Please enter a Person ID.
123
ID not found!
```
```
Please enter a Person ID.
abc
Invalid ID!
```
Testing: run pytest
```
pytest connection.py
============================================================ test session starts ============================================================
platform darwin -- Python 3.9.7, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/raymondyang/Desktop/applecart
collected 4 items

connection.py ....                                                                                                                    [100%]

============================================================= 4 passed in 0.04s =============================================================
```

## Note:
1. Write a function that loads any number of Person records into memory from a JSON file
containing an array of objects formatted like the following sample. `json.load()` can handle a decent size of a json file. For a large json file, it might encounter memory issues. Streaming `ijson` or loading data in chunks `read_json(chunk_size)` might be the solutions.
2. Multiple for loops in the `connection.py` file. It is not efficient, but in reality database and queries will handle this problem.
