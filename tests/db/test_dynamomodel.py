# Copyright (c) 2010-2013 Chris Moyer http://coredumped.org/
# Copyright (c) 2014      Saikat DebRoy <sdebroy@gmail.com>
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
from botoweb.db.property import ListProperty, SetProperty, JSONProperty
from botoweb.db.dynamo import DynamoModel
import time
import uuid


class Model(DynamoModel):
	_table_name = 'Test'

	_properties = {
		'num_list': ListProperty(int),
		'str_list': ListProperty(str),
		'num_set': SetProperty(int),
		'str_set': SetProperty(str),
		'json_item': JSONProperty(),
	}


class Base(object):
	_test_cls = Model

	def setup_class(cls):
		"""Setup this class"""
		cls.objs = []

	def teardown_class(cls):
		"""Remove our objects"""
		for o in cls.objs:
			try:
				o.delete()
			except:
				pass


class TestDynamo(Base):
	def test_list_order(self):
		"""Testing the order of lists"""
		t = self._test_cls()
		t['$id'] = 'TestDynamo' + str(uuid.uuid4())
		t.num_list = [5, 4, 1, 3, 2]
		t.str_list = ["B", "C", "A", "D", "Foo"]
		t.put()
		self.objs.append(t)
		time.sleep(3)
		t = self._test_cls.get_by_id(t.id)
		assert(t.num_list == [5, 4, 1, 3, 2])
		assert(t.str_list == ["B", "C", "A", "D", "Foo"])

	def test_set(self):
		"""Testing assigning and retrieving set values"""
		t = self._test_cls()
		t['$id'] = 'TestDynamo' + str(uuid.uuid4())
		t.num_set = [5, 4, 1, 3, 2, 3, 5]
		t.str_set = ["B", "C", "A", "Foo", "D", "Foo"]
		t.put()
		self.objs.append(t)
		time.sleep(3)
		t = self._test_cls.get_by_id(t.id)
		assert(t.num_set == set([1, 2, 3, 4, 5]))
		assert(t.str_set == set(["A", "B", "C", "D", "Foo"]))

	def test_json(self):
		'Testing assigning and retriveing JSON values'
		t = self._test_cls()
		t['$id'] = 'TestDynamo' + str(uuid.uuid4())
		value = {
			'int_value': 1,
			'str_value': 'A string',
			'list_value': [1, 2, 3, 4],
			'dict_value': {
				'nested': 'value',
			},
		}
		t.json_item = value
		t.put()
		self.objs.append(t)
		time.sleep(3)
		t = self._test_cls.get_by_id(t.id)
		assert(t.json_item.value == value)
