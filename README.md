# Remove approximate duplicates

Sometimes there is a need to get unique or almost unique words from a text.

This program reads lines from a file, removes approximate duplicates, writes result to a file.
Uses a sliding window to keep track of last N lines.

## The similarity limit

the close it is to 1, the stricter the check is, and as a result the more lines go to the output.

## Running

Example:

```
remove_dups.py -i txt-in -o txt-out -s 0.94

```

Input example:
```
abate
abated
abates
abaton
abater
```

Output example:
```
abate
abaton
```
