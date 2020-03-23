# HTML to be injected
header = '<html><body><div id=light_bg>'
footer = '</div></body></html>'
pink = '153, 0, 17'

def get_style(base_font_size=40, english_scaling=0.4, hide_non_vocab_pinyin=False, theme=pink):
	if hide_non_vocab_pinyin:
		pinyin_non_def_color = 'white'
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
		div {\
			margin:5%;\
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
 			border-bottom: 0.5em solid rgba(' + theme + ', 0.60); \
			padding-top: 1em; \
			margin-top: -3em; \
			background-color: #ffffff; \
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
		hr { \
			overflow: visible; /* For IE */ \
			padding: 0; \
			border: none; \
			text-align: center; \
		} \
		hr:after { \
			content: "🌸🌸🌸🌸🌸🌸🌸"; \
			font-size: ' + str(base_font_size) + 'px;\
			display: inline-block; \
			position: relative; \
			top: -0.7em; \
		} \
		#chapter_heading { \
			align-items: center; \
			width: 90%; \
			height: 50%; \
			background: #ffffff none repeat scroll 0 0; \
			border-top:0.5em solid rgba(' + theme + ', 0.60); \
			//border-bottom:0.5em solid rgba(' + theme + ', 0.60); \
			display: table; \
			margin-bottom: 1em; \
			margin-left:auto; \
			margin-right:auto;\
			padding-right: 0em; \
			justify-content: center; \
		} \
		.line-text {\
			position: relative;\
			font-size: ' + str(base_font_size) + 'px;\
			line-height: 2.5;\
			background-color: #ffffff; \
			padding-top: 0.5em; \
			margin-top: -1em; \
			margin-left:auto; \
			margin-right:auto;\
			justify-content: center; \
		}\
		\
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
			z-index: 21 \
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
			padding-top: 5rem!important;\
			z-index: 22;\
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
			padding-top: 1rem!important;\
			z-index: 1;\
			user-select: none; \
			text-align:justify; \
			white-space: pre; \
			font-family: "Alegreya Sans";\
		}\
		.overlay .pinyin span{\
			color: rgb(100, 62, 70);\
		}\
		.pinyin span{\
			color: ' + pinyin_non_def_color + ';\
		}\
		#toc_container { \
			background: #ffffff none repeat scroll 0 0; \
			border:0.5em solid rgba(' + theme + ', 0.60); \
			display: table; \
			font-size: 120%; \
			margin-bottom: -2em; \
			margin-top: -2em; \
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
		#nav { \
			font-size: 120%; \
			font-family: "Alegreya Sans SC";\
			line-height: 1;\
			flex-direction: row; \
			justify-content: center; \
			align-items: center; \
			display: flex; \
			margin-bottom: -1em; \
			margin-top: -2.5em; \
			padding-left: 0em; \
		} \
		a:link, a:visited, a:hover, a:active {color: black;} \
		#disabled { \
			color: gray; \
			cursor: default; \
		} \
		</style>'
	return style

def get_script():
	script = '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>'
	script += '''<script type="text/javascript">
		$(document).ready(function() {

			// index to reference the next/prev display
			var i = 1;
			// get the total number of display sections
			//    where the ID starts with "anchor_"
			var len = $('div[id^="anchor_"]').length - 1;
			console.log(i)
			console.log(len)

			// for next, increment the index, or reset to 0, and concatenate 
			//    it to "anchor_" and set it as the hash
			$('#next').click(function() {
				console.log(i)
				console.log(i < len)
				if (i < len) {
					i++;
					console.log('i + 1 <= len')
					console.log(i)
				}
				window.location.hash = "anchor_" + i;
				console.log(window.location.hash)
				return false;
			});


			// for prev, if the index is 0, set it to the total length, then decrement
			//    it, concatenate it to "anchor_" and set it as the hash
			$('#prev').click(function() {
				if (i > 0) {
					i--;
				}
				window.location.hash = "anchor_" + i;
				return false;
			});

		});
	</script>'''
	return script
