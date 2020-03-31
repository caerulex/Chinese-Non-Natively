# - *- coding: utf- 8 - *-
#!python
#cython: language_level=3
import re
import csv
import os, sys
import glob
from pypinyin import pinyin, load_phrases_dict
import itertools
from PIL import ImageFont
from html_definitions import header, footer, get_style, get_script
from pinyin_exceptions import exceptions as pinyin_exceptions
import time
from cpython cimport bool
from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd
import numpy as np
from itertools import groupby
from operator import itemgetter
import math
import logging
load_phrases_dict(pinyin_exceptions)
base_font_size = round(40 / 12)*12 #36
english_scaling = 0.4 #14
pink = '153, 0, 17'

#Creating an object 
#logger=logging.getLogger() 
  
#Setting the threshold of logger to DEBUG 
#logger.setLevel(logging.DEBUG)

#dir_path = os.path.dirname(__file__)
dir_path = os.path.abspath(os.path.dirname(sys.argv[0]))
print (dir_path)
#logging.error('path for imagefont: ', dir_path + "/fonts/Times_New_Roman.ttf")
font = ImageFont.truetype(dir_path + "/fonts/UbuntuMono-R.ttf", 100)
chinese_font = ImageFont.truetype(dir_path + "/fonts/NotoSansCJK-Regular.ttc", 210)
cdef int chinese_width = chinese_font.getsize("得")[0]
cdef int char_width = font.getsize(" ")[0]

cpdef str stretch_width_english_text(str pinyin_word):
	cdef int pinyin_word_width = char_width*len(pinyin_word)
	while pinyin_word_width <= chinese_width:
		pinyin_word = " " + pinyin_word
		pinyin_word_width += char_width
		if pinyin_word_width <= chinese_width:
			pinyin_word = pinyin_word + " "
			pinyin_word_width += char_width
	return pinyin_word

cpdef bool is_chinese_char(str char):
	return 0x4e00 <= ord(char) <= 0x9fff

cpdef tuple filter_newline(tuple line):
	#print(line[0], type(line[0]))
	line = (re.sub('\n', '<br>', line[0]), line[1], line[2], line[3])
	return line

cpdef list split_phrases(list phrase):
	cdef list grouped_phrase = []
	for k, g in groupby(phrase, itemgetter(2)):
		#print("list",list(g),"key",k)
		grouped_phrase.append(list(g))
	return grouped_phrase

cpdef str add_span(list phrase):
	chinese, ispinyin, pinyin = phrase
	return '<span class="pinyin"><span>' + "".join(pinyin) + "</span>" + "".join(chinese) + "</span>"

cpdef str group_phrases(list phrase):
	cdef str final_phrase = ""
	if not phrase[0][1]:
		chn, tru, pin = zip(*phrase)
		final_phrase += "".join(chn)
	elif len(phrase) > 12:
		final_phrase += add_span(list(zip(*phrase[:12])))
		final_phrase += add_span(list(zip(*phrase[12:])))
	else:
		final_phrase += add_span(list(zip(*phrase)))
	return final_phrase

cpdef str group_and_format(list phrases):
	pool = ThreadPool()
	split_text = split_phrases(phrases)
	cdef list final_phrases = pool.map(group_phrases, split_text)
	pool.close()
	pool.join()
	return "".join(final_phrases)

cpdef str apply_pinyin(str chn):
	return pinyin(chn)[0][0] + " "


cpdef str add_pinyin(str text):

	phrases = pd.DataFrame()
	phrases['chn'] = list(text)

	## parsing
	tic = time.perf_counter()
	phrases['ispinyin'] = phrases.chn.apply(is_chinese_char)
	phrases['pin'] = phrases.chn.apply(apply_pinyin)
	toc = time.perf_counter()
	print(f"\n{'-'*50}\nparsed phrases in {toc - tic:0.4f} seconds")
	
	## stretching width
	tic = time.perf_counter()
	phrases.pin[phrases.ispinyin] = phrases.pin[phrases.ispinyin].apply(stretch_width_english_text)
	toc = time.perf_counter()
	print(f"stretched phrases in {toc - tic:0.4f} seconds")

	## grouping phrases together
	tic = time.perf_counter()
	cdef str grouped_phrases = group_and_format(list(np.array(phrases)))
	toc = time.perf_counter()
	print(f"grouped phrases in {toc - tic:0.4f} seconds\n{'-'*50}\n")

	return grouped_phrases
