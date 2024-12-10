'''
Tests de aceptación para la practica 6 de codigos y criptografia - MD5

Ejemplo:
    $python -m unittest tests.py

'''

import unittest
import hashlib
import md5

def md5_hash(message: str) -> str:
    """Genera un hash MD5 para el mensaje proporcionado."""
    md5 = hashlib.md5()
    md5.update(message.encode('utf-8'))
    return md5.hexdigest()


class TestMD5Hash(unittest.TestCase):

    def test_bytes_len(self):
        self.assertEqual(len(md5.pad_message(b"Hola")), 64) # 512 bits -> 64 Bytes

    def test_empty_string(self):
        self.assertEqual(md5.md5(""), md5_hash(""))
    
    def test_simple_string(self):
        self.assertEqual(md5.md5("hola"), md5_hash("hola"))
    
    def test_case_sensitivity(self):
        self.assertEqual(md5.md5("Hola"), md5_hash("Hola"))
        self.assertNotEqual(md5.md5("hola"), md5.md5("Hola"))
    
    def test_special_characters(self):
        self.assertEqual(md5.md5("!@#"), md5_hash("!@#"))
    
    def test_unicode_characters(self):
        self.assertEqual(md5.md5("😀"), md5_hash("😀"))
