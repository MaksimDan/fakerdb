from fakerdb import generate
from test.resources import sample1


def test_generate_csv():
	generated_tables = generate.generate_csv(sample1.schema, None)

	# ensure all tables are generated
	assert sorted(sample1.schema.get_all_table_names()) == sorted(list(generated_tables.keys()))

	# ensure that each table has the expected number of rows
	assert sample1.schema.get_table_quantity('contacts_contact') == generated_tables['contacts_contact'].shape[0]
	assert sample1.schema.get_table_quantity('goals_goal') == generated_tables['goals_goal'].shape[0]
	assert sample1.schema.get_table_quantity('users_user') == generated_tables['users_user'].shape[0]

	# ensure that the all the columns exists
	assert sorted(sample1.schema.get_table_field_names('contacts_contact')) == sorted(list(generated_tables['contacts_contact'].columns))
	assert sorted(sample1.schema.get_table_field_names('goals_goal')) == sorted(list(generated_tables['goals_goal'].columns))
	assert sorted(sample1.schema.get_table_field_names('users_user')) == sorted(list(generated_tables['users_user'].columns))
