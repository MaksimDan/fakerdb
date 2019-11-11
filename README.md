# fakerdb

Automatically generate data and fill your database tables with large volumes of test data. Fakerdb is written to be programmable within the context of a testing framework in mind. With fakerdb you can creates a context that can be specifically validated against, end to end.

## features
* Generate unique or optional values
* Foreign key support
* Faker wrapper: which can support fields such as date, time values, emails, domains, ip, user agents, paragraphs, sentences, etc.

## usage

Here is an example of a schema file that defines your database structure.

```python
from schema import Field
from schema import Schema
from schema import ForeignKeyType
from test.resources.provider1 import Provider

_TABLE_USER = 'users_user'
_TABLE_CONTACT = 'contacts_contact'
_TABLE_GOALS = 'goals_goal'
_faker_senpai = Provider.get_faker()

# note that the ordering of the fields are crucial. they must align with the order of the columns in the database
_schema = {
	_TABLE_USER: {
		'fields': [
			Field('id', _faker_senpai.unique_integer, offset=99999),
			Field('password', _faker_senpai.password, length=10),
			Field('last_login', _faker_senpai.date),
			Field('is_superuser', _faker_senpai.boolean),
			Field('email', _faker_senpai.email),
			Field('first_name', _faker_senpai.first_name),
			Field('last_name', _faker_senpai.last_name),
			Field('avatar', _faker_senpai.fixed_random_string, length=100),
			Field('token', _faker_senpai.uuid4),
			Field('is_admin', _faker_senpai.boolean),
			Field('is_active', _faker_senpai.boolean),
			Field('is_staff', _faker_senpai.boolean),
			Field('registered_at', _faker_senpai.date)
		],
		'quantity': 100
	},
	_TABLE_CONTACT: {
		'fields': [
			Field('id', _faker_senpai.unique_integer, offset=999999),
			Field('message', _faker_senpai.text_without, max_nb_chars=100, ignore_characters=[',', '\n']),
			Field('sent_at', _faker_senpai.date),
			Field('user_id', None, foreign_key=f'{_TABLE_USER}.id', foreign_key_type=ForeignKeyType.ONE_TO_ONE),
		],
		'quantity': 100
	},
	_TABLE_GOALS: {
		'fields': [
			Field('id', _faker_senpai.unique_integer, offset=999999),
			Field('kind', _faker_senpai.random_choice,
			      elements=['weight_loss', 'run_faster', 'run_further', 'build_strength', 'reduce_stress', 'other']),
			Field('data_point', _faker_senpai.random_int),
			Field('sent_at', _faker_senpai.date_between, start_time='2 days ago', end_time='today',
			      time_format='{0:%Y-%m-%d %H:%M:%S}'),
			Field('user_id', None, foreign_key=f'{_TABLE_USER}.id', foreign_key_type=ForeignKeyType.ONE_TO_MANY),
		],
		'quantity': 1000
	}
}

schema = Schema(_schema)

```

You can define any custom function that generates the data point. In my case, I used faker's provider base class to wrap additional functionality that I need.

To generate the data, you can either write it to file, or expect a dictionary of dataframes.

```python
import generate
from test.resources import sample1


def test_generate_csv():
	generated_tables = generate.generate_csv(sample1.schema, None)

def test_generate_csv2():
	generate.generate_csv(sample1.schema, 'my/path/to/write')
```