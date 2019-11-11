from test.resources import sample1


def test_get_all_table_names():
	expected = ['users_user', 'contacts_contact', 'goals_goal']
	assert expected == list(sample1.schema.get_all_table_names())


def test_get_table_fields():
	expected = ['id', 'kind', 'data_point', 'sent_at', 'user_id']
	assert expected == [f.name for f in sample1.schema.get_table_fields('goals_goal')]


def test_get_table():
	expected = ['id', 'kind', 'data_point', 'sent_at', 'user_id']
	got = [f.name for f in sample1.schema.get_table('goals_goal')['fields']]
	assert expected == got


def test_get_table_quantity():
	expected = 100
	assert expected == sample1.schema.get_table_quantity('contacts_contact')


def test_get_table_fields_names():
	expected = ['id', 'password', 'last_login', 'is_superuser', 'email', 'first_name', 'last_name', 'avatar', 'token', 'is_admin', 'is_active', 'is_staff', 'registered_at']
	assert expected == sample1.schema.get_table_field_names('users_user')


def test_get_table_build_order():
	# note two possible build orders
	expected1 = ['users_user', 'goals_goal', 'contacts_contact']
	expected2 = ['users_user', 'contacts_contact', 'goals_goal']
	out = sample1.schema.get_table_build_order()
	assert expected1 == out or expected2 == out

