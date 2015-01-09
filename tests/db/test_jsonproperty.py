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
from botoweb.db.property import JSONProperty
from botoweb.db.model import Model
import time


class JSONModel(Model):
	json_prop = JSONProperty()


class TestJSONProperty(object):

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

	def test_none_value(self):
		'''Testing setting JSONProperty to None'''
		t = JSONModel()
		t.json_prop = None
		assert t.json_prop is None, 'JSONProperty field should return underlying object'
		t.put()
		time.sleep(3)
		id = t.id
		tt = JSONModel.get_by_id(id)
		assert tt is not None, 'Should be able to fetch objects saved to db by id'
		assert tt.json_prop is None, 'Fetched JSONProperty with a list should match original'

	def test_bool_value(self):
		'''Testing setting JSONProperty to bools'''
		t = JSONModel()
		t.json_prop = True
		assert t.json_prop is True, 'JSONProperty field should return underlying object'
		t.put()
		time.sleep(3)
		id = t.id
		tt = JSONModel.get_by_id(id)
		assert tt is not None, 'Should be able to fetch objects saved to db by id'
		assert tt.json_prop, 'Fetched JSONProperty with True should be truthy'
		t.json_prop = False
		t.put()
		time.sleep(3)
		tt = JSONModel.get_by_id(id)
		assert tt is not None, 'Should be able to fetch objects saved to db by id'
		assert not tt.json_prop, 'Fetched JSONProperty with False should not be truthy'

	def test_string_value(self):
		'''Testing setting JSONProperty to a string'''
		t = JSONModel()
		t.json_prop = 'abcd'
		assert t.json_prop == 'abcd', 'JSONProperty field should return underlying object'
		t.json_prop = u'\u2018' + t.json_prop + u'\u2019'
		assert t.json_prop == u'\u2018abcd\u2019', 'JSONProperty field set to string should allow concatenation'
		t.put()
		time.sleep(3)
		id = t.id
		tt = JSONModel.get_by_id(id)
		assert tt is not None, 'Should be able to fetch objects saved to db by id'
		assert tt.json_prop == u'\u2018abcd\u2019', 'Fetched JSONProperty with a list should match original'

	def test_int_value(self):
		'''Testing setting JSONProperty to an int'''
		t = JSONModel()
		t.json_prop = 735
		assert t.json_prop == 735, 'JSONProperty field should return underlying object'
		t.put()
		time.sleep(3)
		id = t.id
		tt = JSONModel.get_by_id(id)
		assert tt is not None, 'Should be able to fetch objects saved to db by id'
		assert tt.json_prop == 735, 'Fetched JSONProperty with an int should match original'
		t.json_prop = -123456
		t.put()
		time.sleep(3)
		tt = JSONModel.get_by_id(id)
		assert tt is not None, 'Should be able to fetch objects saved to db by id'
		assert tt.json_prop == -123456, 'Fetched JSONProperty with an int should match original'

	def test_list_value(self):
		'''Testing setting JSONProperty to a list'''
		t = JSONModel()
		t.json_prop = [5, 4, 1, 3, 2]
		assert isinstance(t.json_prop, list), 'JSONProperty field should return underlying object'
		assert t.json_prop == [5, 4, 1, 3, 2], 'JSONProperty field should return underlying object'
		t.json_prop.append(7)
		assert t.json_prop == [5, 4, 1, 3, 2, 7], 'JSONProperty field set to a list should support append'
		value = []
		for v in t.json_prop:
			value.append(v)
		assert value == [5, 4, 1, 3, 2, 7], 'JSONProperty object set to a list must be iterable'
		t.put()
		time.sleep(3)
		id = t.id
		tt = JSONModel.get_by_id(id)
		assert tt is not None, 'Should be able to fetch objects saved to db by id'
		assert tt.json_prop == [5, 4, 1, 3, 2, 7], 'Fetched JSONProperty with a list should match original'

	def test_dict_value(self):
		'''Testing setting JSONProperty to a dict'''
		t = JSONModel()
		t.json_prop = {
			'one': 1,
			'two': 2,
		}
		assert isinstance(t.json_prop, dict), 'JSONProperty field should return underlying object'
		assert t.json_prop == dict(one=1, two=2), 'JSONProperty field should return underlying object'
		t.json_prop['three'] = 3
		assert t.json_prop == dict(one=1, two=2, three=3), 'JSONProperty field set to a dict should support assigning to a new key'
		try:
			assert t.json_prop.has_key('one'), 'JSONProperty field set to a dict should support'
		except AttributeError:
			assert False, 'JSONProperty field set to a dict should support has_key'
		assert 'two' in t.json_prop, 'JSONProperty field set to a dict should support membership check'
		keys = []
		values = []
		for k in t.json_prop:
			values.append(t.json_prop[k])
			keys.append(k)
		assert set(keys) == set(['one', 'two', 'three']), 'JSONProperty field set to a dict must be iteration'
		assert set(values) == set([1, 2, 3]), 'JSONProperty object set to a list must be iterable'
		t.json_prop['complex_value'] = {
			'key1': [1, 2, 3, 4],
			'key2': '53'
		}
		t.put()
		time.sleep(3)
		id = t.id
		tt = JSONModel.get_by_id(id)
		assert tt is not None, 'Should be able to fetch objects saved to db by id'
		assert tt.json_prop == dict(one=1, two=2, three=3, complex_value=dict(key1=[1, 2, 3, 4], key2='53')), 'Fetched JSONProperty with a dict should match original'
