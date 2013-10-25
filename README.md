Application can determine the language of the text in Unicode format. Currently there is a possibility of determining Finnish, Swedish, English, German, French, Italian, Estonian, Spanish, Portuguese and Russian.

Analysis is based on Unicode Table http://www.tamasoft.co.jp/en/general-info/unicode.html

ISO standart for names of languages http://en.wikipedia.org/wiki/ISO_639-3

and Wikipedia:Language recognition chart http://en.wikipedia.org/wiki/Wikipedia:Language_recognition_chart



### As input:

- text which has to be analysed.

- List of languages which should be checked. Like 'eng', 'fin', 'swe'
In that case only Finnish, Swedish, English will be analysed.

- And amount of the first characters for analysing - default is 250 - additional - bigger value increases quality, smaller value increases speed of analysis

### Possible languages: 

'eng': English, 
'fin': Finnish, 
'swe': Swedish, 
'deu': German, 
'fra': French, 
'ita': Italian, 
'est': Estonian, 
'spa': Spanish, 
'por': Portuguese, 
'rus': Russian 


### Return: 

List of languages in sorted order. First element is most probable language. In case of failure, the function returns string message.

Please, do not hesitate to leave a comment or send feedback to andrey.kramarev(at)gmail.com or contact the company

http://www.ampparit.com/tietoa/english