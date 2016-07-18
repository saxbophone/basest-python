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
>
> If you have tried or want to try this out on any other Python implementations, your feedback would be greatly appreciated!
>
> [Open an issue](https://github.com/saxbophone/basest-python/issues) if you are interested.

## Usage
Here is a short overview of the functions defined in this library, where to import them from and how to use them.

#### Encode from one base to another (where the encoding ratios to use are known)
For a given **input base**, **input symbol table**, **output base**, **output symbol table**, **output padding**, **input ratio**, **output ratio** and the **input data** (as an iterable composed of items which are defined in **input symbol table**):
Return the input data, encoded into the specified base using the specified encoding ratio and symbol tables (and the supplied **output padding** symbol used if needed).
Returns the output data as a list of items that are guaranteed to be in the **output symbol table**, or the **output padding** symbol.

```py
>>> import basest
>>>
>>> basest.encode(
...     input_base=256, input_symbol_table=range(256),
...     output_base=85, output_symbol_table=range(85),
...     output_padding=85, input_ratio=4, output_ratio=5,
...     input_data=[99, 97, 98, 98, 97, 103, 101, 115]
... )
[31, 79, 81, 71, 52, 31, 25, 82, 13, 76]
```

#### Decode from one encoded base to another.
For a given **input base**, **input symbol table**, **input padding**, **output base**, **output symbol table**, **input ratio**, **output ratio** and the **input data** (as an iterable composed of items which are defined in **input symbol table**), return the input data, decoded from the base it was encoded into.
Returns the output data as a list of items that are guaranteed to be in the **output symbol table**, with no padding.

> This is essentially the inverse of `encode()`

```py
>>> import basest
>>>
>>> basest.decode(
...     input_base=85, input_symbol_table=range(85), input_padding=85,
...     output_base=256, output_symbol_table=range(256),
...     input_ratio=5, output_ratio=4,
...     input_data=[31, 79, 81, 71, 52, 31, 25, 82, 13, 76]
... )
[99, 97, 98, 98, 97, 103, 101, 115]
```

#### Finding the best encoding ratio from one base to any base within a given range
For a given **input base** (e.g. base-256 / 8-bit Bytes), a given desired **output base** (e.g. base 94) **OR** a given range of acceptable **output bases** and a range of **chunk sizes** to consider using for the input (amount of bytes/symbols processed at once), return the most efficient output base and encoding ratio to use (in terms of input base to output base).

Returns tuples containing an integer as the first item (representing the output base that is most efficient) and a tuple as the second, containing two integers representing the ratio of **input base** symbols to **output base** symbols.

```py
>>> import basest
>>>
>>> basest.best_ratio(input_base=256, output_bases=[94], chunk_sizes=range(1, 256))
(94, (68, 83))
>>> basest.best_ratio(input_base=256, output_bases=[94], chunk_sizes=range(1, 512))
(94, (458, 559))
>>> basest.best_ratio(input_base=256, output_bases=range(2, 95), chunk_sizes=range(1, 256))
(94, (68, 83))
>>> basest.best_ratio(input_base=256, output_bases=range(2, 334), chunk_sizes=range(1, 256))
(333, (243, 232))
```

## Further Examples

#### Base-78, using emoji as output (just for fun)
Unicode character ranges `0x1F601` through to `0x1F64F` are allocated for *emoticon emoji*. This range provides us with 78 characters to play with.

First of all, let's find us some appropriate encoding ratios within given ranges:

```py
>>> from basest import best_ratio
>>> best_ratio(256, [78], range(2, 1024))
(78, (1019, 1297))  # hmm, maybe a bit too big
>>> best_ratio(256, [78], range(2, 16))
(78, (7, 9))  # we could probably go a bit larger but this will do
```

Now, let's choose a padding character from one of the other Unicode emoji codepages. I decided to choose the `bear face` emoji (:bear: / 🐻), codepoint `0x1F43B`.

With these chosen parameters and a body of input data (will use text for this example), we can put it all together:

```py
>>> from basest import encode
>>> # input data variable
>>> message = ...
>>> output = encode(
    256, [chr(i) for i in range(256)],  # input base and symbol table
    78, [chr(0x1F601 + o) for o in range(78)],  # output base and symbol table
    chr(0x1F43B),  # padding character
    7, 9,  # encoding ratio
    message
)
```

Given this input message (in ASCII):

```
Fourscore and seven years ago our fathers brought forth on this
continent a new nation, conceived in liberty and dedicated to the
proposition that all men are created equal.
Now we are engaged in a great civil war, testing whether that nation
or any nation so conceived and so dedicated can long endure. We are
met on a great battle field of that war. We have come to dedicate a
portion of that field, as a final resting place for those who here
gave their lives that that nation might live. It is altogether
fitting and proper that we should do this.
But, in a larger sense, we can not dedicate - we can not consecrate
- we can not hallow - this ground. The brave men, living and dead,
who struggled here, have consecrated it, far above our poor power to
add or detract. The world will little note, nor long remember, what
we say here, but it can never forget what they did here. It is for
us the living, rather, to be dedicated here to the unfinished work
which they who fought here have thus far so nobly advanced. It is
rather for us to be here dedicated to the great task remaining
before us - that from these honored dead we take increased devotion
to that cause for which they gave the last full measure of devotion
- that we here highly resolve that these dead shall not have died in
vain - that this nation, under God, shall have a new birth of
freedom - and that government of the people, by the people, for the
people, shall not perish from the earth.
```

We get this output:

😃😉😳😿😷😤😿😺🙆😗🙆🙃😢😼🙊🙋😧😡😇😴🙎🙉😋😧😲😑😍😙🙊😖😿😰😿😂😼😤😖😔😤

😜😅😬😃😝😉😖😃😭😷🙇😥😅😗😰😇😳🙊😎😟😔😌😝🙍😘🙃🙂😬😧😻😟😠😏😇😴😻😬😹😆

😌🙊😈😘😲😣😐😜😣😐😆😨😗😶😂😔😟🙎😃😗🙍😗😶😂😡😘😜😓😛😩😖😴😩😰😸😩😈😜😊

😗😵🙆😙😗🙌😹😼😃😇😴😞😕😼😟😲🙊😡😕🙂😰🙀😫😊😼😗😗😕😭😤😕😝🙃🙇😽😔😕😂😲

😹😺😏😎😬😂😇😵😅🙄😚😎😛😑😣😗🙆😹🙄😦😃😂😝😾😗🙆😮😯😘🙍🙃🙂😏😇😳🙅😎😱😈

😛🙌😼😗😱😷😊😄😐😎😵🙀😘😨😉😭😇😧🙁🙇😝😕🙂😫🙋😅🙌😺🙀🙍😑😉🙄😹😞😕😣😟😅

😕😂😨🙋😶😯😨😟😈😕😁🙁😔🙎😡😾😅😓😇😳🙃😹😪😥😞🙍😖😘🙃🙂😧🙎🙊😈😦😃😇😵😔

😞😥😒😗😎😏😕🙂😵😷😖😤😣😧🙍😙😪😡😻😄😓😟😄😱😇😵😅🙄😘😫😩😖😩😕😂😲😿😻😣

😆😦🙆😘😣😾😶😄😓😓😨😅😕😂😲😿😻😣😇😡😌😗🙁😹😄😨😝🙌😡😊😖😴🙋😱😢😷😹🙈😍

😕😭😤😫😺😼😲🙇😖😕😲😂😴😎😟😯😭😅😇😳🙎😹🙈😩🙆😨🙊😗😶😊😩🙉😲🙍😃😲😘😨😈

😮😹😸🙍😩😙😕😂😨🙋😬😲🙁😆😇😇😴😻😬😹😃😧😓🙄😘😨😉😭😇😞😘😭😦😘🙉😈😾😼😧

😵😭😒😕🙂😓😑😕😺😱😁😩😘🙈😛🙎😭😰🙅😖😄😘😤😳😾😽🙂😆🙋😱😕😂😼😦🙎😝😨😊🙄

😕😽😦😤😺😔😳😁😆😕😲😂😴😎😟😯😬😏😔🙊😁😠😮😷😥😺😼😗🙆😮😯😖😸😽😭🙅😖😣😱

😦😧😺😭😲😐😗😕🙆😙🙆😨😇😫😥😔🙋😞😱🙃😟😬😪😓😇😴🙊😄😗😹😆😧😇😖😏😪😍😽😾

😊😯😦😇😴😏😳😔😋😃😝😹😗🙆🙈😙😯😢😬😪😮😇😴😙😒😂😿🙈😑😬😕😂😼😦🙎😟🙂🙋😖

😖😴😶😽😪😠🙅😘😼😘😳🙀🙉😽😬😌🙃😱😘🙈😛🙎😭😰🙄🙆😨😘🙈😡😌😏😿😚😾😠😖😔😃

😼😽😟🙊🙎😭😕😾😛😑😊😰😱😢🙄😘😳🙀😭😪😽😙😑😸😕🙂😺😜😒😷😒😹😓😖😴🙂😌😊😸

😹😮😓😕😂😕😠🙆🙀😏😌😦😘😈😆😈🙅😉😅🙄😈😘🙃🙂🙅😹😲😕😖😻😗🙇😄😒😅😑😺🙍🙄

😇😵😅🙄😜😎😑🙃😇😎😳🙋😕🙄😴😒😌😹😇😳🙃😹😬😷🙀😟😈😕🙂😯😑😫😼😇😗😠😕😾😑

😣😺😫😶😴🙆😕😂😔😊😏🙈😸😔😳😕😱😽😌😠😔😞😥😑😕😽😥😈😴😕😅😟😽😕😡😧🙈😄😗

😈🙇😥😇😳🙎🙎😻😋😝😦😾😘😧🙄😟🙋😟😪😴😃😙😪😑😽🙀🙈😐😭🙅😗😶😳😏😈😵😝🙂😟

😗😖😯😤😫😼😄😳🙅😖😤😊😩😱😔😶😰😢😙😊😻😓😈😈😳😚🙋😕😽😦😉🙍😋😞🙅🙊😇😴😱

😲😋😉😦😙😉😖😴🙋😷😣😧😚😭😦😗😵🙉🙅😣🙂😵😢😯😊😄😹😙😌😵🙀🙄😾😘🙈🙍😐😨🙊

😑😉😮😕😭😤😛😚😂😋😃😡😇😴😙😌😈😧😄🙆😲😗🙆😰😎😶🙈😟😙😢😘🙈😍😠😆😣😔😢😳

😇😴😏😞😡😵😁😝😛😗🙇😈🙌😆😻😍🙂😕😇😴🙀😥😧😛🙉😣😥😗🙇😍🙃😞😑🙂😂🙎😃😋😛

😡😫😑😨😗🙃😇😴😅😶😹🙌😏🙃🙈😘🙄😷😭😽😟😚😕😕😙😪🙄😎😊😋😟😁😠😖😴😚🙉😏🙀

😧🙄😋😘🙈😯😯😛😮😦🙈🙇😕😾😑😣😶😦🙉😤😯😗😖😯😗😭😱😕😧😂😗😥🙎😛😘😥😐😣😅

😇😵😔😨😽🙅😑😗😄😕😽😦😣😎😃😝🙁😹😕🙂😰😩😽😹🙉😫🙊😘🙃🙂😰🙍🙌😫😛🙆😗😱😷

😝😘😼😠😧🙋😇😴😏😳😔😔🙁😫😑😇😵😔😨😽🙅😒😑😑😖😣🙅😉😓😵😢😱😁😇😴😙😒😂😿

🙉😸😿😐😈😄😂🙍😡😭😇😃😗🙆🙁😷🙆😨😝🙌😓😖😣🙃😡😗😐😅🙁😲😗😶😊😻😞😼🙍😺😯

😖😣🙄🙌🙆😼😗😌😦😇😳🙉🙈😮🙍😠😨😷😖😳😼😽🙅😩🙂😘😛😖😣🙄🙍😒😯😤😋😸😇😵😅

🙄😚😑😞😠😙😖😄😆😳😯😗😣😿🙊😕😭😤😱😷😄😕😉😃😙😪😡🙀🙆😴😱😲😯😖😣🙅😉😓😸

😅😓😼😇😴😏😳😕😰🙆😤😯😇😴😙😒😂😿🙉😋😽😕😂😼😦🙎😟🙂🙋😦😘😳🙀😴🙇🙊🙌😆🙊

😗🙁😹😔🙄😸😰😼😬😇😳🙅😂😽😦😖🙆😒😕🙁😹😊😚😛🙈😖😿😖😴😻😓😴🙁🙄😥😵😕🙂😯

😑😥🙅🙄😠🙃😙😋😄😜😥🙊😐😸😍😕😽😦😒🙁😥😬😥😽😕😱😽😌😠😔😞😥😑😕🙁😸🙃🙎😂

🙀🙍😉😖😣🙃😡😔🙊😪😇😂😘🙃🙂🙁😓🙄😮😲😷😘😨😉😾🙁😗😪🙍😮😗😶😊😉😏😫😆🙈😪

😘😨😈😚😟🙁🙄😸😠😇😵😅🙄😘😫😩😖😡😘😨😺😰😸😖😺😬🙀😘😸😊😑🙁😟😏😰😖😘😨😉

😱😅😩😷😆😄😕😭😤😱😲😝😠😓😺😗😅🙉😇😾😐🙌😢😡😕🙁😫😾🙆😰🙀😎😻😕🙂🙄😔😞😯

😧😐😅😃😌😪😟😑😚😋😡😂😘🙃🙂😧🙋😙😋😜😤😇😴😏😳😔😋😃😧😭😖😳😼🙇😿😸😐😭😚

😙🙅🙌😃😢😸😷😝😩😘🙈😜😆😃😿🙉😫😸😘🙃🙂😬😪😤😵🙎🙃😗😥🙎😉😫😿😬😄😠😇😴😻

😠🙀😽😝😐🙅😗🙆🙍😖🙁😿😆😵😒😇😵😅🙄😘😫😩😖😲😕😽😦😒🙁😥😬😥😽😖😤😊😘😏😧

🙍😾🙋😘😨😉🙇🙁🙂😛🙉😖😇😵😅🙄😘😫😩😖😯😖😣🙄🙎😸😲😂😊😜😕😁😱😗🙋😺🙀🙊😛

😗😑😳😮😜😞😽😋😅😕😂😼😦🙎😝😲😳😖😕😭😤😜🙃🙊😪😨😤😖😴😣😓🙃🙋😓😆😋😕😂😱

😡😏😗😕🙂😦😇😴😶😣😄😔😛🙍😇😊😆😈😶😟😅🙀😞😁😇😲😔😗😬😆😇😋😈😖😣😱😛😃😿

😑😱😒😙😚😏🙆😘😣😇😽🙆😙😥🙈😍😃😕😕😩😩😇😴😻😠😶😿🙄😎😤😕🙁😺😝😥😙😵😘😏

😕😂😕😠🙆🙀😹🙀😘😘🙃🙂😭🙍😾😨😩😏😗😶😩😋😮😴🙄😟🙈😕🙍😨😜😐😴😇😵😉😕🙂😢

😈😃🙆😴🙎😇😕😒🙋😸🙀🙋😪😳🙁😘😈😆😄🙅😔😫😗😉😇😴😏😳😔😋😃😝😹😕😼😈🙌😫🙍

😓😅🙍😕😾😑😣😸😺😹😚🙇😗😑😳😮😜😞😽😋😍😕🙂😰😰😌😎😔😙😣😘😨😺😰😸😖😺😬🙀

😇😴😊😧😯😞😄😎😵😃😅😓🐻🐻🐻🐻🐻🐻
