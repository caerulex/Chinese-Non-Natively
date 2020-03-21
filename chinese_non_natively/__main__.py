from chinese_non_natively.find_replace_chinese import ChineseLanguageAssistantReader
from chinese_non_natively.export_html_and_browse import browseLocal

def main():
	reader = ChineseLanguageAssistantReader(raw_chinese_files_dir = 'raw_chinese_files')
	reader.load_dict('chinese_non_natively/chinese_english_dict.csv')
	text = reader.wrap_raw_text_with_english_and_pinyin(show_pinyin=True, show_definitions=True)
	browseLocal(text)

if __name__ == "__main__":
	main()
	