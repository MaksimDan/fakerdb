import math
import random
import string
from datetime import timedelta
from random import randrange
from typing import List

import dateparser
import faker
from faker.providers import BaseProvider


class Provider(BaseProvider):
	"""
	Define your custom faker operators here
	"""
	SEED = 42
	__unique_integer = 0

	@classmethod
	def get_faker(cls):
		cls.senpai = faker.Faker()
		cls.senpai.seed(Provider.SEED)
		cls.senpai.add_provider(Provider)
		return cls.senpai

	@staticmethod
	def unique_integer(offset=None):
		"""
		obj: return sequence incrementor
		"""
		Provider.__unique_integer += 1
		return Provider.__unique_integer + (offset or 0)

	@staticmethod
	def fixed_random_integer(length):
		"""
		obj: produce an integer with some fixed length
		"""
		return random.randint(math.pow(10, length - 1), math.pow(10, length) - 1)

	@staticmethod
	def fixed_random_string(length, chars=string.ascii_uppercase + string.digits):
		"""
		obj: produce a string with some fixed length
		"""
		return ''.join(random.choice(chars) for _ in range(length))

	def text_without(self, ignore_characters: List = None, **kwargs):
		"""
		obj: wrapper around faker.text but with the additional functionality to ignore some sharacters
		"""
		original_text = self.senpai.text(**kwargs)
		if ignore_characters:
			for c in ignore_characters:
				original_text = original_text.replace(c, '')
		return original_text

	def random_choice(self, **kwargs):
		"""
		obj: returns a single random element in a list
		"""
		original_text = self.senpai.random_choices(**kwargs, length=1)
		if not original_text:
			raise ValueError(f'Expected to have a choice, got {original_text}')
		return original_text[0]

	@staticmethod
	def date_between(start_time, end_time, time_format='{0:%Y-%m-%d %H:%M:%S:%MS}'):
		start_time = dateparser.parse(start_time)
		end_time = dateparser.parse(end_time)

		delta = end_time - start_time
		int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
		random_second = randrange(int_delta)
		random_date_time = start_time + timedelta(seconds=random_second)

		if time_format == 'unix:int':
			return int(random_date_time.timestamp())
		elif time_format == 'unix:float':
			return random_date_time.timestamp()

		return time_format.format(random_date_time)
