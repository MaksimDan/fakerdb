from os.path import join
from random import randrange
from fakerdb.schema import ForeignKeyType
import pandas as pd


def generate_csv(schema, out=None):
	"""
	obj: generate csv tables `out`, authored by a faker `schema`
	"""
	# define build order with topological sorting on table foreign key
	table_build_order = schema.get_table_build_order()

	# store previously written tables into memory, for foreign key reference
	previously_built_tables = {}

	for table_name in table_build_order:
		foreign_index = 0
		table_quantity = schema.get_table_quantity(table_name)
		rows = []

		for i in range(table_quantity):
			row = {}
			for field in schema.get_table_fields(table_name):

				# field can be independently generated
				if field.foreign_key is None:
					row[field.name] = field.func(**field.params)

				# field is dependent on another table
				else:
					# one to one mappings are a simple reference copy
					if field.foreign_key_type == ForeignKeyType.ONE_TO_ONE:
						row[field.name] = previously_built_tables[field.foreign_key.table][field.foreign_key.field][foreign_index]
						foreign_index += 1
					# one to many mappings will randomly pick a mapping
					elif field.foreign_key_type == ForeignKeyType.ONE_TO_MANY:
						foreign_dataframe = previously_built_tables[field.foreign_key.table]
						row[field.name] = foreign_dataframe[field.foreign_key.field][randrange(0, len(foreign_dataframe))]
				if not row:
					print(f'Unable to author row {i} for {field.name}.')
			rows.append(row)

		previously_built_tables[table_name] = pd.DataFrame(rows)

	# write the data to disk is needed
	if out:
		for table_name, df in previously_built_tables.items():
			full_name_out = join(out, table_name + '.csv')
			df.to_csv(full_name_out, index=False)

	return previously_built_tables
