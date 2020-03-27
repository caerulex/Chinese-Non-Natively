# HTML to be injected
header = '<html><body><div id=light_bg>'
footer = '</div></body></html>'
pink = '153, 0, 17'
border_opacity = str(0.2)
drop_shadow = '1px 2px 4px rgba(0, 0, 0, .1)'

def get_style(base_font_size=40, english_scaling=0.4, hide_non_vocab_pinyin=False, theme=pink):
	if hide_non_vocab_pinyin:
		pinyin_non_def_color = 'rgba(255, 255, 255, 0.0)'
	else:
		pinyin_non_def_color = '#900C3F'
	style = "<link href='https://fonts.googleapis.com/css?family=Ma Shan Zheng' rel='stylesheet'>"\
		"<link href='https://fonts.googleapis.com/css?family=Alegreya' rel='stylesheet'>" \
		"<link href='https://fonts.googleapis.com/css?family=Alegreya SC' rel='stylesheet'>" \
		"<link href='https://fonts.googleapis.com/css?family=Alegreya Sans' rel='stylesheet'>" \
		"<link href='https://fonts.googleapis.com/css?family=Alegreya Sans SC' rel='stylesheet'>"
	style += '<style> \
		body { \
			background: rgba(' + theme + ', 0.20);	\
			    width: 100%; \
				height: 100%; \
				margin: 0; \
				padding: 0; \
				overflow-x: hidden; \
		} \
		.button { \
			background-color: white; \
			color: black; \
  			border: 2px solid rgb(' + pink + '); \
			border: none; \
			color: white; \
			padding: 16px 32px; \
			text-align: center; \
			text-decoration: none; \
			display: inline-block; \
			font-size: 16px; \
			margin: 4px 2px; \
			transition-duration: 0.4s; \
			cursor: pointer; \
		} \
		.button:hover { \
			background-color: rgb(' + pink + '); \
			color: white; \
			} \
		div {\
			margin:3%;\
			box-shadow: ' + drop_shadow + '; \
		}\
		h1 { \
			text-align: center;\
			font-family: "Alegreya Sans SC";\
		}\
		#fancy_chinese { \
			font-family: "Ma Shan Zheng";\
			font-size: 180%; \
			font-weight: 1; \
			text-align: center; \
		} \
		#anchor_0 { \
 			border-bottom: 0.5em solid rgba(' + theme + ', ' + border_opacity +'); \
			padding-top: 1%; \
			margin-top: -3%; \
			background-color: #ffffff; \
			box-shadow: ' + drop_shadow + '; \
		}	\
		br { \
			display: block; /* makes it have a width */ \
			content: ""; /* clears default height */ \
			margin-top: 1.5rem; /* change this to whatever height you want it */ \
		} \
		\
		#light_bg { \
			background: rgba(255, 255, 255, 0.75)	\
		} \
		[id^="anchor_"] { \
			margin-top: -0.75%; \
			box-shadow: none; \
		} \
		#chapter_heading { \
			align-items: center; \
			width: 90%; \
			height: 50%; \
			background: #ffffff none repeat scroll 0 0; \
			border-top:0.5em solid rgba(' + theme + ', ' + border_opacity +'); \
			display: table; \
			margin-bottom: 1%; \
			margin-left:auto; \
			margin-right:auto;\
			padding-right: 0em; \
			justify-content: center; \
		} \
		#percent_sub { \
			text-align: center;\
			font-family: "Alegreya Sans SC";\
			margin-top: -2.5%; \
			color: rgba(0,0,0,0.6) \
			box-shadow: none; \
		} \
		#nav { \
			font-size: 120%; \
			font-family: "Alegreya Sans SC";\
			line-height: 1;\
			flex-direction: row; \
			justify-content: center; \
			align-items: center; \
			display: flex; \
			margin-bottom: 0.5%; \
			margin-top: 0%; \
			padding-left: 0em; \
			box-shadow: none; \
		} \
		#nav p { \
			margin: 0em; \
		} \
		.line-text {\
			position: relative;\
			font-size: ' + str(base_font_size) + 'px;\
			line-height: 3.0;\
			padding-top: 0.5%; \
			padding-left: 2%; \
			margin-top: 0%; \
			margin-left:auto; \
			margin-right:auto;\
			justify-content: center; \
		}\
		#bg { \
			background-color: #ffffff; \
			z-index: 0; \
		} \
		.overlay {\
			color: rgb(' + pink + ');\
			vertical-align: middle;\
			padding-right: .7rem!important;\
			padding-left: .7rem!important;\
			white-space: pre;\
			z-index: 20 \
		}\
		.pinyin {\
			vertical-align: middle;\
			padding-right: .3rem!important;\
			padding-left: .3rem!important;\
			white-space: pre;\
			z-index: 21; \
		}\
		.overlay #english{\
			text-indent: 0px;\
			-webkit-text-emphasis: none;\
			font-size: ' + str(english_scaling*100) + '%;\
			line-height: 1;\
			text-align: start;\
			color: rgba(20, 20, 160, 1.0);\
			position: absolute;\
			display:initial;\
			padding-left: .4rem!important;\
			padding-top: 5.5rem!important;\
			z-index: -1;\
			user-select: none; \
			text-align:left; \
			white-space: pre-line; \
			font-family: "Alegreya Sans";\
		}\
		.overlay .pinyin span, .pinyin span{\
			text-indent: 0px;\
			-webkit-text-emphasis: none;\
			font-size: ' + str(english_scaling*100) + '%;\
			line-height: 1;\
			text-align: start;\
			position: absolute;\
			display:initial;\
			padding-left: .1rem!important;\
			padding-top: 1.5rem!important;\
			z-index: 1;\
			user-select: none; \
			text-align:justify; \
			white-space: pre; \
			font-family: "DejaVuSans"; \
		}\
		.overlay .pinyin span{\
			color: rgb(100, 62, 70);\
		}\
		.pinyin span{\
			color: ' + pinyin_non_def_color + ';\
		}\
		#toc_container { \
			background: #ffffff none repeat scroll 0 0; \
			border:0.5em solid rgba(' + theme + ', ' + border_opacity +'); \
			display: table; \
			font-size: 120%; \
			margin-bottom: -1%; \
			margin-top: -1%; \
			margin-left:auto; \
			margin-right:auto;\
			padding-right: 2em; \
			justify-content: center; \
			font-family: "Alegreya Sans";\
		} \
		.toc_title { \
			font-weight: 700; \
			text-align: center; \
			padding-left: 2em; \
			font-family: "Alegreya Sans SC";\
		} \
		#toc_container li, #toc_container ul, #toc_container ul li{ \
			list-style: outside none none !important; \
			padding-left: 1em; \
			text-align: center; \
		} \
		a {\
			text-decoration: none;\
		} \
		a:link, a:visited, a:hover, a:active {color: black;} \
		#disabled { \
			color: rgba(0,0,0,0.3); \
			cursor: default; \
		} \
		</style>'
	return style

def get_script():
	script = '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>'
	script += '''<script type="text/javascript">
		$(document).ready(function() {
		});
	</script>'''
	return script
