# basest-python
Converts symbols from any number base to any other number base, in Python

## Usage
Here is a short overview of the functions defined in this library, where to import them from and how to use them.

### Finding the best encoding ratio from one base to another
For a given **input base** (e.g. base-256 / 8-bit Bytes), a given desired **output base** (e.g. base 94) and the maximmum number of symbols to consider using on either side of the encoding ratio (**max chunk size**), return the encoding ratio (in terms of input base to output base) which is the most efficient in terms of data storage achieved.

Returns tuples containing two integers, representing the ratio of **input base** symbols to **output base** symbols.

```py
>>> import basest
>>>
>>> basest.best_ratio_for_base(input_base=256, output_base=94, max_chunk_size=256)
(92, 99)
>>> basest.best_ratio_for_base(input_base=256, output_base=94, max_chunk_size=512)
(355, 382)
```
