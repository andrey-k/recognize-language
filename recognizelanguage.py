# -*- coding: utf-8 -*-
"""Language recognizing

Application can determine the language of the text in Unicode format. 
Currently there is a possibility of determining Finnish, Swedish, English,
German, French, Italian, Estonian, Spanish, Portuguese and Russian.

Analysis is based on
Unicode Table
http://www.tamasoft.co.jp/en/general-info/unicode.html
ISO standart for names of languages
http://en.wikipedia.org/wiki/ISO_639-3
and
Wikipedia:Language recognition chart
http://en.wikipedia.org/wiki/Wikipedia:Language_recognition_chart

Copyright (c) 2009- Andrey Kramarev, Ampparit Inc. (www.ampparit.com)

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above
    copyright notice, this list of conditions and the following
    disclaimer in the documentation and/or other materials provided
    with the distribution.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE, DAMMIT.

"""

import re
__author__ = "Andrey Kramarev, Ampparit Inc"
__copyright__ = "Copyright (c) 2009- Andrey Kramarev, Ampparit Inc."
__license__ = "New BSD License"
__version__ = "1.1"
__email__ = "andrey.kramarev@ampparit.com"

# Main function. Input: text which has to be analysed,
# list of languages which should be checked 
# and amount of the first characters for analysing - default is 250
#
# Parameters:
# originalText = text for analysing in Unicode format
# languages = List of possible languages. Like ['eng', 'fin', 'swe']
# In that case only Finnish, Swedish, English will be analysed.
# textLength - additional - bigger value increases quality, 
# smaller value increases speed of analysis
# Possible languages 
# 'eng': English,
# 'fin': Finnish,
# 'swe': Swedish, 
# 'deu': German,
# 'fra': French,
# 'ita': Italian,
# 'est': Estonian,
# 'spa': Spanish,
# 'por': Portuguese,
# 'rus': Russian
#
# Return:
# List of languages in sorted order. First element is
# most probable language.
# In case of failure, the function returns string message.

def recognizeLanguage(originalText, languages, textLength=250): 
    # Is text in Unicode
    if not isinstance(originalText, unicode):
        return "text not in unicode"
    # Returns list of language for analyzing
    languages = usedLanguages(languages)
    if isinstance(languages, str):
        return languages

    # Application uses first 250 text characters if length of text more
    # than 250 - default. It is possible to increase length 
    # to get more accurate result
    end = originalText.find(" ", textLength)
    if end < 0:
        end = None
    text = ' ' + originalText[0:end] + ' '

    # Transfer text to lowercase
    text = text.lower()

    # Replace all punctuation
    text = text.replace('!', ' ')
    text = text.replace('?', ' ')
    text = text.replace(':', ' ')
    text = text.replace(';', ' ')
    text = text.replace(',', ' ')
    text = text.replace('.', ' ')
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    text = ' '.join(text.split())

    # Detecting alphabet: Cyrillic or Latin
    hasKey = languages.has_key
    if hasKey('rus'):
        alphabet = detectAlphabet(text)
    else:
        alphabet = 'latin'

    if alphabet == 'cyrillic':
        if detectRussian(text) == 'rus':
            languages['rus'] = 1

    elif alphabet == 'latin':
        if hasKey('fin'):
            languages['fin'] = detectFinnish(text)
        if hasKey('swe'):
            languages['swe'] = detectSwedish(text)
        if hasKey('eng'):
            languages['eng'] = detectEnglish(text)
        if hasKey('deu'):
            languages['deu'] = detectGerman(text)
        if hasKey('fra'):
            languages['fra'] = detectFrench(text)
        if hasKey('ita'):
            languages['ita'] = detectItalian(text)
        if hasKey('est'):
            languages['est'] = detectEstonian(text)
        if hasKey('spa'):
            languages['spa'] = detectSpanish(text)
        if hasKey('por'):
            languages['por'] = detectPortuguese(text)
    
    # List of languages in sorted order. First element is
    # most probable language
    return sorted(languages, key=languages.__getitem__, reverse=True)
    """end of detectLanguage function"""
"""-------------------------------------"""

def usedLanguages(languages):
    """Variables initialization"""
    # Input value has to be a list
    if not isinstance(languages, list):
        return 'not list'
    # By default all languages are not included into analysis
    possibleLanguages = {
        'eng': False,
        'fin': False,
        'swe': False, 
        'deu': False,
        'fra': False,
        'ita': False,
        'est': False,
        'spa': False,
        'por': False,
        'rus': False,
    }
    listOfLanguages = {}
    for search in languages:
        if search in possibleLanguages:
            listOfLanguages[search] = 0
        else:
            return ''.join(['unknown language: ', search])

    # Function returns list of languages with user settings
    return listOfLanguages
    """end of usedLanguages function"""
"""-------------------------------------"""

def detectAlphabet(text):
    """Alphabet recognizing
    Variables initialization"""

    latinAlphabet = 0
    cyrillicAlphabet = 0
    usedAlphabet = []
    # Application uses first 60 text characters if length of text more
    # than 60.
    if len(text) >= 60:
        maxPosition = 60
    else: maxPosition = len(text)

    # We check every seventh text symbol to determine to which alphabet
    # it belongs 
    for letterPosition in xrange(0, maxPosition, 6):
        # If text character belongs to Latin interval we increase 
        # the latinAlphabet variable with 1
        if text[letterPosition] >= u'a' and text[letterPosition] <= u'z':
            latinAlphabet += 1
        # If text character belongs to Cyrillic interval we increase 
        # the cyrillicAlphabet variable with 1
        elif text[letterPosition] >= u'Ё' and text[letterPosition] <= u'ё':
            cyrillicAlphabet += 1
        # The loop stops if 3 Latin or 3 Cyrillic characters are found
        if latinAlphabet == 3 or cyrillicAlphabet == 3:
            break

    if latinAlphabet == 3:
        usedAlphabet = 'latin'
    elif cyrillicAlphabet == 3:
        usedAlphabet = 'cyrillic'
    else:
        usedAlphabet = 'Text language does not belong to the language list'
    # If there are less than 60 characters then choose the bigger
    if len(text) < 60:
        if latinAlphabet >= cyrillicAlphabet:
            usedAlphabet = 'latin'
        else:
            usedAlphabet = 'cyrillic'

    return usedAlphabet    
    """end of detectAlphabet function"""
"""-------------------------------------"""

def detectRussian(text):
    """Variables initialization"""

    numberOfI = 0
    # Last possible symbol used in Russian
    possibleSymbols = u'¾'
    error = 0

    # We know that it is Cyrillic and we have to be sure that it is Russian
    """detection of Russian language"""
    numberOfI += text.count(u'и')
    for letterPosition in xrange(0, len(text)):
        # We increase error variable if character does not belong 
        # to possible symbols
        if (text[letterPosition] > possibleSymbols and
            (text[letterPosition] < u'А' and text[letterPosition] != u'Ё' or
             text[letterPosition] > u'я' and text[letterPosition] != u'ё')):
            error += 1            
        if error == 7:
            # Return default language
            language = 'eng'
            return language

    # If text uses enough Russian "i" we can say that it is Russian
    if numberOfI >= 2:
        language = 'rus'
    else: 
        language = 'eng'

    return language
    """end of detectRussian function"""
"""-------------------------------------"""

# There are several rules for each language. 
# Different rules have different rates depending on how often characters 
# combination are present in language and are not present into other languages
def detectFinnish(text):
    """Variables initialization"""
    fin = 0
    ruleOne = [u'nen ', u' on ', u' ja ', u' en ']
    ruleTwo = [u'en ', u'in ', u'ka ', u'kä ']
    ruleThree = [u'sinä ', u'minä ']
    ruleFour = [u'aa', u'ee', u'ii', u'kk', u'll', u'ss', u'mm', u'uu', u'oo',
                u'tt', u'ei', u'äi', u'ai', u'ie', u'oi', u'ng', u'ää']
    ruleFive = [u'ä', u'ö']
    ruleSix = [u'yö', u'hd', u'uo']
    
    count = text.count
    for search in ruleOne:
        fin += 1.1 * count(search)
    for search in ruleTwo:
        fin += 1.5 * count(search)
    for search in ruleThree:
        fin += count(search)
    for search in ruleFour:
        fin += 1.1 * count(search)
    for search in ruleFive:
        fin += count(search)
    for search in ruleSix:
        fin += 3 * count(search)
    fin -= 2 * count(u'd ')
    fin -= 5 * count(u'ü')
    fin -= count(u'é')

    return fin
    """end of detectFinnish function"""
"""-------------------------------------"""

def detectSwedish(text):
    """Variables initialization"""
    swe = 0
    ruleOne = [u'stj', u'skj', u'er ', u'en ']
    ruleTwo = [u'sj', u'tj', u'll', u'tt', u'rr']
    ruleThree = [u' är ', u' på ']
    ruleFour = [u'ä', u'ö']
    ruleFive = [u'nen ', u' on ', u' ja ', u' en ', u' av ', u' om ', u' de ']
    ruleSix = [u' den ', u' var ', u' man ', u' men ']
    ruleSeven = [u' som ', u' och ', u' att ', u' det ', u' hur ']
    
    count = text.count
    for search in ruleOne:
        swe += count(search)
    for search in ruleTwo:
        swe += count(search)
    for search in ruleThree:
        swe += 6 * count(search)
    for search in ruleFour:
        swe += count(search)
    for search in ruleFive:
        swe += 1.1 * count(search)
    for search in ruleSix:
        swe += count(search)
    for search in ruleSeven:
        swe += 6 * count(search)
    swe += 6 * count(u'å')
    swe += 2 * count(u' i ')
    swe += 3 * count(u' och ')

    return swe
    """end of detectSwedish function"""
"""-------------------------------------"""

def detectEstonian(text):
    """Variables initialization"""
    est = 0
    ruleOne = [u'ü', u'ä', u'ö']
    ruleTwo = [u' on ', u' ja ', u' ej ', u' ka ']
    ruleThree = [u' see ', u' saa ']
    ruleFour = [u'd ', u'aa', u'ee', u'ii', u'kk', u'll', u'tt', u'ss', u'oo',
                u'uu', u'ei', u'äi', u'ie', u'ää']
    
    count = text.count
    for search in ruleOne:
        est += count(search)
    for search in ruleTwo:
        est += count(search)
    for search in ruleThree:
        est += 1.5 * count(search)
    for search in ruleFour:
        est += 1.1 * count(search)
    est += 2 * count(u' ta ')
    est += 4 * count(u'õ')
    
    return est
    """end of detectEstonian function"""
"""-------------------------------------"""

def detectGerman(text):
    """Variables initialization"""
    deu = 0
    ruleOne = [u' und ', u' dir ', u' der ', u' die ', u' von ', u' das ',
               u' den ', u' dem ', u' des ', u' ist ', u' ich ', u' sie ',
               u'chen ']
    ruleTwo = [u' er ', u' es ', u' du ', u'ern ', u'ung ', u'tsch']
    ruleThree = [u'sch', u'en ', u'er ', u'st ']
    ruleFour = [u'tz', u'ss', u'ie', u'äu']
    ruleFive = [u'ü', u'ä', u'ö']
    ruleSix = [u'ß']
    ruleSeven = [u'à', u'â', u'ç', u'è', u'é', u'ê', u'î', u'ô', u'û']

    count = text.count
    for search in ruleOne:
        deu += 5 * count(search)
    for search in ruleTwo:
        deu += 5 * count(search)
    for search in ruleThree:
        deu += count(search)
    for search in ruleFour:
        deu += count(search)
    for search in ruleFive:
        deu += count(search)
    for search in ruleSix:
        deu += 5 * count(search)
    for search in ruleSeven:
        deu -= 9 * count(search)
    deu += 8 * count(u' aber ')
    
    return deu
    """end of detectGerman function"""
"""-------------------------------------"""

def detectEnglish(text):
    """Variables initialization"""
    eng = 0
    ruleOne = [u' and ', u' the ', u' are ', u'tion ', u' you ']
    ruleTwo = [u"'re ", u"'ll ", u"'ve ", u'ough', u'augh', u' we ', u' be ',
               u' is ', u' am ', u' an ', u' in ', u' of ', u' on ', u'ing ',
               u'age ', u"n't ", u"'ve "]
    ruleThree = [u' a ', u' i ', u"'s ", u"'d ", u"'m ", u'ed ']
    ruleFour = [u' und ', u' der ', u' das ']
    ruleFive = [u'th', u'ch', u'sh']
    ruleSix = [u' have ', u' will ']
    ruleSeven = [u'ì', u'ò', u'è', u'ú', u'à', u'â', u'ç', u'è', u'é', u'î',
                 u'ô', u'û', u'ü', u'ä', u'ö', u'ß'] 

    count = text.count
    for search in ruleOne:
        eng += 4 * count(search)
    for search in ruleTwo:
        eng += 3 * count(search)
    for search in ruleThree:
        eng += 1.5 * count(search)
    for search in ruleFour:
        eng -= count(search)
    for search in ruleFive:
        eng += count(search)
    for search in ruleSix:
        eng += 3 * count(search)
    for search in ruleSeven:
        eng -= 3 * count(search)
    eng += 3 * count(u' that ')
    

    return eng
    """end of detectEnglish function"""
"""-------------------------------------"""

def detectFrench(text):
    """Variables initialization"""
    fra = 0
    ruleOne = [u' en ', u' de ', u' le ', u' la ', u' il ']
    ruleTwo = [u' du ', u'aux ', u'eux ', u' et ']
    ruleThree = [u" l'", u" d'"]
    ruleFour = [u'à', u'â', u'ç', u'è', u'é', u'ê', u'î', u'ô', u'û']
    ruleFive = [u'á', u'í', u'ì', u'ó', u'ò']
    
    count = text.count
    for search in ruleOne:
        fra += count(search)
    for search in ruleTwo:
        fra += 5 * count(search)
    for search in ruleThree:
        fra += 3 * count(search)
    for search in ruleFour:
        fra += 2 * count(search)
    for search in ruleFive:
        fra -= count(search)
    fra += 2 * count(u' des ')

    return fra   
    """end of detectFrenchItalian function"""
"""-------------------------------------"""

def detectItalian(text):
    """Variables initialization"""
    ita = 0
    ruleOne = [u' è ', u'tà ', u' e ']
    ruleTwo = [u'zz', u'bb', u'gn', u'tt', u'cc', u'ss', u'pp', u'll', u'o ']
    ruleThree = [u'a ', u'e ']
    ruleFour = [u'zione ', u'aggio ']
    ruleFive = [u'gli', u'sci']
    ruleSix = [u'ì', u'ò', u'é', u'ú']
    ruleSeven = [u" l'", u" d'"]
    ruleEight = [u'â', u'ç', u'ê', u'î', u'ô', u'û']

    count = text.count
    for search in ruleOne:
        ita += count(search)
    for search in ruleTwo:
        ita += count(search)
    for search in ruleThree:
        ita += 0.5 * count(search)
    for search in ruleFour:
        ita += 3 * count(search)
    for search in ruleFive:
        ita += count(search)
    for search in ruleSix:
        ita += count(search)
    for search in ruleSeven:
        ita += 2 * count(search)
    for search in ruleEight:
        ita -= 0.5 * count(search)
    ita += count(u' perché ')
    ita += count(u' il ')
    ita += count(u'mento ')

    return ita    
    """end of detectItalian function"""
"""-------------------------------------"""

def detectSpanish(text):
    """Variables initialization"""
    spa = 0
    ruleOne = [u' o ', ' a ']
    ruleTwo = [u'ción ', u' uno ', u' una ']
    ruleThree = [u' los ', u' las ']
    ruleFour = [u' de ', u' la ']
    ruleSix = [u'o ', u'a ']
    ruleSeven = [u' unos ', u' unas ']
    ruleFive = [u'á', u'í', u'ñ', u'ú', u'ó', u'¡', u'¿', u'é']

    count = text.count
    for search in ruleOne:
        spa += 0.5 * count(search)
    for search in ruleTwo:
        spa += 2 * count(search)
    for search in ruleThree:
        spa += 2 * count(search)
    for search in ruleFour:
        spa += count(search)
    for search in ruleFive:
        spa += count(search)
    for search in ruleSix:
        spa += 0.5 * count(search)
    for search in ruleSeven:
        spa += 5 * count(search)
    spa += 5 * count(u'miento ')
    spa += 4 * count(u'dad ')
    spa += 5 * count(u' y ')
    spa += 5 * count(u' el ')
    spa += 5 * count(u' ll')
    spa += 5 * count(u'ñ')

    return spa
    """end of detectSpanish function"""
"""-------------------------------------"""

def detectPortuguese(text):
    """Variables initialization"""
    por = 0
    ruleOne = [u' o ', u' a ', u' e ', u' à ', u' é ']
    ruleTwo = [u' de ', u' da ', u' ou ']
    ruleThree = [u' aos ', u' das ', u' uns ', u' uma ', u' ele ', u' ela ',
                 u' não ', u'ções ', u'dade ']
    ruleFour = [u'nh', u'lh', u'm ', u'z ']
    ruleFive = [u'á', u'í', u'ú', u'ó', u'é', u'â', u'ê', u'ô', u'â']
    ruleSix = [u' os ', u' às ', u' ao ', u' um ', u'ção ', u'ões ']
    ruleEight = [u' do ', u' as ', u' em ']
    ruleNine = [u'a ', u'o ']
    ruleSeven = [u' dos ', u' que ', u' por ']

    count = text.count
    for search in ruleOne:
        por += count(search)
    for search in ruleTwo:
        por += count(search)
    for search in ruleThree:
        por += count(search)
    for search in ruleFour:
        por += count(search)
    for search in ruleFive:
        por += count(search)
    for search in ruleSix:
        por += 5 * count(search)
    for search in ruleSeven:
        por += count(search)
    for search in ruleEight:
        por += 2 * count(search)
    for search in ruleNine:
        por += 0.5 * count(search)
    por += 2 * count(u'ã')
    por += 2 * count(u'õ')

    return por
    """end of detectSpanish function"""
"""-------------------------------------"""