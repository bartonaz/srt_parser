"""Parser of subtitles in SRT format"""

import re
from copy import copy

class SrtParser:
    # Global parameters of the class instance
    MS_POSITION_FACTOR = (int(60*60*1e3), int(60*1000), int(1000), 1)
    CLEANUP_TEXT = True
    # Global parameters of the loop over lines
    INPUT_FILE_NAME = None
    ENTRIES = []
    ENTRY = None

    
    def __init__(self, filename):

        self.INPUT_FILE_NAME = filename
        # Creating precompiled regular expression used by parser
        self.RE_SEP = re.compile(r'^\s*$')
        self.RE_ID = re.compile(r'^\d+$')
        self.RE_TIME = re.compile(r'(\d+):(\d+):(\d+),(\d+)')
        self.RE_CLEANUP = re.compile(r'</?[bui]>|{/?[bui]}|[\|]')
        self.RE_MULTISPACE = re.compile(r'\s{2,}')
        self.RE_TEXTONLY = re.compile(r'[.,:!?#/<>"]|[-]\s+')
        self.reset_entry()


    def reset_entry(self):
        """Reset internal parameters of the entry that is being currently constructed"""

        self.ENTRY = {
            'id': None, 'start': None, 'end': None, 
            'text': None, 'text_only': None, 
            'text_line_count': 0, 'words_count': 0}


    def entry_valid(self):
        """Check if the current subtitle entry has all necessary information defined"""

        if None in (self.ENTRY['id'], self.ENTRY['start'], self.ENTRY['end'], self.ENTRY['text']):
            return False

        return True


    def append_entry(self):
        """Append the current entry to the list of entries"""

        self.ENTRIES.append( copy(self.ENTRY) )


    def reading_text(self):
        """Whether currently the text section is being processed"""

        return self.ENTRY['text_line_count'] > 0


    def cleanup_text(self):
        """Remove typical formatting characters and whitespaces"""

        if not self.ENTRY['text']:
            return

        self.ENTRY['text'].strip()
        if self.CLEANUP_TEXT:
            self.ENTRY['text'] = self.RE_CLEANUP.sub('', self.ENTRY['text'])
            self.ENTRY['text'] = self.RE_MULTISPACE.sub('', self.ENTRY['text'])

    
    def textonly_string(self, _text):
        """Removes all characters that are not words"""

        text = _text
        text = self.RE_TEXTONLY.sub('', text)
        text = self.RE_MULTISPACE.sub('', text)

        return text.strip()


    def ms_from_string(self, string):
        """Extract the number of milliseconds from the specified string"""

        nMs = 0
        re_match = self.RE_TIME.match(string)
        for iG in range(self.RE_TIME.groups):
            nMs += int(float( re_match.group(iG+1) )) * self.MS_POSITION_FACTOR[iG]

        return nMs


    def parse(self):
        """Looping through lines of the input file and extracting every subtitle entry"""

        with open(self.INPUT_FILE_NAME) as input_file:
            for _line in input_file:
                line = _line.strip()
                # print len(line)
                if len(line) == 0:
                    if self.entry_valid():
                        if self.CLEANUP_TEXT:
                            self.cleanup_text()
                        self.ENTRY['text_only'] = self.textonly_string(self.ENTRY['text'])
                        self.ENTRY['words_count'] = len(self.ENTRY['text'].split())
                        self.append_entry()
                    # print " #### Empty: reset"
                    self.reset_entry()
                    continue
                elif self.RE_ID.match(line) and not self.reading_text():
                    self.ENTRY['id'] = int(float(line))
                    # print " #### ID: {0}".format(self.ENTRY['id'])
                elif '-->' in line and not self.reading_text():
                    lst_str_time = [str_time.strip() for str_time in line.split('-->')]
                    if len(lst_str_time) != 2:
                        continue
                    self.ENTRY['start'] = self.ms_from_string(lst_str_time[0])
                    self.ENTRY['end'] = self.ms_from_string(lst_str_time[1])
                    # print " #### Start/end: {0:d}/{1:d}".format(self.ENTRY['start'], self.ENTRY['end'])
                else:
                    if self.ENTRY['text'] == None:
                        self.ENTRY['text'] = ''
                    if self.ENTRY['text_line_count'] > 0:
                        self.ENTRY['text'] += ' '
                    self.ENTRY['text'] += line.strip()
                    self.ENTRY['text_line_count'] += 1
                    # print " #### Text: {0}".format(self.ENTRY['text'])

        return self
