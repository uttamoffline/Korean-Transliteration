import re
'''
This romanizer is largely inspired by Ilkyu Ju (@osori) and contains slight modifications
    - partial / incomplete korean syllables (i.e. ㅋㅋㅋ)
    - specific 'consonant followed by vowel' cases
    - begin to tackle consonant assimilation cases
'''

'''
### Vowels ###
'''
vowel = {
    #simple vowels
    'ㅏ' : 'a',
    'ㅓ' : 'eo',
    'ㅗ' : 'o',
    'ㅜ' : 'u',
    'ㅡ' : 'eu',
    'ㅣ' : 'i',
    'ㅐ' : 'ae',
    'ㅔ' : 'e',
    'ㅚ' : 'oe',
    'ㅟ' : 'wi',
    
    #diphthongs
    'ㅑ' : 'ya',
    'ㅕ' : 'yeo',
    'ㅛ' : 'yo',
    'ㅠ' : 'yu',
    'ㅒ' : 'yae',
    'ㅖ' : 'ye',
    'ㅘ' : 'wa',
    'ㅙ' : 'wae',
    'ㅝ' : 'wo',
    'ㅞ' : 'we',
    'ㅢ' : 'ui', 
}

'''
### Consonants ###
'''
#initial position (choseong)
onset = {
    # 파열음 stops/plosives
    'ᄀ' : 'g',
    'ᄁ' : 'kk',
    'ᄏ' : 'k',
    'ᄃ' : 'd',
    'ᄄ' : 'tt',
    'ᄐ' : 't',
    'ᄇ' : 'b',
    'ᄈ' : 'pp',
    'ᄑ' : 'p',
    # 파찰음 affricates
    'ᄌ' : 'j',
    'ᄍ' : 'jj',
    'ᄎ' : 'ch',
    # 마찰음 fricatives
    'ᄉ' : 's',
    'ᄊ' : 'ss',
    'ᄒ' : 'h',
    # 비음 nasals
    'ᄂ' : 'n',
    'ᄆ' : 'm',
    # 유음 liquids
    'ᄅ' : 'r',
    # Null sound
    'ᄋ' : '',
}

#coda position (jongseong)
coda = {
    # 파열음 stops/plosives
    'ᆨ' : 'k',
    'ᆮ' : 't',
    'ᆸ' : 'p',
    'ᇁ' : 'p',
    # 비음 nasals
    'ᆫ' : 'n',
    'ᆼ' : 'ng',
    'ᆷ' : 'm',
    # 유음 liquids
    'ᆯ' : 'l',
    None: '',
}

#if needed to map higher range jamo to lower range jamo
unicode_onset_lower = {
    'ㄱ' : 'ᄀ',
    'ㄲ' : 'ᄁ',
    'ㅋ' : 'ᄏ',
    'ㄷ' : 'ᄃ',
    'ㄸ' : 'ᄄ',
    'ㅌ' : 'ᄐ',
    'ㅂ' : 'ᄇ',
    'ㅃ' : 'ᄈ',
    'ㅍ' : 'ᄑ',
    # 파찰음 affricates
    'ㅈ': 'ᄌ',
    'ㅉ' : 'ᄍ',
    'ㅊ' : 'ᄎ',
    # 마찰음 fricatives
    'ㅅ' : 'ᄉ',
    'ㅆ' : 'ᄊ',
    'ㅎ' : 'ᄒ',
    # 비음 nasals
    'ㄴ' : 'ᄂ',
    'ㅁ' : 'ᄆ',
    # 유음 liquids
    'ㄹ' : 'ᄅ',
    # Null sound
    'ㅇ' : 'ᄋ'}

#if needed to map higher range jamo to lower range jamo
unicode_coda_lower = {
    # 파열음 stops/plosives
    'ㄱ': 'ᆨ',
    'ㄷ' : 'ᆮ',
    'ㅂ' : 'ᆸ',
    'ㅍ' : 'ᇁ',
    # 비음 nasals
    'ㄴ' : 'ᆫ',
    'ㅇ' : 'ᆼ',
    'ㅁ' : 'ᆷ',
    # 유음 liquids
    'ㄹ' : 'ᆯ',
}

#unicode_initial = [ 'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 
#'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
unicode_initial = [ chr(initial_code) for initial_code in range(4352, 4371)]
unicode_medial = [ 'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 
'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

#unicode_final = [ None,  'ㄱ',  'ㄲ',  'ㄳ',  'ㄴ',  'ㄵ',  'ㄶ',  'ㄷ',  'ㄹ',  'ㄺ', 
# 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ','ㅀ', 'ㅁ', 'ㅂ', 'ㅄ',  'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 
# 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
unicode_final = [ chr(final_code) for final_code in range(0x11a8, 0x11c3)]
unicode_final.insert(0, None)

#'_' acts as a placeholder (some jamo in initial position do not exist in final position)
unicode_compatible_finals = ['ᆨ', 'ᆩ', 'ᆫ', 'ᆮ', '_', 'ᆯ', 'ᆷ', 'ᆸ', '_', 
'ᆺ', 'ᆻ', 'ᆼ', 'ᆽ', '_', 'ᆾ', 'ᆿ', 'ᇀ', 'ᇁ', 'ᇂ']

double_consonant_final = {
    'ㄳ' : ('ㄱ', 'ㅅ'),
    'ㄵ' : ('ᆫ', 'ㅈ'), 
    'ᆭ' : ('ᆫ', 'ᇂ'),
    'ㄺ' : ('ㄹ', 'ㄱ'), 
    'ㄻ' : ('ㄹ', 'ㅁ'), 
    'ㄼ' : ('ㄹ', 'ㅂ'), 
    'ㄽ' : ('ㄹ', 'ㅅ'), 
    'ㄾ' : ('ㄹ', 'ㅌ'), 
    'ㄿ' : ('ㄹ', 'ㅍ'),
    'ㅀ' : ('ㄹ', 'ᇂ'), 
    'ㅄ' : ('ㅂ', 'ㅅ'), 
    'ㅆ' : ('ㅅ', 'ㅅ')
}

NULL_CONSONANT = 'ᄋ'

HANGUL_OFFSET = 0xAC00
'''
Korean unicode beginning
'''
#separates syllable into initial, medial, and final components
class Syllable(object):
    def __init__(self, char):
        self.char = char
        _is_hangul = self.is_hangul(char)
        if _is_hangul:
            _separated = self.separate(char)
            self.initial = unicode_initial[_separated[0]]
            self.medial = unicode_medial[_separated[1]]
            self.final = unicode_final[_separated[2]]
        else:
            self.initial = ord(char)
            self.medial = None
            self.final = None

    #check if syllable is korean
    def is_hangul(self, char):
        if HANGUL_OFFSET <= ord(char) <= 0xD7A3:
            return True
        return False

    #separate korean into initial, medial (vowel), and final components
    def separate(self, char):
        if(self.is_hangul(char)):
            initial = ((ord(char) - HANGUL_OFFSET) // 588)
            final = (ord(char) - HANGUL_OFFSET) % 28
            medial = ((ord(char) - HANGUL_OFFSET - final) % 588) // 28
            '''why were these used'''

        return [initial, medial, final]

    #construct character from the initial, medial, and final components
    def construct(self, initial, medial, final):
        if self.is_hangul(self.char):
            initial = ord(initial) - 4352
            medial = unicode_medial.index(medial)
            #some characters do not have a final components
            if final is None:
                final = 0
            else:
                final = unicode_final.index(final)
            constructed = chr((final + (medial * 28) + (initial * 588)) + HANGUL_OFFSET)
        else:
            constructed = self.char
        
        self.char = constructed
        return constructed

    #moves the character in the final position to the intial position of next syllable
    def final_to_initial(self, char):
        idx = unicode_compatible_finals.index(char)
        return unicode_initial[idx]

    #useful for "official" string representation
    def __repr__(self):
        self.construct(self.initial, self.medial, self.final)
        return self.char
    
    #useful for informal (readable) string representation
    def __str__(self):
        self.char = self.construct(self.initial, self.medial, self.final)
        return self.char

#based on separated syllable, apply rules to account for special provisions 
class RomanizeRules(object):
    def __init__(self, text):
        self._syllables = [Syllable(char) for char in text]
        self.pronounced = ''.join([str(char) for char in self.rules()])

    def rules(self):
        for index, syllable in enumerate(self._syllables):
            #see if there is a next syllable
            try:
                next_syllable = self._syllables[index + 1]
                if HANGUL_OFFSET > ord(next_syllable.char) or ord(next_syllable.char) > 0xD7A3:
                    next_syllable = None
            except IndexError:
                next_syllable = None

            #see if final is before a consonant
            try: 
                final_before_consonant = syllable.final and next_syllable.initial not in (None, NULL_CONSONANT)
            except AttributeError:
                final_before_consonant = False

            #see if final is before a vowel
            try:
                final_before_vowel = syllable.final and next_syllable.initial in (NULL_CONSONANT)
            except AttributeError:
                final_before_vowel = False

            #see if consonant followed by consonant
            try:
                consonant_before_consonant = final_before_consonant and syllable.final not in (None, NULL_CONSONANT)
            except AttributeError:
                consonant_before_consonant = False

            #consonant followed by a consonant and consonant assimilation
            if consonant_before_consonant:
                if syllable.final in ['ᆩ', 'ᆿ', 'ᆪ', 'ㄺ']:
                    syllable.final = 'ᆨ'
                elif syllable.final in ['ᆺ', 'ᆻ', 'ᆽ', 'ᆾ', 'ᇀ']:
                    syllable.final = 'ᆮ'
                elif(syllable.final in ['ᇁ', 'ㅄ', 'ㄿ']):
                    syllable.final = 'ᆸ'
                elif(syllable.final in ['ᆲ', 'ᆳ', 'ᆴ']):
                    syllable.final = 'ᆯ'
                elif(syllable.final in ['ᆬ']):
                    syllable.final = 'ᆫ'
                elif(syllable.final in ['ᆱ']):
                    syllable.final = 'ᆷ'

                #consonant assimilation
                if syllable.final == 'ᆫ' and next_syllable.initial == 'ᄅ':
                      syllable.final = 'ᆯ'
                if syllable.final == 'ᆨ' and next_syllable.initial == 'ᄂ':
                    syllable.final = 'ᆼ'
                if syllable.final == 'ᆨ' and next_syllable.initial == 'ᄅ':
                    syllable.final = 'ᆼ'
                    next_syllable.initial = 'ᄂ'
                if syllable.final == 'ᆼ' and next_syllable.initial == 'ᄅ':
                    next_syllable.initial = 'ᄂ'
                if next_syllable.initial == 'ᄒ':
                    if syllable.final == 'ᆨ':
                        next_syllable.initial = 'ᄏ'
                    elif syllable.final == 'ᆸ':
                        next_syllable.initial = 'ᄑ'
                    elif syllable.final == 'ᆮ':
                        next_syllable.initial = 'ᄐ'
    
            #changes based on ㅎ
            if syllable.final in ['ᇂ', 'ᆭ', 'ᆶ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄀ', 'ᄃ', 'ᄌ', 'ᄉ']:
                        change_to = {'ᄀ': 'ᄏ','ᄃ': 'ᄐ','ᄌ':'ᄎ', 'ᄉ': 'ᄊ'}
                        syllable.final = None
                        next_syllable.initial = change_to[next_syllable.initial]

                    elif next_syllable.initial == 'ᆫ':
                        if syllable.final == 'ᆶ':
                            syllable.final = 'ᆯ' 
                        else:
                            syllable.final = 'ᆫ'

                    elif next_syllable.initial == NULL_CONSONANT:
                        if syllable.final == 'ᆭ':
                            syllable.final = 'ᆫ'
                        elif syllable.final == 'ᆶ':
                            syllable.final = 'ᆯ' 
                        else:
                            syllable.final = None
                else:
                    if syllable.final == 'ᇂ':
                            syllable.final = None

            #consonant followed by a vowel
            if syllable.final and final_before_vowel:
                if syllable.final != 'ᆼ':
                    next_syllable.initial = next_syllable.final_to_initial(syllable.final)
                    syllable.final = None
                elif next_syllable.medial == 'ㅣ':
                    if syllable.final == 'ᇀ':
                        next_syllable.initial = next_syllable.final_to_initial('ᆾ')
                    elif syllable.final == 'ᆮ':
                        next_syllable.initial = next_syllable.final_to_initial('ᆽ')
                        
            #double consonant finals (겹받침)
            if syllable.final in double_consonant_final and next_syllable:
                double_consonant = double_consonant_final[syllable.final]
                syllable.final = double_consonant[0]
                next_syllable.initial = next_syllable.final_to_initial(double_consonant[1])

        return self._syllables

class Romanizer(object):
    def __init__(self, text):
        self.text = text

    def romanize(self):
        pronounced = RomanizeRules(self.text).pronounced
        hangul = r'[가-힣]'
        hangul_component = r'[ㄱ-ㅣ]'
        _sep_romanized = []
        _romanized = ''
        _full_char = ''

        #romanize full korean syllables and partial korean syllables
        for char in pronounced:
            if re.match(hangul, char):
                s = Syllable(char)
                try:
                    _full_char = onset[s.initial] + vowel[s.medial] + coda[s.final]
                    _sep_romanized.append(_full_char)
                except:
                    _sep_romanized.append('#')
            elif re.match(hangul_component, char):
                if char in unicode_onset_lower:
                    _sep_romanized.append(onset[unicode_onset_lower[char]])
                elif char in vowel:
                    _sep_romanized.append(vowel[char])
                elif char in unicode_coda_lower:
                     _sep_romanized.append(coda[unicode_coda_lower[char]])
                else:
                    _sep_romanized.append('#')
            else:
                _sep_romanized += char

        #hypenating the text to avoid confusion / decrease uncertainty
        for i in range(len(_sep_romanized)):
            if i != len(_sep_romanized) - 1:
                if _sep_romanized[i] == ' ':
                    _romanized += ' '
                else:
                    if _sep_romanized[i + 1] == ' ':
                        _romanized += _sep_romanized[i]
                    #account for punctuation in middle of sentence
                    elif _sep_romanized[i + 1] in [';', ':', ',', '-', '--', '.']:
                        _romanized += _sep_romanized[i]
                    else:
                        _romanized += _sep_romanized[i] + '-'
            else:
                _romanized += _sep_romanized[i]
        
        return _romanized

#later, use nltk to capitalize proper nouns

#examples
string1 = '안녕하세요.'
string2 = '저는 대학생 입나다 ㅋㅋㅋ ㅏㅏㅏ.' #partial korean syllables
string3 = '종로, 그렇지, 입학, 행복하다, 곧할거야' #consonant assimilation
string4 = 'This doesnt contain any Korean #@12345?!'
print(Romanizer(string1).romanize())
print(Romanizer(string2).romanize())
print(Romanizer(string3).romanize())
print(Romanizer(string4).romanize())
