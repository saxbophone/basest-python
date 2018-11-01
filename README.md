# basest-python
Arbitrary base binary-to-text encoder (any base to any base), in Python.

## What?
In short, **basest** is *based on* (pun *definitely* intended :wink:) the concept of binary-to-text conversion, that is where binary or 8-bit data is converted or serialised into a text-based representation format that can be safely passed through a medium that would otherwise destroy or corrupt the meaning of the binary data.

This concept is very commonly used in areas such as Email, the PDF format and Public Key Cryptography, to name but a few.

There are many different formats and schemes for serilising binary data to text, employing different alphabet sizes and different printable ASCII characters used for various different reasons.

It is also not just 8-bit binary data that could be serialised. Any collection of symbols declared to be in a given number base or alphabet size can be serialised into any other, provided an encoding ratio between the two symbols can be established and the input and output symbols defined.

This library is my implementation of a generic, base-to-base converter which addresses this last point. An encoder and decoder for every binary-to-text format currently existing can be created and used with this library, requiring only for the details of the desired format to be given. Due to its flexibility, the library also makes it trivial to invent new wonderful and interesting base-to-base serialisation/conversion formats (I myself plan to work on and release one that translates binary files into a purely emoji-based format!).

One limitation of the library is that it cannot encode data from a smaller input base to a larger output base with padding on the input (i.e. if you're encoding from base 2 to base 1000, you need to ensure that the number of input symbols exactly matches the encoding ratio you're using). This is an accepted limitation due to the complexities of implementing a padding system that works in the same manner as base-64 and others but which can be extended to any arbitrary base.

So, I hope you find this library fun, useful or both!

## Installation

#### Python Versions Supported
This library is designed to work with the following **CPython** versions: **2.7.x**, **3.3.x or greater**.

> :bulb: **Help Wanted**
>
> If you have tried or want to try this out on any other Python implementations, your feedback would be greatly appreciated!
>
> [Open an issue](https://github.com/saxbophone/basest-python/issues) if you are interested.

#### Install from PyPi (preferred)
> **Note:** Package is currently not hosted on PyPi, but will be in the future.

`pip install basest`

#### Install from git repository (at master branch)
`pip install git+git://github.com/saxbophone/basest-python`

## Usage
Here is a short overview of the interfaces defined in this library, where to import them from and how to use them.

There is a functional interface and a class-based interface (the class-based one piggy-backs on the functional one, but will also be used to add additional features in the future).

### Class-based Interface

To use the class-based interface, you will need to create a subclass of `basest.encoders.Encoder` and override attributes of the class, as shown below (using base64 as an example):

```py
from basest.encoders import Encoder

class CustomEncoder(Encoder):
    input_base = 256
    output_base = 64
    input_ratio = 3
    output_ratio = 4
    # these attributes are only required if using decode() and encode()
    input_symbol_table = [chr(c) for c in range(256)]
    output_symbol_table = [
        s for s in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    ]
    padding_symbol = '='

```

> **Note:** You must subclass `Encoder`, you cannot use it directly!

Subclasses of `Encoder` have the following public methods available:

#### Encode from one base to another
`encode()` will encode an iterable of symbols in the class' **input symbol table** into an iterable of symbols in the class' **output symbol table**, observing the chosen encoding ratios and padding symbol.

```py
encoder = CustomEncoder()
encoder.encode(['c', 'a', 'b', 'b', 'a', 'g', 'e', 's'])
# -> ['Y', '2', 'F', 'i', 'Y', 'm', 'F', 'n', 'Z', 'X', 'M', '=']
```

#### Encode Raw
`encode_raw()` works just like `encode()`, except that symbols are not interpreted. Instead, plain integers within range 0->(base - 1) should be used. the value of the base is used as the padding symbol.

```py
encoder = CustomEncoder()
encoder.encode_raw([1, 2, 3, 4, 5, 6, 7])
# -> [0, 16, 8, 3, 1, 0, 20, 6, 1, 48, 64, 64]
```

#### Decode from one base to another
`decode()` works in the exact same way as `encode()`, but in the inverse.

```py
encoder = CustomEncoder()
encoder.decode(['Y', '2', 'F', 'i', 'Y', 'm', 'F', 'n', 'Z', 'X', 'M', '='])
# -> ['c', 'a', 'b', 'b', 'a', 'g', 'e', 's']
```

#### Decode Raw
`decode_raw()` works just like `decode()`, except that symbols are not interpreted. Instead, plain integers within range 0->(base - 1) should be used. the value of the base is used as the padding symbol.

```py
encoder = CustomEncoder()
encoder.decode_raw([0, 16, 8, 3, 1, 0, 20, 6, 1, 48, 64, 64])
# -> [1, 2, 3, 4, 5, 6, 7]
```

### Functional Interface

#### Encode from one base to another (where the encoding ratios to use are known)
For a given **input base**, **input symbol table**, **output base**, **output symbol table**, **output padding**, **input ratio**, **output ratio** and the **input data** (as an iterable composed of items which are defined in **input symbol table**):
Return the input data, encoded into the specified base using the specified encoding ratio and symbol tables (and the supplied **output padding** symbol used if needed).
Returns the output data as a list of items that are guaranteed to be in the **output symbol table**, or the **output padding** symbol.

```py
import basest

basest.core.encode(
    input_base=256,
    input_symbol_table=[chr(c) for c in range(256)],
    output_base=64,
    output_symbol_table=[
        s for s in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    ],
    output_padding='=', input_ratio=3, output_ratio=4,
    input_data='falafel'
)
# -> ['Z', 'm', 'F', 's', 'Y', 'W', 'Z', 'l', 'b', 'A', '=', '=']
```

#### Encode Raw
Similar to the function above, `basest.core.encode_raw` will encode one base into another, but only accepts and returns arrays of integers (e.g. bytes would be passed as integers between 0-255, not as `byte` objects). As such, it omits the **padding** and **symbol table** arguments, but is otherwise identical in function and form to `encode`.

```py
import basest

basest.core.encode_raw(
    input_base=256, output_base=85,
    input_ratio=4, output_ratio=5,
    input_data=[99, 97, 98, 98, 97, 103, 101, 115]
)
# -> [31, 79, 81, 71, 52, 31, 25, 82, 13, 76]
```

#### Decode from one encoded base to another.
For a given **input base**, **input symbol table**, **input padding**, **output base**, **output symbol table**, **input ratio**, **output ratio** and the **input data** (as an iterable composed of items which are defined in **input symbol table**), return the input data, decoded from the base it was encoded into.
Returns the output data as a list of items that are guaranteed to be in the **output symbol table**, with no padding.

> This is essentially the inverse of `encode()`

```py
import basest

basest.core.decode(
    input_base=64,
    input_symbol_table=[
        s for s in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    ],
    input_padding='=',
    output_base=256, output_symbol_table=[chr(c) for c in range(256)],
    input_ratio=4, output_ratio=3,
    input_data='YWJhY3VzIFpaWg=='
)
# -> ['a', 'b', 'a', 'c', 'u', 's', ' ', 'Z', 'Z', 'Z']
```

#### Decode Raw
Similar to the function above, `basest.core.decode_raw` will decode from one base to another, but only accepts and returns arrays of integers (e.g. base64 would be passed as integers between 0-65 (65 is for the padding symbol), not as `str` objects). As such, it omits the **padding** and **symbol table** arguments, but is otherwise identical in function and form to `decode`.

```py
import basest

basest.core.decode_raw(
    input_base=85, output_base=256,
    input_ratio=5, output_ratio=4,
    input_data=[31, 79, 81, 71, 52, 31, 25, 82, 13, 76]
)
# -> [99, 97, 98, 98, 97, 103, 101, 115]
```

#### Finding the best encoding ratio from one base to any base within a given range
For a given **input base** (e.g. base-256 / 8-bit Bytes), a given desired **output base** (e.g. base 94) **OR** a given range of acceptable **output bases** and a range of **chunk sizes** to consider using for the input (amount of bytes/symbols processed at once), return the most efficient output base and encoding ratio to use (in terms of input base to output base).

Returns tuples containing an integer as the first item (representing the output base that is most efficient) and a tuple as the second, containing two integers representing the ratio of **input base** symbols to **output base** symbols.

```py
import basest

basest.core.best_ratio(input_base=256, output_bases=[94], chunk_sizes=range(1, 256))
# -> (94, (68, 83))
basest.core.best_ratio(input_base=256, output_bases=[94], chunk_sizes=range(1, 512))
# -> (94, (458, 559))
basest.core.best_ratio(input_base=256, output_bases=range(2, 95), chunk_sizes=range(1, 256))
# -> (94, (68, 83))
basest.core.best_ratio(input_base=256, output_bases=range(2, 334), chunk_sizes=range(1, 256))
# -> (333, (243, 232))
```
