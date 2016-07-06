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

### Finding the best encoding ratio from one base to any base within a given range

For a given **input base**, an iterable of one or more acceptable **output bases** and the maximmum number of symbols to consider using on either side of the encoding ratio (**max chunk size**), return the most efficient base pair and encoding ratio to use (in terms of input base to output base).

Returns tuples containing an integer as the first item (representing the output base that is most efficient), and a tuple as the second, which is the same as the output of the previous function i.e. the encoding ratio to use.

```py
>>> import basest
>>>
>>> basest.best_ratio_for_base_range(input_base=256, output_bases=range(2, 95), max_chunk_size=256)
(94, (68, 83))
>>> basest.best_ratio_for_base_range(input_base=256, output_bases=range(2, 333), max_chunk_size=256)
(333, (243, 232))
```
