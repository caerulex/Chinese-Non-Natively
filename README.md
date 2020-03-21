# Chinese Non-Natively

# Summary
Have you ever tried reading Chinese?
If you're a non-native to the language, it can be difficult to read quickly.

Adding in pinyin can be very useful to help bootstrap novices.

Additionally, the option to create dictionary mappings (i.e. flashcards) that can be
overlayed beneath Chinese characters is also useful for novices and experts alike (great for proper nouns and idioms).

In general, this application is geared toward people who have some knowledge of Mandarin Chinese, 
and are looking to read raw Chinese texts with pinyin and (optionally) a flashcard-like definition overlay.

# Usage
## Setup
### Python
To download required python packages, use the command:

`make requirements`

### Dictionary Definitions
Dictionary definition mappings (currently, Chinese --> English) are in `find_replace_chinese/chinese_english_dict.csv`
Modify this file at will. You don't need to provide an English translation; the Chinese characters can be mapped to anything.

### Pinyin Exceptions
If you don't like a certain character's pinyin mapping, you can edit the `find_replace_chinese/pinyin_exceptions.py`
`exceptions` dictionary following this format:
```
{
'character': [['desired_pinyin']],
}
```

i.e.

```
{
    '得': [['de|děi']],
}
```

### Raw Chinese text files
Copy and paste the Chinese text into a text file in the `raw_chinese_files` folder.

You can place multiple files in this folder; the program will output translations for all of the provided files in one webpage.

### Pinyin and Vocab Display Options

There are 3 options for displaying pinyin:

1. No pinyin
2. Pinyin only above vocab
3. Pinyin above all characters

There are only 2 options for displaying vocab:

1. Show vocab
2. Hide vocab

These are controlled by args into the python program.

Control these args using the makefile:

`make generate ARGS="[--hide_pinyin|--hide_vocab|hide_non_vocab_pinyin]"`

i.e., to disable pinyin and vocab (so just display unmodified raw text):

`make generate ARGS="--hide_pinyin --hide_vocab]"`

Alternatively, calling python directly, you can use the command:

`python -m chinese_non_natively --help` to see arguments along with descriptions.

Note: hiding all pinyin removes pinyin completely from output; however, hiding non vocab pinyin mutes pinyin above non-vocab words by turning its font color to white. This makes it easy to highlight a character and see its associated pinyin.

#### The reason for this design choice:

People with an intermediate knowledge of chinese may find that pinyin displayed above all words can be distracting. It's possible that they would like to see pinyin only over unknown vocab words. At the same time, they might still wish to have the option to see the pinyin of a non-vocab word.

Note: Vocab definitions and pinyin are set to be un-selectable/un-highlightable. This is because selecting text with highlighting enabled for vocab, pinyin, and Chinese characters results in a jumbled output. With highlighting of pinyin and vocab disabled, users can easily copy lines of Chinese text without issue.

## Usage
### Simple html file
To simply create an html file and open the file in the browser using default settings
(showing pinyin above all characters, and showing all vocab):

`make generate`

is sufficient.

### Webpage Serving w/ nginx
To dispay the html file w/ nginx:
(this enables the use of [Zhongwen: Chinese Popup Dictionary](https://chrome.google.com/webstore/detail/zhongwen-chinese-english/kkmlkkjojmombglmlpbpapmhcaljjkde), an amazing tool)

...you can use an nginx docker container.

Make sure docker is installed on the system, and that your user has been added to the docker group.
Then, run:

`make build`

`make run`

Then, open to `localhost:8081`
If you would like to use different ports for listening/displaying:

#### listening:

modify the `default.conf` and the Makefile `run` command

#### displaying:

modify the Makefile `run` command
