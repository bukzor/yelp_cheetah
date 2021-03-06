from __future__ import unicode_literals

import unittest

from Cheetah.compile import compile_to_class
from Cheetah.NameMapper import NotFound
from Cheetah.NameMapper import valueFromFrame
from Cheetah.NameMapper import valueFromFrameOrSearchList
from Cheetah.NameMapper import valueFromSearchList
from Cheetah.NameMapper import valueForName


class DummyClass(object):
    classVar1 = 123

    def __init__(self):
        self.instanceVar1 = 123

    def meth1(self, arg="doo"):
        return arg

    def meth2(self):
        raise ValueError

    def meth3(self):
        """Tests a bug that Jeff Johnson reported on Oct 1, 2001"""
        x = 'A string'
        return x


class DummyClassGetAttrRaises(object):
    def __getattr__(self, name):
        raise ValueError


def dummyFunc(arg="Scooby"):
    return arg


def funcThatRaises():
    raise ValueError


testNamespace = {
    'aStr': 'blarg',
    'anInt': 1,
    'aFloat': 1.5,
    'aDict': {
        'one': 'item1',
        'two': 'item2',
        'nestedDict': {
            'one': 'nestedItem1',
            'two': 'nestedItem2',
            'funcThatRaises': funcThatRaises,
            'aClass': DummyClass,
        },
        'nestedFunc': dummyFunc,
    },
    'aClass': DummyClass,
    'aFunc': dummyFunc,
    'anObj': DummyClass(),
    'anObjThatRaises': DummyClassGetAttrRaises(),
    'aMeth': DummyClass().meth1,
    'none': None,
    'emptyString': '',
    'funcThatRaises': funcThatRaises,
}

autoCallResults = {
    'aFunc': 'Scooby',
    'aMeth': 'doo',
}

results = testNamespace.copy()
results.update({
    'anObj.meth1': 'doo',
    'aDict.one': 'item1',
    'aDict.nestedDict': testNamespace['aDict']['nestedDict'],
    'aDict.nestedDict.one': 'nestedItem1',
    'aDict.nestedDict.aClass': DummyClass,
    'aDict.nestedFunc': 'Scooby',
    'aClass.classVar1': 123,
    'anObj.instanceVar1': 123,
    'anObj.meth3': 'A string',
})

for k in testNamespace.keys():
    # put them in the globals for the valueFromFrame tests
    exec('%s = testNamespace[k]' % k)

##################################################
# TEST BASE CLASSES


class NameMapperTest(unittest.TestCase):
    failureException = NotFound
    _testNamespace = testNamespace
    _results = results

    def namespace(self):
        return self._testNamespace

    def VFN(self, name, autocall=True):
        return valueForName(self.namespace(), name, autocall)

    def VFS(self, searchList, name, autocall=True):
        return valueFromSearchList(searchList, name, autocall)

    # alias to be overriden later
    get = VFN

    def check(self, name):
        got = self.get(name)
        if name in autoCallResults:
            expected = autoCallResults[name]
        else:
            expected = self._results[name]
        assert got == expected


##################################################
# TEST CASE CLASSES

class VFN(NameMapperTest):

    def test1(self):
        """string in dict lookup"""
        self.check('aStr')

    def test2(self):
        """string in dict lookup in a loop"""
        for _ in range(10):
            self.check('aStr')

    def test3(self):
        """int in dict lookup"""
        self.check('anInt')

    def test4(self):
        """int in dict lookup in a loop"""
        for _ in range(10):
            self.check('anInt')

    def test5(self):
        """float in dict lookup"""
        self.check('aFloat')

    def test6(self):
        """float in dict lookup in a loop"""
        for _ in range(10):
            self.check('aFloat')

    def test7(self):
        """class in dict lookup"""
        self.check('aClass')

    def test8(self):
        """class in dict lookup in a loop"""
        for _ in range(10):
            self.check('aClass')

    def test9(self):
        """aFunc in dict lookup"""
        self.check('aFunc')

    def test10(self):
        """aFunc in dict lookup in a loop"""
        for _ in range(10):
            self.check('aFunc')

    def test11(self):
        """aMeth in dict lookup"""
        self.check('aMeth')

    def test12(self):
        """aMeth in dict lookup in a loop"""
        for _ in range(10):
            self.check('aMeth')

    def test13(self):
        """aMeth in dict lookup"""
        self.check('aMeth')

    def test14(self):
        """aMeth in dict lookup in a loop"""
        for _ in range(10):
            self.check('aMeth')

    def test15(self):
        """anObj in dict lookup"""
        self.check('anObj')

    def test16(self):
        """anObj in dict lookup in a loop"""
        for _ in range(10):
            self.check('anObj')

    def test17(self):
        """aDict in dict lookup"""
        self.check('aDict')

    def test18(self):
        """aDict in dict lookup in a loop"""
        for _ in range(10):
            self.check('aDict')

    def test19(self):
        """aClass.classVar1 in dict lookup"""
        self.check('aClass.classVar1')

    def test20(self):
        """aClass.classVar1 in dict lookup in a loop"""
        for _ in range(10):
            self.check('aClass.classVar1')

    def test23(self):
        """anObj.instanceVar1 in dict lookup"""
        self.check('anObj.instanceVar1')

    def test24(self):
        """anObj.instanceVar1 in dict lookup in a loop"""
        for _ in range(10):
            self.check('anObj.instanceVar1')

    def test27(self):
        """anObj.meth1 in dict lookup"""
        self.check('anObj.meth1')

    def test28(self):
        """anObj.meth1 in dict lookup in a loop"""
        for _ in range(10):
            self.check('anObj.meth1')

    def test29(self):
        """aDict.one in dict lookup"""
        self.check('aDict.one')

    def test30(self):
        """aDict.one in dict lookup in a loop"""
        for _ in range(10):
            self.check('aDict.one')

    def test31(self):
        """aDict.nestedDict in dict lookup"""
        self.check('aDict.nestedDict')

    def test32(self):
        """aDict.nestedDict in dict lookup in a loop"""
        for _ in range(10):
            self.check('aDict.nestedDict')

    def test33(self):
        """aDict.nestedDict.one in dict lookup"""
        self.check('aDict.nestedDict.one')

    def test34(self):
        """aDict.nestedDict.one in dict lookup in a loop"""
        for _ in range(10):
            self.check('aDict.nestedDict.one')

    def test35(self):
        """aDict.nestedFunc in dict lookup"""
        self.check('aDict.nestedFunc')

    def test36(self):
        """aDict.nestedFunc in dict lookup in a loop"""
        for _ in range(10):
            self.check('aDict.nestedFunc')

    def test37(self):
        """aDict.nestedFunc in dict lookup - without autocalling"""
        assert self.get('aDict.nestedFunc', False) == dummyFunc

    def test38(self):
        """aDict.nestedFunc in dict lookup in a loop - without autocalling"""
        for _ in range(10):
            assert self.get('aDict.nestedFunc', False) == dummyFunc

    def test39(self):
        """aMeth in dict lookup - without autocalling"""
        assert self.get('aMeth', False) == self.namespace()['aMeth']

    def test40(self):
        """aMeth in dict lookup in a loop - without autocalling"""
        for _ in range(10):
            assert self.get('aMeth', False) == self.namespace()['aMeth']

    def test41(self):
        """anObj.meth3 in dict lookup"""
        self.check('anObj.meth3')

    def test42(self):
        """aMeth in dict lookup in a loop"""
        for _ in range(10):
            self.check('anObj.meth3')

    def test43(self):
        """NotFound test"""

        def test(self=self):
            self.get('anObj.methX')
        self.assertRaises(NotFound, test)

    def test44(self):
        """NotFound test in a loop"""

        def test(self=self):
            self.get('anObj.methX')

        for _ in range(10):
            self.assertRaises(NotFound, test)

    def test45(self):
        """Other exception from meth test"""

        def test(self=self):
            self.get('anObj.meth2')
        self.assertRaises(ValueError, test)

    def test46(self):
        """Other exception from meth test in a loop"""

        def test(self=self):
            self.get('anObj.meth2')

        for _ in range(10):
            self.assertRaises(ValueError, test)

    def test47(self):
        """None in dict lookup"""
        self.check('none')

    def test48(self):
        """None in dict lookup in a loop"""
        for _ in range(10):
            self.check('none')

    def test49(self):
        """EmptyString in dict lookup"""
        self.check('emptyString')

    def test50(self):
        """EmptyString in dict lookup in a loop"""
        for _ in range(10):
            self.check('emptyString')

    def test51(self):
        """Other exception from func test"""

        def test(self=self):
            self.get('funcThatRaises')
        self.assertRaises(ValueError, test)

    def test52(self):
        """Other exception from func test in a loop"""

        def test(self=self):
            self.get('funcThatRaises')

        for _ in range(10):
            self.assertRaises(ValueError, test)

    def test53(self):
        """Other exception from func test"""

        def test(self=self):
            self.get('aDict.nestedDict.funcThatRaises')
        self.assertRaises(ValueError, test)

    def test54(self):
        """Other exception from func test in a loop"""

        def test(self=self):
            self.get('aDict.nestedDict.funcThatRaises')

        for _ in range(10):
            self.assertRaises(ValueError, test)

    def test55(self):
        """aDict.nestedDict.aClass in dict lookup"""
        self.check('aDict.nestedDict.aClass')

    def test56(self):
        """aDict.nestedDict.aClass in dict lookup in a loop"""
        for _ in range(10):
            self.check('aDict.nestedDict.aClass')

    def test57(self):
        """aDict.nestedDict.aClass in dict lookup - without autocalling"""
        assert self.get('aDict.nestedDict.aClass', False) == DummyClass

    def test58(self):
        """aDict.nestedDict.aClass in dict lookup in a loop - without autocalling"""
        for _ in range(10):
            assert self.get('aDict.nestedDict.aClass', False) == DummyClass

    def test59(self):
        """Other exception from func test -- but without autocalling shouldn't raise"""

        self.get('aDict.nestedDict.funcThatRaises', False)

    def test60(self):
        """Other exception from func test in a loop -- but without autocalling shouldn't raise"""

        for _ in range(10):
            self.get('aDict.nestedDict.funcThatRaises', False)

    def test61(self):
        """Accessing attribute where __getattr__ raises shouldn't segfault if something follows it"""

        def test(self=self):
            self.get('anObjThatRaises.willraise.anything')
        self.assertRaises(ValueError, test)


class VFS(VFN):
    _searchListLength = 1

    def searchList(self):
        return {
            1: [self.namespace()],
            2: [self.namespace(), {'dummy': 1234}],
            3: ({'dummy': 1234}, self.namespace(), {'dummy': 1234}),
            4: self.searchListGenerator(),
        }[self._searchListLength]

    def searchListGenerator(self):
        class Test(object):
            pass

        return iter([
            Test(), {'dummy': 1234}, self.namespace(), {'dummy': 1234}
        ])

    def get(self, name, autocall=True):
        return self.VFS(self.searchList(), name, autocall)


class VFS_2namespaces(VFS):
    _searchListLength = 2


class VFS_3namespaces(VFS):
    _searchListLength = 3


class VFS_4namespaces(VFS):
    _searchListLength = 4


class VFF(VFN):
    def get(self, name, autocall=True):
        locals().update({
            'ns': self._testNamespace,
            'aStr': self._testNamespace['aStr'],
            'aFloat': self._testNamespace['aFloat'],
            'none': 'some',
        })
        return valueFromFrame(name, autocall)

    def setUp(self):
        """Mod some of the data
        """
        self._testNamespace = ns = self._testNamespace.copy()
        self._results = res = self._results.copy()
        ns['aStr'] = res['aStr'] = 'BLARG'
        ns['aFloat'] = res['aFloat'] = 0.1234
        res['none'] = 'some'
        res['True'] = True
        res['False'] = False
        res['None'] = None
        res['eval'] = eval

    def test_VFF_1(self):
        """Builtins"""
        self.check('True')
        self.check('None')
        self.check('False')
        assert self.get('eval', False) == eval
        assert self.get('range', False) == range


class VFFSL(VFS):
    _searchListLength = 1

    def setUp(self):
        """Mod some of the data
        """
        self._testNamespace = ns = self._testNamespace.copy()
        self._results = res = self._results.copy()
        ns['aStr'] = res['aStr'] = 'BLARG'
        ns['aFloat'] = res['aFloat'] = 0.1234
        res['none'] = 'some'

        del ns['anInt']  # will be picked up by globals

    def VFFSL(self, searchList, name, autocall=True):
        locals().update({'anInt': 1, 'none': 'some'})
        return valueFromFrameOrSearchList(searchList, name, autocall)

    def get(self, name, autocall=True):
        return self.VFFSL(self.searchList(), name, autocall)


class VFFSL_2(VFFSL):
    _searchListLength = 2


class VFFSL_3(VFFSL):
    _searchListLength = 3


class VFFSL_4(VFFSL):
    _searchListLength = 4


def test_map_builtins_int():
    template_cls = compile_to_class(
        '''
        #def intify(val)
            #return $int(val)
        #end def
        ''',
    )
    assert 5 == template_cls().intify('5')
