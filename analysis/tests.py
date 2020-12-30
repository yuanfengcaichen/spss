from django.test import TestCase

# Create your tests here.
b = bytes()
b = str(b'\x80\x04\x95$\x00\x00\x00\x00\x00\x00\x00\x8c 2129f5e3bbdc443b8136be24723e14fc\x94.')
print(type(b))
print(b)
b = bytes(b)
print(type(b))
print(b)
b = b'\x80\x04\x95$\x00\x00\x00\x00\x00\x00\x00\x8c 2129f5e3bbdc443b8136be24723e14fc\x94.'
print(type(b))
print(b)
