# - *- coding: utf- 8 - *-
import re
import csv
import os
import glob
from pypinyin import pinyin, load_phrases_dict
import itertools
from PIL import ImageFont
from html_definitions import header, footer, get_style, get_script
from pinyin_exceptions import exceptions as pinyin_exceptions
import time
from add_pinyin import add_pinyin
load_phrases_dict(pinyin_exceptions)
base_font_size = round(40 / 12)*12 #36
english_scaling = 0.4 #14
pink = '153, 0, 17'

dir_path = os.path.dirname(__file__)
font = ImageFont.truetype(dir_path + "/fonts/Times_New_Roman.ttf", 100)
chinese_font = ImageFont.truetype(dir_path + "/fonts/NotoSansCJK-Regular.ttc", 250)

class ChineseLanguageAssistantReader():

	def __init__(self, raw_chinese_files_dir = '../raw_chinese_files'):
		self.mapping_dict = dict()
		self.raw_chinese_files_dir = raw_chinese_files_dir

	def calculate_width_chinese(self, text):
		#return len(text)*60
		return chinese_font.getsize(text)[0]

	def load_dict(self, chinese_english_dict_name):
		with open(chinese_english_dict_name, newline='') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if len(row) > 1:
					chn = row[0]
					eng = row[1]
					chinese_width = len(chn)*base_font_size
					self.mapping_dict.update({chn:'<span class="overlay"><span id=english style="width:' + str(chinese_width) + 'px">' \
						+ eng + "</span>" + chn + "</span>"})

	def add_english_definitions(self, text):
		pattern = re.compile(r'|'.join(re.escape(key) for key in self.mapping_dict.keys()))
		result, num_subs = pattern.subn(lambda x: self.mapping_dict[x.group()], text)
		return result, num_subs

	def get_file_contents(self, file_name):
		file_contents = ""
		try:
			with open(file_name) as f: # No need to specify 'r': this is the default.
				file_contents = f.read()
		except:
			print("Could not open file ", file_name)
		return file_contents

	def add_toc(self):
		text = '<div id="toc_container"><p class="toc_title">Table of Contents</p><ul class="toc_list">'
		idx = 1
		for file_name in self.text_files:
			text += '<li><a href=#anchor_' + str(idx) + '>' + \
				os.path.splitext(os.path.basename(file_name))[0] + '</a></li>'
			idx +=1
		text += '</ul></div>'
		return text

	def add_nav(self, idx, file_name, percent_subbed=0):
		text = '<div id=chapter_heading>'
		# add file title
		text += '<div id=anchor_' + str(idx) + '><h1>' + \
				os.path.splitext(os.path.basename(file_name))[0] + \
				'</h1></div>'
		# add % substitutions
		text += "<p id=percent_sub>" + str('{0:.2f}'.format(percent_subbed*100)) + "% of file covered by vocab file.</p>"
		# add navigation to previous, top, and next
		if idx == 1:
			text += '<div id=nav>\
					<p id="disabled">[prev]</p> \
					<a href=#top>[top]</a> \
					<a href=#anchor_' + str(idx+1) + ' id="next">[next]</a></div>'
		elif idx == len(self.text_files):
			text += '<div id=nav>\
					<a href=#anchor_' + str(idx-1) + ' id="prev">[prev]</a> \
					<a href=#top>[top]</a> \
					<p id="disabled">[next]</a></p></div>'
		else:
			text += '<div id=nav>\
					<a href=#anchor_' + str(idx-1) + ' id="prev">[prev]</a> \
					<a href=#top>[top]</a> \
					<a href=#anchor_' + str(idx+1) + ' id="next">[next]</a></div>'
		text += '&nbsp</div>'
		return text


	def wrap_raw_text_with_english_and_pinyin(self, show_pinyin=True, show_definitions=True, hide_non_vocab_pinyin=False):
		self.text_files = sorted(glob.glob(self.raw_chinese_files_dir + '/*.txt'))
		print("translating: ", self.text_files)
		text = self.add_toc()
		idx = 1
		for file_name in self.text_files:
			file_contents = self.get_file_contents(file_name)
			
			if show_definitions:
				tic = time.perf_counter()
				subbed_text, num_subs = self.add_english_definitions(file_contents)
				toc = time.perf_counter()
				print(f"subbed vocab in {toc - tic:0.4f} seconds")
				percent_subbed = num_subs / len(file_contents)
				text += self.add_nav(idx,file_name,percent_subbed)
				text += '\n<div><div class="line-text" id=bg>'
				if show_pinyin:
					tic = time.perf_counter()
					text += add_pinyin(subbed_text)
					toc = time.perf_counter()
					print(f"added pinyin in {toc - tic:0.4f} seconds")
				else:
					text += subbed_text
			# if only pinyin, no definitions
			elif show_pinyin:
				tic = time.perf_counter()
				text += self.add_nav(idx,file_name)
				text += '\n<div><div class="line-text" id=bg>'
				text += add_pinyin(file_contents)
				toc = time.perf_counter()
				print(f"added pinyin in {toc - tic:0.4f} seconds")
			# neither show pinyin or definitions; raw text
			else:
				text += '<p>' + re.sub('\n', '<br>', file_contents) + '</p>'
			text += '</div></div>'
			idx += 1
		return text

	def wrap_raw_text(self, show_pinyin=True, show_definitions=True, hide_non_vocab_pinyin=False, theme=pink):
		style = get_style(hide_non_vocab_pinyin=hide_non_vocab_pinyin, \
			base_font_size=base_font_size, english_scaling=english_scaling, theme=theme)
		page_header = "<a name=top><div id=anchor_0><h1>Chinese Non-Natively</h1>\
				<h2 id=fancy_chinese>让中文浅显易懂</h2></div></a>"
		text = self.wrap_raw_text_with_english_and_pinyin(show_pinyin=show_pinyin, \
			show_definitions=show_definitions, hide_non_vocab_pinyin=hide_non_vocab_pinyin)
		return  '<!DOCTYPE html>' + style + header + "\n" + page_header + text + footer

