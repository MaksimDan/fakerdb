from fakerdb._graph import GraphTools
from enum import Enum


class ForeignKeyType(Enum):
	ONE_TO_ONE = 'one-to-one'
	ONE_TO_MANY = 'one-to-many'


class ForeignKey:
	def __init__(self, table_name_field_name):
		"""
		obj: conventionally split foreign key by its table and field name
		ex. table_name.field_name
		:param table_name_field_name:
		"""
		split = table_name_field_name.split('.')
		if len(split) != 2:
			raise ValueError('Expected the table and field name to be split by a period. For example, table_name.field_name')
		self.table, self.field = split


class Field:
	_FOREIGN_KEY = 'foreign_key'
	_FOREIGN_KEY_TYPE = 'foreign_key_type'

	def __init__(self, name, func, **params):
		self.name = name
		self.func = func
		self.params = params

		has_foreign_key = Field._FOREIGN_KEY in self.params and Field._FOREIGN_KEY_TYPE in self.params
		if has_foreign_key:
			self.foreign_key, self.foreign_key_type = ForeignKey(self.params.pop(Field._FOREIGN_KEY)), self.params.pop(
				Field._FOREIGN_KEY_TYPE)
		else:
			self.foreign_key, self.foreign_key_type = None, None


class Schema:
	_FIELDS = 'fields'
	_QUANTITY = 'quantity'

	def __init__(self, schema):
		self.schema = schema

	def get_table_build_order(self):
		deps = []
		for table_name in self.get_all_table_names():
			for field in self.get_table_fields(table_name):
				if field.foreign_key is not None:
					deps.append([table_name, field.foreign_key.table])
		return GraphTools.top_sort(deps, self.get_all_table_names())

	def get_all_table_names(self):
		return self.schema.keys()

	def get_table(self, table_name):
		if table_name not in self.get_all_table_names():
			raise KeyError(f'{table_name} was not found in the schema.')
		return self.schema[table_name]

	def get_table_fields(self, table_name):
		return self.get_table(table_name)[Schema._FIELDS]

	def get_table_field_names(self, table_name):
		all_fields = self.get_table_fields(table_name)
		return [f.name for f in all_fields]

	def get_table_quantity(self, table_name):
		return self.get_table(table_name)[Schema._QUANTITY]
