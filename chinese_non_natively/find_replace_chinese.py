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
load_phrases_dict(pinyin_exceptions)
base_font_size = 40
english_scaling = 0.4
pink = '153, 0, 17'

font = ImageFont.truetype(\
	"fonts/DejaVuSans.ttf",\
	 int(base_font_size * english_scaling))
chinese_font = ImageFont.truetype(\
	"fonts/NotoSansCJK-Regular.ttc",\
	 base_font_size)

class ChineseLanguageAssistantReader():

	def __init__(self, raw_chinese_files_dir = '../raw_chinese_files'):
		self.mapping_dict = dict()
		self.raw_chinese_files_dir = raw_chinese_files_dir

	def calculate_width_chinese(self, text):
		return chinese_font.getsize(text)[0]

	def load_dict(self, chinese_english_dict_name):
		with open(chinese_english_dict_name, newline='') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if len(row) > 1:
					chn = row[0]
					eng = row[1]
					chinese_width = self.calculate_width_chinese(chn)
					self.mapping_dict.update({chn:'<span class="overlay"><span id=english style="width:' + str(chinese_width) + 'px">' \
						+ eng + "</span>" + chn + "</span>"})

	def calculate_num_spaces(self, text):
		text_no_space = list(filter(str.strip, list(text)))
		num_spaces = len(list(text)) - len(text_no_space)
		return num_spaces

	def stretch_spaces(self, text):
		replacements = 1
		total_space_width = self.calculate_num_spaces(text) * self.space_width
		difference_to_fill_with_whitespace = self.chinese_width - self.english_width

		if total_space_width > 0:
			while difference_to_fill_with_whitespace > 0:
				difference_to_fill_with_whitespace -= total_space_width
				replacements += 1
			text = re.sub(' ', ' ' * (replacements+1), text)
		return text

	def stretch_width_english_text(self, text):
		self.english_width = font.getsize(text)[0]
		self.space_width = font.getsize(" ")[0]
		text = self.stretch_spaces(text)
		return re.sub(' ', '&nbsp', text)

	def process_phrase(self, pinyin_text, chinese_text):
		self.chinese_width = self.calculate_width_chinese(chinese_text)
		stretched_pinyin_text = self.stretch_width_english_text(pinyin_text)
		phrase = '<span class="pinyin"><span>' \
			+ stretched_pinyin_text  + "</span>" + chinese_text + "</span>"
		return phrase

	def is_chinese_char(self, char):
		return 0x4e00 <= ord(char) <= 0x9fff

	def find_chinese_phrase(self, text_list, phrase_end_ind):
		phrase_start_ind = phrase_end_ind
		# parse all chinese characters until a non-chinese character appears
		while self.is_chinese_char(text_list[phrase_end_ind]):
			phrase_end_ind += 1
		# skip index i to the end of phrase to avoid re-parsing part of the phrase
		pinyin_text = " ".join(list(itertools.chain.from_iterable(pinyin(text_list[phrase_start_ind:phrase_end_ind]))))
		chinese_text = "".join(text_list[phrase_start_ind:phrase_end_ind])
		phrase_text = self.process_phrase(pinyin_text, chinese_text)
		return phrase_text, phrase_end_ind

	def add_pinyin(self,text):
		text_list = list(text)
		final_text = ""
		i = 0
		while i < len(text_list):
			# if we encounter a chinese character, begin processing
			if self.is_chinese_char(text_list[i]):
				phrase_text, i = self.find_chinese_phrase(text_list, i)
				final_text += phrase_text
			else:
				final_text += str(text_list[i])
				# add a <br> tag in html if there is a new line in the raw text
				if str(text_list[i]) == '\n':
					final_text += '<br>'
				# increment i by 1
				i += 1
		return final_text

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


	def wrap_raw_text_with_english_and_pinyin(self, show_pinyin=True, show_definitions=True, hide_non_vocab_pinyin=False, theme=pink):
		style = get_style(hide_non_vocab_pinyin=hide_non_vocab_pinyin, \
			base_font_size=base_font_size, english_scaling=english_scaling, theme=theme)
		self.text_files = sorted(glob.glob(self.raw_chinese_files_dir + '/*.txt'))
		print("translating: ", self.text_files)
		text = "<a name=top><div id=anchor_0><h1>Chinese Non-Natively</h1>\
				<h2 id=fancy_chinese>让中文浅显易懂</h2></div></a>"
		text += self.add_toc()
		idx = 1
		for file_name in self.text_files:
			file_contents = self.get_file_contents(file_name)
			
			if show_definitions:
				subbed_text, num_subs = self.add_english_definitions(file_contents)
				percent_subbed = num_subs / len(file_contents)
				text += self.add_nav(idx,file_name,percent_subbed)
				text += '\n<div><div class="line-text" id=bg>'
				if show_pinyin:
					text += self.add_pinyin(subbed_text)
				else:
					text += subbed_text
			# if only pinyin, no definitions
			elif show_pinyin:
				text += self.add_nav(idx,file_name)
				text += '\n<div><div class="line-text" id=bg>'
				text += self.add_pinyin(file_contents)
			# neither show pinyin or definitions; raw text
			else:
				text += '<p>' + re.sub('\n', '<br>', file_contents) + '</p>'
			text += '</div></div>'
			idx += 1
		return '<!DOCTYPE html>' + style + header + "\n" + text + footer

