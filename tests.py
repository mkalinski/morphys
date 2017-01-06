# coding: utf8

import unittest as ut
import codecs
import sys

import morphys


# The default encoding is defined by morphys.
# The other encoding could be anything other, used just for testing switchings
# encodings.
_DEFAULT_ENC = 'utf-8'
_OTHER_ENC = 'utf-16'

if sys.version_info.major < 3:
    _uni_t = unicode
    _byt_t = str
else:
    _uni_t = str
    _byt_t = bytes


# Class of the object that will be used to test casting.
class _TestObject(object):

    TEXT = u'żąć'

    def _text(self):
        return self.TEXT

    # Morphys only uses the unicode method to ensure right encoding
    if sys.version_info.major < 3:
        __unicode__ = _text
    else:
        __str__ = _text


class DefaultEncoding(ut.TestCase):
    """Test the ensure functions and StrMorpher with default encoding."""

    def setUp(self):
        self.__u_text = u'łóżko'
        self.__b_text = self.__u_text.encode(_DEFAULT_ENC)

    def test_default_u_to_b(self):
        """ensure_bytes on unicode text encodes it with the default."""

        ens_text = morphys.ensure_bytes(self.__u_text)
        self.assertEqual(ens_text, self.__b_text)

    def test_morph_default_u_to_b(self):
        """
        StrMorpher on unicode text cast to bytes encodes it with the default.
        """

        morph = morphys.StrMorpher(self.__u_text)
        # The identity only occurs after the cast.
        self.assertNotEqual(morph, self.__b_text)
        self.assertEqual(_byt_t(morph), self.__b_text)

    def test_b_to_b(self):
        """ensure_bytes on byte text returns it."""

        ens_text = morphys.ensure_bytes(self.__b_text)
        self.assertIs(ens_text, self.__b_text)

    def test_morph_b_to_b(self):
        """StrMorpher on byte text cast to bytes returns it."""

        morph = morphys.StrMorpher(self.__b_text)
        self.assertNotEqual(morph, self.__b_text)
        self.assertIs(_byt_t(morph), self.__b_text)

    def test_default_b_to_u(self):
        """ensure_unicode on byte text decodes it with the default."""

        dec_text = morphys.ensure_unicode(self.__b_text)
        self.assertEqual(dec_text, self.__u_text)

    def test_morph_default_b_to_u(self):
        """
        StrMorpher on byte text cast to unicode decodes it with the default.
        """

        morph = morphys.StrMorpher(self.__b_text)
        self.assertNotEqual(morph, self.__u_text)
        self.assertEqual(_uni_t(morph), self.__u_text)

    def test_u_to_u(self):
        """ensure_unicode on unicode text returns it."""

        dec_text = morphys.ensure_unicode(self.__u_text)
        self.assertIs(dec_text, self.__u_text)

    def test_morph_u_to_u(self):
        """StrMorpher on unicode text cast to unicode returns it."""

        morph = morphys.StrMorpher(self.__u_text)
        self.assertNotEqual(morph, self.__u_text)
        self.assertIs(_uni_t(morph), self.__u_text)


class OtherEncoding(ut.TestCase):
    """Test ensure functions and StrMorpher with non-default encoding."""

    def setUp(self):
        self.__u_text = u'łóżko'
        self.__b_text = self.__u_text.encode(_OTHER_ENC)

    def test_u_to_b(self):
        """ensure_bytes on unicode text encodes it in selected encoding."""

        ens_text = morphys.ensure_bytes(self.__u_text, encoding=_OTHER_ENC)
        self.assertEqual(ens_text, self.__b_text)

    def test_morph_u_to_b(self):
        """
        StrMorpher on unicode text cast to bytes encodes it in selected encoding.
        """

        morph = morphys.StrMorpher(self.__u_text, encoding=_OTHER_ENC)
        self.assertNotEqual(morph, self.__b_text)
        self.assertEqual(_byt_t(morph), self.__b_text)

    def test_b_to_u(self):
        """ensure_unicode on byte text decodes it in selected encoding."""

        dec_text = morphys.ensure_unicode(self.__b_text, encoding=_OTHER_ENC)
        self.assertEqual(dec_text, self.__u_text)

    def test_morph_b_to_u(self):
        """
        StrMorpher on byte text cast to unicode decodes it in selected encoding.
        """

        morph = morphys.StrMorpher(self.__b_text, encoding=_OTHER_ENC)
        self.assertNotEqual(morph, self.__u_text)
        self.assertEqual(_uni_t(morph), self.__u_text)

    def test_noop_b_to_b(self):
        """ensure_bytes on byte text ignores the actual encoding."""

        enc_text = morphys.ensure_bytes(self.__b_text, encoding=_DEFAULT_ENC)
        self.assertIs(enc_text, self.__b_text)

    def test_morph_noop_b_to_b(self):
        """StrMorpher on byte text cast to bytes ignores the actual encoding."""

        morph = morphys.StrMorpher(self.__b_text, encoding=_DEFAULT_ENC)
        self.assertNotEqual(morph, self.__b_text)
        self.assertIs(_byt_t(morph), self.__b_text)


class ObjectEncoding(ut.TestCase):
    """Testing the ensure functions and StrMorpher on objects."""

    def setUp(self):
        self.__o = _TestObject()

    def test_default_o_to_u(self):
        """ensure_unicode on object casts it to unicode."""

        o_text = morphys.ensure_unicode(self.__o)
        self.assertEqual(o_text, _TestObject.TEXT)

    def test_morph_default_o_to_u(self):
        """
        StrMorpher on object is an effective no-op (casting to unicode works as
        usual).
        """

        morph = morphys.StrMorpher(self.__o)
        self.assertEqual(_uni_t(morph), _uni_t(self.__o))

    def test_default_o_to_b(self):
        """ensure_bytes on object casts it to unicode and encodes."""

        o_btext = morphys.ensure_bytes(self.__o)
        self.assertEqual(o_btext, _TestObject.TEXT.encode(_DEFAULT_ENC))

    def test_morph_default_o_to_b(self):
        """
        StrMorpher on object casts it to unicode and encodes when cast to
        unicode.
        """

        morph = morphys.StrMorpher(self.__o)
        self.assertEqual(_byt_t(morph), _TestObject.TEXT.encode(_DEFAULT_ENC))

    def test_other_o_to_u(self):
        """ensure_unicode on object ignores passed encoding."""

        o_text = morphys.ensure_unicode(self.__o, encoding=_OTHER_ENC)
        self.assertEqual(o_text, _TestObject.TEXT)

    def test_morph_other_o_to_u(self):
        """Casting StrMorpher on object to unicode ignores passed encoding."""

        morph = morphys.StrMorpher(self.__o, encoding=_OTHER_ENC)
        self.assertEqual(_uni_t(morph), _TestObject.TEXT)

    def test_other_o_to_b(self):
        """
        ensure_bytes on object casts it to unicode and encodes in select
        encoding.
        """

        o_btext = morphys.ensure_bytes(self.__o, encoding=_OTHER_ENC)
        self.assertEqual(o_btext, _TestObject.TEXT.encode(_OTHER_ENC))

    def test_morph_other_o_to_b(self):
        """
        StrMorpher on object casts it to unicode and encodes in select
        encoding when cast to bytes.
        """

        morph = morphys.StrMorpher(self.__o, encoding=_OTHER_ENC)
        self.assertEqual(_byt_t(morph), _TestObject.TEXT.encode(_OTHER_ENC))


class EnsureChangedDefaultEncoding(ut.TestCase):
    """Test ensure functions when the default encoding was changed."""

    def setUp(self):
        self.__u_text = u'łóżko'
        self.__b_text = self.__u_text.encode(_OTHER_ENC)
        morphys.default_encoding = _OTHER_ENC

    def tearDown(self):
        morphys.default_encoding = _DEFAULT_ENC

    def test_u_to_b(self):
        """ensure_bytes uses the changed default encoding."""

        enc_text = morphys.ensure_bytes(self.__u_text)
        self.assertEqual(enc_text, self.__b_text)

    def test_b_to_u(self):
        """ensure_unicode uses the changed default encoding."""

        dec_text = morphys.ensure_unicode(self.__b_text)
        self.assertEqual(dec_text, self.__u_text)


class StrMorpherChangedDefaultEncoding(ut.TestCase):

    def setUp(self):
        self.__u_text = u'łóżko'
        self.__b_def_text = self.__u_text.encode(_DEFAULT_ENC)

    def tearDown(self):
        morphys.default_encoding = _DEFAULT_ENC

    def test_u_to_b(self):
        """
        StrMorpher uses the default encoding at the moment of creation for
        encoding.
        """

        morph = morphys.StrMorpher(self.__u_text)
        morphys.default_encoding = _OTHER_ENC
        self.assertEqual(_byt_t(morph), self.__b_def_text)

    def test_b_to_u(self):
        """
        StrMorpher uses the default encoding at the moment of creation for
        decoding.
        """

        morph = morphys.StrMorpher(self.__b_def_text)
        morphys.default_encoding = _OTHER_ENC
        self.assertEqual(_uni_t(morph), self.__u_text)
