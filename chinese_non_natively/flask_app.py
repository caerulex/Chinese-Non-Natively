
# A very simple Flask Hello World app for you to get started with...

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import html_definitions
from find_replace_chinese import base_font_size, english_scaling, pink
show_definitions=True
hide_non_vocab_pinyin=False
theme=pink

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file',
									filename=filename))
	return '''
	<h1>Upload new File</h1>
	<form method=post enctype=multipart/form-data>
	  <input type=file name=file>
	  <input type=submit value=Upload>
	</form>
	'''

@app.route('/', methods=['GET', 'POST'])
def main():
	style = html_definitions.get_style(hide_non_vocab_pinyin=hide_non_vocab_pinyin, base_font_size=base_font_size, english_scaling=english_scaling, theme=theme)
	text = "<a name=top><div id=anchor_0><h1>Chinese Non-Natively</h1><h2 id=fancy_chinese>让中文浅显易懂</h2></div></a>"
	return '<!DOCTYPE html>' + style + html_definitions.header + "\n" + text + upload_file() + html_definitions.footer
	