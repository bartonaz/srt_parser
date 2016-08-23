"""Parser of subtitles in SRT format"""

import re

class SrtParser:
    # Global parameters of the class instance
    TIME_MS_FACTOR = 1
    MS_POSITION_FACTOR = (60*60*1e3, 60*1e3, 1e3, 1)
    CLEANUP_TEXT = True
    # Global parameters of the loop over lines
    INPUT_FILE_NAME = None
    RE_ID = None
    RE_TIME = None
    RE_CLEANUP = None
    ENTRIES = []
    ENTRY = None

    
    def __init__(self, filename):

        self.INPUT_FILE_NAME = filename
        self.RE_ID = re.compile(r'^\d+$')
        self.RE_TIME = re.compile(r'(\d+):(\d+):(\d+),(\d+)')
        self.RE_CLEANUP = re.compile(r'</?[bui]>|{/?[bui]}|\|')
        self.reset_entry()

    
    def reset_entry(self):
        """Reset internal parameters of the entry that is being currently constructed"""

        self.ENTRY = {id: None, start: None, end: None, text: None, text_line_count: 0}


    def entry_valid(self):
        """Check if the current subtitle entry has all necessary information defined"""

        if None in (self.id, self.start, self.end, self.text):
            return False

        return True


    def append_entry(self):
        """Append the currenty entry to the list of entries"""

        self.ENTRIES.append(self.ENTRY)


    def cleanup_text(self):
        """Remove typical formatting characters and whitespaces"""

        if not self.text:
            return

        self.text.strip()
        self.text.replace()


    @staticmethod
    def ms_from_string(self, string):
        """Extract the number of milliseconds from the specified string"""

        nMs = 0
        re_match = self.RE_TIME.match(string)
        for iG in range(self.RE_TIME.groups):
            nMs += re_match.group(iG)*self.MS_POSITION_FACTOR[iG]

        return nMs


    def read_entries():
        """Looping through lines of the input file and extracting every subtitle entry"""

        with open(self.INPUT_FILE_NAME) as input_file:
            for line in input_file:
                if len(line) == 0:
                    if (self.entry_valid()):
                        if self.CLEANUP_TEXT:
                            self.cleanup_text()
                        self.append_entry()
                    self.reset_entry()
                    continue
                elif self.RE_ID.match(line):
                    self.ENTRY.id = int(float(line))
                elif '-->' in line:
                    lst_str_time = (str_time.strip() for str_time in line.split('-->'))
                    if len(lst_str_time) != 2:
                        continue
                    self.ENTRY.start = self.ms_from_string(lst_str_time[0])
                    self.ENTRY.end = self.ms_from_string(lst_str_time[1])
                else:
                    self.ENTRY.text += line.strip()
                    if self.ENTRY.text_line_count > 0:
                        self.ENTRY.text += ' '
                    self.ENTRY.text_line_count += 1










