from snowballstemmer import RussianStemmer, EnglishStemmer
from langdetect import detect


# --- Utils: models.py --- #

def highlight_basics_of_words(title):
	"""Get basics of words from video's title to improve the search results"""

	punctuation_marks = [
		'.', ',', ';', ':', '...', '?', '!', '—', '~', 
		'`', '+', '=', '-', '<', '>', '/', '\\', '_', 
		'[', ']', '(', ')', '{', '}', '#', '№', '^',
	]

	def is_significant_word(word): # algorithm of filtering is worth updating ^_^
		"""Filter significant words from pronouns and other small words"""
		if len(word) >= 3:
			return word
		else:
			return ''

	def get_basics(stem, c_title):
		'''Get lower-case list of basics'''
		basics = list( # step2 - stemming
			map(stem.stemWord, list( 
					map(is_significant_word, c_title.lower().split()) # step1 - filtering from pronouns
				)
			)
		)
		return list(word for word in basics if word != '')

	cleared_title = title # create "cleared_title" to leave "title" unchanged while iterating
	for symbol in title: # clear data from punctuation marks before *stemming*
		if symbol in punctuation_marks:
			cleared_title = cleared_title.replace(symbol, '')

	if detect(title) == 'en':
		stemmer = EnglishStemmer()
		return get_basics(stemmer, cleared_title)

	elif detect(title) == 'ru':
		stemmer = RussianStemmer()
		return get_basics(stemmer, cleared_title)

	else:
		stemmer = EnglishStemmer()
		return get_basics(stemmer, cleared_title)