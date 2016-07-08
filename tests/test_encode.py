import unittest

from ddt import data, ddt, unpack

from basest import encode


@ddt
class TestEncode(unittest.TestCase):
    @data(
        (
            256, 85, 4, 5,
            [99, 97, 98, 98, 97, 103, 101, 115],
            [31, 79, 81, 71, 52, 31, 25, 82, 13, 76]
        )
    )
    @unpack
    def test_encode(
        self, input_base, output_base, input_ratio, output_ratio, input_data,
        expected_output_data
    ):
        """
        Test that basest.encode can encode data to an expected output given
        various base and ration settings and that it can also decode the output
        back to the original input.
        """
        output_data = encode(
            input_base=input_base, input_symbol_table=range(input_base),
            output_base=output_base, output_symbol_table=range(output_base),
            input_ratio=input_ratio, output_ratio=output_ratio,
            input_data=input_data
        )

        self.assertEqual(output_data, expected_output_data)

        decoded_data = encode(
            input_base=output_base, input_symbol_table=range(output_base),
            output_base=input_base, output_symbol_table=range(input_base),
            input_ratio=output_ratio, output_ratio=input_ratio,
            input_data=output_data
        )

        self.assertEqual(decoded_data, input_data)
