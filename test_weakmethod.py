import unittest2 as unittest
import gc
import weakref
import weakrefmethod

class Object:
    def __init__(self, arg):
        self.arg = arg
    def __repr__(self):
        return "<Object %r>" % self.arg
    def __eq__(self, other):
        if isinstance(other, Object):
            return self.arg == other.arg
        return NotImplemented
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result
    def __lt__(self, other):
        if isinstance(other, Object):
            return self.arg < other.arg
        return NotImplemented
    def __hash__(self):
        return hash(self.arg)
    def some_method(self):
        return 4
    def other_method(self):
        return 5


class WeakMethodTestCase(unittest.TestCase):
    def _subclass(self):
        """Return an Object subclass overriding `some_method`."""
        class C(Object):
            def some_method(self):
                return 6
        return C

    def test_alive(self):
        o = Object(1)
        r = weakrefmethod.WeakMethod(o.some_method)
        self.assertIsInstance(r, weakref.ReferenceType)
        self.assertIsInstance(r(), type(o.some_method))
        self.assertIs(r().__self__, o)
        self.assertIs(r().__func__, o.some_method.__func__)
        self.assertEqual(r()(), 4)

    def test_object_dead(self):
        o = Object(1)
        r = weakrefmethod.WeakMethod(o.some_method)
        self.assertIsInstance(r, weakref.ReferenceType)
        self.assertIsInstance(r(), type(o.some_method))
        self.assertIs(r().__self__, o)
        self.assertIs(r().__func__, o.some_method.__func__)
        self.assertEqual(r()(), 4)

    def test_method_dead(self):
        C = self._subclass()
        o = C(1)
        r = weakrefmethod.WeakMethod(o.some_method)
        del C.some_method
        gc.collect()
        self.assertIs(r(), None)

    def test_callback_when_object_dead(self):
        # Test callback behavior when object dies first.
        C = self._subclass()
        calls = []
        def cb(arg):
            calls.append(arg)
        o = C(1)
        r = weakrefmethod.WeakMethod(o.some_method, cb)
        del o
        gc.collect()
        self.assertEqual(calls, [r])
        # Callback is only called once.
        C.some_method = Object.some_method
        gc.collect()
        self.assertEqual(calls, [r])

    def test_callback_when_method_dead(self):
        # Test callback behavior when method dies first.
        C = self._subclass()
        calls = []
        def cb(arg):
            calls.append(arg)
        o = C(1)
        r = weakrefmethod.WeakMethod(o.some_method, cb)
        del C.some_method
        gc.collect()
        self.assertEqual(calls, [r])
        # Callback is only called once.
        del o
        gc.collect()
        self.assertEqual(calls, [r])

    def test_no_cycles(self):
        # A WeakMethod doesn't create any reference cycle to itself.
        o = Object(1)
        def cb(_):
            pass
        r = weakrefmethod.WeakMethod(o.some_method, cb)
        wr = weakref.ref(r)
        del r
        self.assertIs(wr(), None)

    def test_equality(self):
        def _eq(a, b):
            self.assertTrue(a == b)
            self.assertFalse(a != b)
        def _ne(a, b):
            self.assertTrue(a != b)
            self.assertFalse(a == b)
        x = Object(1)
        y = Object(1)
        a = weakrefmethod.WeakMethod(x.some_method)
        b = weakrefmethod.WeakMethod(y.some_method)
        c = weakrefmethod.WeakMethod(x.other_method)
        d = weakrefmethod.WeakMethod(y.other_method)
        # Objects equal, same method
        _eq(a, b)
        _eq(c, d)
        # Objects equal, different method
        _ne(a, c)
        _ne(a, d)
        _ne(b, c)
        _ne(b, d)
        # Objects unequal, same or different method
        z = Object(2)
        e = weakrefmethod.WeakMethod(z.some_method)
        f = weakrefmethod.WeakMethod(z.other_method)
        _ne(a, e)
        _ne(a, f)
        _ne(b, e)
        _ne(b, f)
        del x, y, z
        gc.collect()
        # Dead WeakMethod compare by identity
        refs = a, b, c, d, e, f
        for q in refs:
            for r in refs:
                self.assertEqual(q == r, q is r)
                self.assertEqual(q != r, q is not r)

    def test_hashing(self):
        # Alive WeakMethods are hashable if the underlying object is
        # hashable.
        x = Object(1)
        y = Object(1)
        a = weakrefmethod.WeakMethod(x.some_method)
        b = weakrefmethod.WeakMethod(y.some_method)
        c = weakrefmethod.WeakMethod(y.other_method)
        # Since WeakMethod objects are equal, the hashes should be equal.
        self.assertEqual(hash(a), hash(b))
        ha = hash(a)
        # Dead WeakMethods retain their old hash value
        del x, y
        gc.collect()
        self.assertEqual(hash(a), ha)
        self.assertEqual(hash(b), ha)
        # If it wasn't hashed when alive, a dead WeakMethod cannot be hashed.
        self.assertRaises(TypeError, hash, c)
