# Copyright (c) 2015      Saikat DebRoy <sdebroy@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
from botoweb.db.property import JSONProperty, ListProperty, SetProperty
from botoweb.db.model import Model
import time


class JSONModel(Model):
	test_prop = JSONProperty()


class ListModel(Model):
	test_prop = ListProperty(str)


class SetModel(Model):
	test_prop = SetProperty(str)


class Base(object):
	def setup_class(cls):
		'''Setup this class'''
		cls.objs = []

	def teardown_class(cls):
		'''Remove our objects'''
		for o in cls.objs:
			try:
				o.delete()
			except:
				pass

	def common_test(self, value):
		t = self._test_cls()
		t.test_prop = value
		doc = t.to_xml()
		tt = self._test_cls.from_xml(doc.toxml().encode('utf-8'))
		assert isinstance(tt, self._test_cls), 'XMLManager unmarshall did not return correct type'
		assert tt.test_prop == t.test_prop, 'XMLManager marshal/unmarshal did not preserve property value'


class TestJSONProperty(Base):
	_test_cls = JSONModel

	def test_int(self):
		self.common_test(1234)
		self.common_test(-1234)

	def test_string(self):
		self.common_test('abcd')
		self.common_test(u'\u2018abcd\u2019')

	def test_bool(self):
		self.common_test(True)
		self.common_test(False)

	def test_list(self):
		self.common_test(['a', 'b', 'c', 'd'])

	def test_dict(self):
		self.common_test({'a': 1, 'b': [2, 3, 4], 'c': {'d': 5, 'e': 6}})


class TestListProperty(Base):
	_test_cls = ListModel

	def test_list(self):
		self.common_test(['abcd', 'efgh', u'\u2018abcd\u2019'])


class TestSetProperty(Base):
	_test_cls = SetModel

	def test_list(self):
		self.common_test(set(['abcd', 'efgh', u'\u2018abcd\u2019']))
