# - *- coding: utf- 8 - *-
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import random, string
import glob
import shutil
import logging


logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
handler = logging.FileHandler('test.log') # creates handler for the log file
logger.addHandler(handler) # adds handler to the werkzeug WSGI logger

import html_definitions
from find_replace_chinese import ChineseLanguageAssistantReader, base_font_size, english_scaling, pink

show_pinyin=True
pinyin_only_on_defs=True
show_definitions=True
hide_non_vocab_pinyin=False
theme=pink
dir_path = os.path.dirname(__file__)
temp_hash = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
UPLOAD_FOLDER = dir_path +  '/' + temp_hash
ALLOWED_EXTENSIONS = {'txt', 'csv'}

page_head = "<a name=top><div id=anchor_0><h1>Chinese Non-Natively</h1> \
	<h2 id=fancy_chinese>让中文浅显易懂</h2></div></a>"
upload_form = '''
	'<div id="toc_container"><h1>Upload new File</h1><ul class="toc_list">
	<form method=post enctype=multipart/form-data>
	<input type=file multiple="" name="file[]">
	<input type=submit value=Upload>
	</form>'</ul></div>'
	'''
button = '<button name="runButton" onclick="run_button()">Run</button>'
global text
text = ""


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def run_button():
	app.logger.error('run_button proc')
	reader = ChineseLanguageAssistantReader(raw_chinese_files_dir = UPLOAD_FOLDER)
	csv_files = sorted(glob.glob(UPLOAD_FOLDER + '/*.csv'))
	app.logger.error("csv_files: ", csv_files, csv_files[0])
	reader.load_dict(UPLOAD_FOLDER + '/' + csv_files[0])
	global text
	text += reader.wrap_raw_text_with_english_and_pinyin(show_pinyin=show_pinyin,
														show_definitions=show_definitions,
														hide_non_vocab_pinyin=pinyin_only_on_defs)
	print(text[0:20])
	## Try to remove temp folder; if failed show an error using try...except on screen
	try:
		shutil.rmtree(UPLOAD_FOLDER)
	except OSError as e:
		print ("Error: %s - %s." % (e.filename, e.strerror))
	return redirect(request.url)

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
	if request.method == 'POST':
		uploaded_files = request.files.getlist("file[]")
		# check if the post request has the file part
		for f in uploaded_files:
			if f and allowed_file(f.filename):
				filename = secure_filename(f.filename)
				f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		if uploaded_files:
			app.logger.error("run_button")
			run_button()

@app.route('/', methods=['GET', 'POST'])
def main():
	style = html_definitions.get_style(hide_non_vocab_pinyin=hide_non_vocab_pinyin, base_font_size=base_font_size, \
		english_scaling=english_scaling, theme=theme)
	
	return '<!DOCTYPE html>' + style + html_definitions.header + "\n" + \
		page_head + upload_form + button + \
			text  + html_definitions.footer
	