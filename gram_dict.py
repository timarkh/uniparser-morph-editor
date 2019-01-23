import re
import json
import os


class GrammDict:
    """
    Represents one file with the description of stems.
    """
    rxLemma = re.compile('-lexeme\n(?: [^\r\n]+\n)+', flags=re.DOTALL)
    rxLines = re.compile('(?<=\n) ([^:\r\n]+): *([^\r\n]*)(?=\n)', flags=re.DOTALL)
    rxFieldNum = re.compile('_[0-9]+$', flags=re.DOTALL)

    def __init__(self):
        fSettings = open('settings.json', 'r', encoding='utf-8-sig')
        self.settings = json.loads(fSettings.read())
        fSettings.close()
        filename = os.path.join(self.settings['dirname'], self.settings['filename'])
        fIn = open(filename, 'r', encoding='utf-8-sig')
        self.lemmaList = self.load_dict(fIn.read())
        fIn.close()
        print('Dictionary loaded,', len(self.lemmaList), 'lemmata found.')

    @property
    def cur_lemma(self):
        if 'cur_lemma' not in self.settings:
            self.settings['cur_lemma'] = 0
        return self.settings['cur_lemma']

    @cur_lemma.setter
    def cur_lemma(self, value):
        if 0 <= value < len(self.lemmaList):
            self.settings['cur_lemma'] = value

    def load_dict(self, text):
        """
        Find all lemmata in a string and return them as a list of lists [[key, value],...].
        """
        lemmaList = []
        lemmata = self.rxLemma.findall(text)
        for lemma in lemmata:
            dictLemma = [[line[0], line[1]] for line in self.rxLines.findall(lemma)]
            lemmaList.append(dictLemma)
        return lemmaList

    def save_lemmata(self):
        """
        Save the list of lemmata to the file indicated in the settings.
        """
        if len(self.lemmaList) <= 0:
            return
        filename = os.path.join(self.settings['dirname'], self.settings['filename'])
        fOut = open(filename, 'w', encoding='utf-8-sig')
        fOut.write('\n\n'.join('-lexeme\n ' + '\n '.join(kv[0] + ': ' + kv[1] for kv in l)
                               for l in self.lemmaList))
        fOut.close()

    def save_settings(self):
        """
        Overwrite current settings.
        """
        if len(self.settings) <= 0:
            return
        fSettings = open('settings.json', 'w', encoding='utf-8-sig')
        fSettings.write(json.dumps(self.settings, ensure_ascii=False, indent=2))
        fSettings.close()

    def get_prev_word(self):
        self.cur_lemma -= 1
        return self.get_cur_word()

    def get_next_word(self):
        self.cur_lemma += 1
        return self.get_cur_word()

    def get_cur_word(self):
        return self.lemmaList[self.cur_lemma]

    def update_cur_word(self, dictFields):
        fields = [[self.rxFieldNum.sub('', k)[6:], dictFields[k]]
                  for k in sorted(dictFields, key=lambda field: self.rxFieldNum.findall(field)[0])]
        self.lemmaList[self.cur_lemma] = fields


if __name__ == '__main__':
    gd = GrammDict()
    gd.save_lemmata()
