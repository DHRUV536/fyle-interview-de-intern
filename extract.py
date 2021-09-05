# Your imports go here
import logging
import json
logger = logging.getLogger(__name__)

'''
    Given a directory with receipt file and OCR output, this function should extract the amount

    Parameters:
    dirpath (str): directory path containing receipt and ocr output

    Returns:
    float: returns the extracted amount

'''
def extract_amount(dirpath: str) -> float:
    logger.info('extract_amount called for dir %s', dirpath)
    common_words = ['credit','total','payment','price','paid','debit','total:']
    path = dirpath + '/ocr.json'                       
    with open(path,encoding='utf-8') as json_file:
        file = json.load(json_file)                    
        list_of_words = []                              # First i will build list of all words in json file...
        for text in file['Blocks']:
            try:                                        # Some blocks don't have 'Text' key so i used try and except
                list_of_words.append(text['Text'])      # appending word one by one list
            except KeyError:
                pass
        k = []
        for i in reversed(list_of_words):               # it will be easy to use reversed list because obviously we will find total amount at the end of the list
            if i.lower() in common_words:               # searching if any word  in common words list like total, paid, price etc
                index = list_of_words.index(i)          # note down index of that word in acutaly list of words
                # there are high chances we get total amount in 3 words after common word ( total,paid etc ), this idea actually worked for 18 images
                for j in list_of_words[index:index+3]:
                    try:
                        if 1 not in k:
                            value =  float(j.replace('$','').replace('USD',''))        # Replace '$' and 'USD' and check if no.  is float, if yes this is amount
                        k.append(1)
                    except ValueError:
                        pass
            if 1 in k:                                                  # if we found the amount in first three words ( after common word ), get out of the loop then
                break
        # Now there are some images ( there are acutally 2 images ) in which total amount is not immediately after common words, so we will collect every float value after common word
        if 1 in k:
            pass
        else:
            dollars_words = []                                         # list of floating point values
            for word in list_of_words[index+3:index+30]:
                if '$' in word:
                    dollars_words.append(word.replace('$','').replace(',',''))
            value = float(max(dollars_words))                          # returning maximum floating point value, and that is our total amount
        return value
