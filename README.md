# Dict.cc Dictionary for OS-X

## Preface

This is an updated version of the "input2xml.py dict.cc to Apple Dictionary Plugin Script"
by Philipp Brauner/Lipflip 2008 (lipflip@lipflip.org), licensed under the GPL.

## Requirements
1. Download and Install "Xcode" from the AppStore or https://developer.apple.com/downloads
2. Recursively clone this repository (i.e. "git clone --recursive")
3. Download the utf-8 encoded dictionary tab files from http://www1.dict.cc/translation_file_request.php
4. Rename them to en-de.txt and de-en.txt and move them to this directory

## Build
1. Run make (this takes a while)
2. Run make install (will use over 700MB at ~/Library/Dictionaries)
3. Start Dictionary.app
