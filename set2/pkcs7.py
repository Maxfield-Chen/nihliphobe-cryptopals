import unittest as ut

def pkcs7(data, pl):
    if pl > 255:
        raise AssertionError("Cannot use blocksize longer than 255 bytes")
    pb = pl - (len(data) % pl)
    return data + chr(pb) * pb

class TestPKCS7(ut.TestCase):
    def test_none(self):
        self.assertEqual(pkcs7("A"*8, 8), "A"*8+chr(8)*8)
    def test_full(self):
        self.assertEqual(pkcs7("", 8), chr(8)*8)
    def test_partial(self):
        self.assertEqual(pkcs7("A"*3, 8), "A"*3+chr(5)*5)
    def test_given(self):
        self.assertEqual(pkcs7("YELLOW SUBMARINE", 20), "YELLOW SUBMARINE" + chr(4)*4)

if __name__ == '__main__':
    ut.main()
