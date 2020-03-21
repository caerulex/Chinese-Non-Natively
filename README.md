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

## Usage
### Simple html file
To simply create an html file and open the file in the browser,

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
