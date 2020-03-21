# HTML to be injected
base_font_size = 40
english_scaling = 0.4
header = '<!DOCTYPE html><html><body>'
footer = '</body></html>'

style = '<style> \
div {\
	margin:5%;\
}\
h1 { \
	text-align: center;\
}\
br { \
	display: block; /* makes it have a width */ \
	content: ""; /* clears default height */ \
	margin-top: 1.5rem; /* change this to whatever height you want it */ \
} \
\
.line-text {\
	position: relative;\
	font-size: ' + str(base_font_size) + 'px;\
	line-height: 3;\
}\
\
.overlay {\
color: red;\
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
	color: blue;\
	width: 20%;\
	position: absolute;\
	display:initial;\
	padding-left: .1rem!important;\
	padding-top: 5.5rem!important;\
	z-index: -1;\
	user-select: none; \
	text-align:left; \
	white-space: pre-line; \
}\
.pinyin span{\
  text-indent: 0px;\
	-webkit-text-emphasis: none;\
	font-size: ' + str(english_scaling*100) + '%;\
	line-height: 1;\
	text-align: start;\
	color: #900C3F;\
	position: absolute;\
	display:initial;\
	padding-left: .1rem!important;\
	padding-top: 1.5rem!important;\
	z-index: 1;\
	user-select: none; \
	text-align:justify; \
	white-space: pre; \
}\
</style>'
