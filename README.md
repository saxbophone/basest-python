# basest-python
Converts symbols from any number base to any other number base, in Python

## What?
In short, **basest** is *based on* (pun *definitely* intended :wink:) the concept of binary-to-text conversion, that is where binary or 8-bit data is converted or serialised into a text-based representation format that can be safely passed through a medium that would otherwise destroy or corrupt the meaning of the binary data.

This concept is very commonly used in areas such as Email, the PDF format and Public Key Cryptography, to name but a few.

There are many different formats and schemes for serilising binary data to text, employing different alphabet sizes and different printable ASCII characters used for various different reasons.

It is also not just 8-bit binary data that could be serialised. Any collection of symbols declared to be in a given number base or alphabet size can be serialised into any other, provided an encoding ratio between the two symbols can be established and the input and output symbols defined.

This library is my implementation of a generic, base-to-base converter which addresses this last point. An encoder and decoder for every binary-to-text format currently existing can be created and used with this library, requiring only for the details of the desired format to be given. Due to its flexibility, the library also makes it trivial to invent new wonderful and interesting base-to-base serialisation/conversion formats (I myself plan to work on and release one that translates binary files into a purely emoji-based format!).

So, I hope you find this library fun, useful or both!

## Installation

#### Python Versions Supported
This library is designed to work with the following **CPython** versions: **2.7.x**, **3.3.x or greater**.

> :bulb: **Help Wanted**
> If you have tried or want to try this out on any other Python implementations, your feedback would be greatly appreciated!
>
> [Open an issue](https://github.com/saxbophone/basest-python/issues) if you are interested.

## Usage
Here is a short overview of the functions defined in this library, where to import them from and how to use them.

#### Encode from one base to another (where the encoding ratios to use are known)
For a given **input base**, **input symbol table**, **output base**, **output symbol table**, **input ratio**, **output ratio** and the **input data** (as an iterable composed of items which are defined in **input symbol table**):
Return the input data, encoded into the specified base using the specified encoding ratio and symbol tables.
Returns the output data as a list of items that are guaranteed to be in the **output symbol table**.

```py
>>> import basest
>>>
>>> basest.encode(
...     input_base=256, input_symbol_table=range(256),
...     output_base=85, output_symbol_table=range(85),
...     input_ratio=4, output_ratio=5,
...     input_data=[99, 97, 98, 98, 97, 103, 101, 115]
... )
[31, 79, 81, 71, 52, 31, 25, 82, 13, 76]
```

#### Finding the best encoding ratio from one base to any base within a given range
For a given **input base** (e.g. base-256 / 8-bit Bytes), a given desired **output base** (e.g. base 94) **OR** a given range of acceptable **output bases** and a range of **chunk sizes** to consider using for the input (amount of bytes/symbols processed at once), return the most efficient output base and encoding ratio to use (in terms of input base to output base).

Returns tuples containing an integer as the first item (representing the output base that is most efficient) and a tuple as the second, containing two integers representing the ratio of **input base** symbols to **output base** symbols.

```py
>>> import basest
>>>
>>> basest.best_ratio(input_base=256, output_base=94, chunk_sizes=range(256))
(94, (92, 99))
>>> basest.best_ratio(input_base=256, output_base=94, chunk_sizes=range(512))
(94, (355, 382))
>>> basest.best_ratio(input_base=256, output_bases=range(2, 95), chunk_sizes=range(256))
(94, (68, 83))
>>> basest.best_ratio(input_base=256, output_bases=range(2, 333), chunk_sizes=range(256))
(333, (243, 232))
```
