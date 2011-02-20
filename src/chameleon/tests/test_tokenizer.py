from unittest import TestCase


class TokenizerTest(TestCase):
    def test_sample_files(self):
        import os
        import traceback
        path = os.path.join(os.path.dirname(__file__), "inputs")
        for filename in os.listdir(path):
            if not filename.endswith('.xml'):
                continue
            f = open(os.path.join(path, filename), 'rb')
            source = f.read()

            from ..utils import read_encoded
            try:
                want = read_encoded(source)
            except UnicodeDecodeError as e:
                self.fail("%s - %s" % (e, filename))

            from ..tokenize import iter_xml
            try:
                tokens = iter_xml(want)
                got = "".join(tokens)
            except:
                self.fail(traceback.format_exc())

            from doctest import OutputChecker
            checker = OutputChecker()

            if checker.check_output(want, got, 0) is False:
                from doctest import Example
                example = Example(f.name, want)
                diff = checker.output_difference(
                    example, got, 0)
                self.fail("(%s) - \n%s" % (f.name, diff))
