import argparse
from chinese_non_natively.find_replace_chinese import ChineseLanguageAssistantReader
from chinese_non_natively.export_html_and_browse import browseLocal

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--hide_pinyin', help='hide all pinyin above text', action="store_true")
	parser.add_argument('--hide_vocab', help='hide vocab below text', action="store_true")
	parser.add_argument('--hide_non_vocab_pinyin', help='hide pinyin, except above vocab', action="store_true")
	parser.add_argument('--theme', help='either "pink", "teal", or a custom rgb color "###,###,###" i.e. "125,125,125"', default="pink")
	args = parser.parse_args()

	pink = '153, 0, 17'
	teal = '0, 135, 153'

	SHOW_PINYIN, SHOW_VOCAB, PINYIN_ONLY_ON_DEFINITIONS, THEME = True, True, False, pink
	if args.hide_pinyin:
		SHOW_PINYIN = False
	if args.hide_vocab:
		SHOW_VOCAB = False
	if args.hide_non_vocab_pinyin:
		PINYIN_ONLY_ON_DEFINITIONS = True
	if args.theme is not None:
		if args.theme == "pink":
			THEME=pink
		elif args.theme == "teal":
			THEME=teal
		else:
			THEME=args.theme
			print('using custom color ', THEME)
	
	reader = ChineseLanguageAssistantReader(raw_chinese_files_dir = 'raw_chinese_files')
	reader.load_dict('chinese_non_natively/vocab.csv')
	text = reader.wrap_raw_text_with_english_and_pinyin(show_pinyin=SHOW_PINYIN,
														show_definitions=SHOW_VOCAB,
														hide_non_vocab_pinyin=PINYIN_ONLY_ON_DEFINITIONS,
														theme=THEME)
	browseLocal(text)

if __name__ == "__main__":
	main()
	