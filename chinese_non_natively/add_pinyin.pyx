# - *- coding: utf- 8 - *-
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
load_phrases_dict(pinyin_exceptions)
base_font_size = round(40 / 12)*12 #36
english_scaling = 0.4 #14
pink = '153, 0, 17'

#dir_path = os.path.dirname(__file__)
dir_path = os.path.abspath(os.path.dirname(sys.argv[0]))
print (dir_path)

font = ImageFont.truetype(dir_path + "/fonts/Times_New_Roman.ttf", 100)
chinese_font = ImageFont.truetype(dir_path + "/fonts/NotoSansCJK-Regular.ttc", 250)

cdef int space_width = font.getsize(" ")[0]

cpdef int calculate_width_chinese(str text):
    #return len(text)*60
    return chinese_font.getsize(text)[0]

cpdef int calculate_num_spaces(str text):
    cdef str text_no_space = list(filter(str.strip, list(text)))
    cdef int num_spaces = len(list(text)) - len(text_no_space)
    return num_spaces

cpdef str stretch_char_space(str pinyin_preceding, str pinyin_word, int chinese_preceding_width):
    #print('preceeding: ', " ".join(pinyin_preceding), pinyin_word, chinese_preceding_width)
    #print(self.space_width)
    cdef int current_pinyin_width = font.getsize(pinyin_preceding)[0]
    cdef int pinyin_word_width = font.getsize(pinyin_word)[0]
    #print("init widths: ", current_pinyin_width, chinese_preceding_width)
    #i = 0
    cdef int difference = chinese_preceding_width - current_pinyin_width
    pinyin_word = " " * round(difference / space_width) + " " + pinyin_word
    #while current_pinyin_width <= chinese_preceding_width:
    #	pinyin_word = " " + pinyin_word
    #	current_pinyin_width += self.space_width
    #	i += 1
        
    if pinyin_word_width >= 208:
        #print('<= 208: ',pinyin_word, pinyin_word_width)
        pinyin_word = pinyin_word[1:]
    elif pinyin_word_width < 123:
        #print('< 123: ',pinyin_word, pinyin_word_width)
        pinyin_word = "  " + pinyin_word
    elif pinyin_word_width >= 123 and pinyin_word_width < 158:
        #print('123 <= x < 158: ',pinyin_word, pinyin_word_width)
        pinyin_word = " " + pinyin_word
    elif pinyin_word_width >= 158 and pinyin_word_width < 208:
        #print('158 <= x < 208: ',pinyin_word, pinyin_word_width)
        pinyin_word = "" + pinyin_word
    return pinyin_preceding + pinyin_word

cpdef str stretch_width_english_text_old(str pinyin_text, str chinese_text):
    cdef list splityin = pinyin_text.split(" ")
    cdef str stretched_pinyin = ""
    cdef int i
    for i in range(len(chinese_text)):
        chinese_preceding_width = calculate_width_chinese(chinese_text[:i])
        #print('preceeding: ', " ".join(splityin[:i]), splityin[i], i)
        stretched_pinyin = stretch_char_space(stretched_pinyin, splityin[i], chinese_preceding_width)
    return stretched_pinyin

cpdef str process_phrase_old(str pinyin_text, str chinese_text):
    cdef str stretched_pinyin_text = stretch_width_english_text(pinyin_text, chinese_text)
    stretched_pinyin_text = re.sub(' ', '&nbsp', stretched_pinyin_text)

    cdef str phrase = '<span class="pinyin"><span>' \
        + stretched_pinyin_text  + "</span>" + chinese_text + "</span>"
    return phrase

cpdef str stretch_width_english_text(str pinyin_text, str chinese_text):
    cdef list splityin = pinyin_text.split(" ")
    cdef str stretched_pinyin = ""
    cdef int i
    #print('len chinese to parse:',len(chinese_text), chinese_text)
    pool = ThreadPool()
    pool.map( 8-=)
    for i in range(len(chinese_text)):
        chinese_preceding_width = calculate_width_chinese(chinese_text[:i])
        #print('preceeding: ', " ".join(splityin[:i]), splityin[i], i)
        stretched_pinyin = stretch_char_space(stretched_pinyin, splityin[i], chinese_preceding_width)
    return stretched_pinyin

cpdef list unzip(list phrases):
    # using list comprehension to 
    # perform Unzipping 
    #print('phrases: ',phrases, len(phrases))
    cdef list res = list(zip(*phrases))
    #print(res)
    return res

cpdef tuple process_phrase(list phrases):
    # phrases: pinyin, chinese, ind
    phrases = unzip(phrases)
    #print('process phrase: ',phrases)
    cdef str chinese_phrase = "".join(list(phrases[0]))
    cdef str pinyin_phrase = " ".join(list(phrases[1]))
    cdef str stretched_pinyin_text = stretch_width_english_text(pinyin_phrase,chinese_phrase)
    stretched_pinyin_text = re.sub(' ', '&nbsp', stretched_pinyin_text)

    cdef str phrase = '<span class="pinyin"><span>' \
        + stretched_pinyin_text + "</span>" + chinese_phrase + "</span>"
    #print('phrase: ', phrase)
    #print('zip list: ', list(zip([phrase],[phrases[2]])))
    return tuple(zip([phrase],[phrases[2]]))

cpdef bool is_chinese_char(str char):
    return 0x4e00 <= ord(char) <= 0x9fff

cpdef bool sort_key_true(tuple s):
    #print(s, s[3])
    return s[3] == True

cpdef bool sort_key_false(tuple s):
    return s[3] == False

cpdef tuple filter_newline(tuple line):
    #print(line[0], type(line[0]))
    line = (re.sub('\n', '<br>', line[0]), line[1], line[2], line[3])
    return line

cpdef list split_mega(list mega):
    cdef list grouped_mega = []
    for k, g in groupby(mega, itemgetter(3)):
        grouped_mega.append(list(g))
    #print(grouped_mega)
    return grouped_mega

cpdef tuple strip_extra_col_all(tuple final):
    return (final[0], final[1][0], final[2], final[3])

cpdef list parse_phrases(list text_list):
    pool = ThreadPool()
    cdef list chinese_char_bool_map = pool.map(is_chinese_char, text_list)
    cdef list mega = list(zip(text_list,pinyin(text_list),range(len(text_list)),chinese_char_bool_map))
    chinese_mega = list(filter(sort_key_true,mega))
    mega = pool.map(strip_extra_col_all, mega)
    megas = split_mega(mega)
    
    non_chinese_mega = list(filter(sort_key_false,mega))
    non_chinese_mega = pool.map(filter_newline, non_chinese_mega)
    pool.close()
    pool.join()
    return megas

cpdef tuple strip_tuple(tuple final):
    return final[0]

cpdef tuple strip_extra_col(tuple final):
    return (final[0],final[2])

cpdef str add_pinyin(str text):
    cdef list text_list = list(text)
    cdef int i = 0
    cdef str phrase_text
    cdef list phrases = []
    cdef list chinese_mega
    cdef list non_chinese_mega
    tic = time.perf_counter()
    megas  = parse_phrases(text_list)
    #print(chinese_mega[0], non_chinese_mega[0])
    toc = time.perf_counter()
    #print(f"stretched width in {toc - tic:0.4f} seconds")
    pool = ThreadPool()
    cdef list final_phrases = pool.map(process_phrase, megas)
    final_phrases = pool.map(strip_tuple, final_phrases)
    #non_chinese_mega = pool.map(strip_extra_col, non_chinese_mega)
    pool.close()
    pool.join()
    #print('final_phrases: ', final_phrases)

    cdef list final = final_phrases
    #print('type of final: ', final, type(final), np.array(final).shape)
    final_sorted = pd.DataFrame(final).sort_values(by=[1])
    cdef str final_text = "".join(list(final_sorted[0][:]))
    return final_text
