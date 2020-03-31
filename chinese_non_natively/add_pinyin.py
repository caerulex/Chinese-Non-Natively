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
dir_path = os.path.abspath(os.path.dirname(sys.argv[0]))
font = ImageFont.truetype(dir_path + "/fonts/UbuntuMono-R.ttf", 100)
chinese_font = ImageFont.truetype(dir_path + "/fonts/NotoSansCJK-Regular.ttc", 210)
chinese_width = chinese_font.getsize("得")[0]
char_width = font.getsize(" ")[0]

def stretch_width_english_text(pinyin_word):
	pinyin_word_width = char_width*len(pinyin_word)
	while pinyin_word_width <= chinese_width:
		pinyin_word = " " + pinyin_word
		pinyin_word_width += char_width
		if pinyin_word_width <= chinese_width:
			pinyin_word = pinyin_word + " "
			pinyin_word_width += char_width
	return pinyin_word

def is_chinese_char(char):
	return 0x4e00 <= ord(char) <= 0x9fff

def filter_newline(line):
	line = (re.sub('\n', '<br>', line[0]), line[1], line[2], line[3])
	return line

def split_phrases(phrase):
	grouped_phrase = []
	for k, g in groupby(phrase, itemgetter(2)):
		#print("list",list(g),"key",k)
		grouped_phrase.append(list(g))
	return grouped_phrase

def add_span(phrase):
	chinese, ispinyin, pinyin = phrase
	return '<span class="pinyin"><span>' + "".join(pinyin) + "</span>" + "".join(chinese) + "</span>"

def group_phrases(phrase):
	final_phrase = ""
	if not phrase[0][1]:
		chn, tru, pin = zip(*phrase)
		final_phrase += "".join(chn)
	elif len(phrase) > 12:
		final_phrase += add_span(list(zip(*phrase[:12])))
		final_phrase += add_span(list(zip(*phrase[12:])))
	else:
		final_phrase += add_span(list(zip(*phrase)))
	return final_phrase

def group_and_format(phrases):
	pool = ThreadPool()
	split_text = split_phrases(phrases)
	final_phrases = pool.map(group_phrases, split_text)
	pool.close()
	pool.join()
	return "".join(final_phrases)

def apply_pinyin(chn):
	return pinyin(chn)[0][0] + " "


def add_pinyin(text):

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
	grouped_phrases = group_and_format(list(np.array(phrases)))
	toc = time.perf_counter()
	print(f"grouped phrases in {toc - tic:0.4f} seconds\n{'-'*50}\n")

	return grouped_phrases
