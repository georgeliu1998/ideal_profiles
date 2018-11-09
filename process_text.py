from nltk import word_tokenize
from nltk.corpus import stopwords 
from nltk.stem.snowball import SnowballStemmer



def make_text_list(postings_dict, first_n_postings=100):
    """
    Extract the texts from postings_dict into a list of strings
    
    Parameters:
        postings_dict:  
        first_n_postings:  
    
    Returns:
        text_list: list of job posting texts
    
    """
    
    text_list = []
    for i in range(0, first_n_postings+1):
        # Since some number could be missing due to errors in scraping, handle exception here 
        # so that program can run error free
        try:
            text_list.append(postings_dict[str(i)]['posting'])
        except:
            continue        
    
    return text_list



def nltk_process(text, stem=False):
    """
    Tokenize, stem and remove stop words for the given text
    
    Parameters:
        text: a text string
    
    Returns:
        token_list: the processed text as a list of tokens
    """
    
    stop_words = set(stopwords.words('english')) 
    stemmer = SnowballStemmer("english")
    tokens = word_tokenize(text.lower())

    # Remove non-alphabetic tokens
    tokens = [token for token in tokens if token.isalpha()]

    # Remove stop words
    tokens = [token for token in tokens if token not in stop_words]
    # Stem tokens
    if stem:
        tokens = [stemmer.stem(i) for i in tokens]
                    
    return tokens 



def clean_text(text_list, stem=False, return_string=False):
    """
    Clean the text so that all words are root...
    
    Parameters:
        text_list -- list of job posting strings
        
    Returns:
        cleaned_text -- a text string for word cloud plot
    """
    # Split the text based on slash, space and newline, then take set     
    #text = [set(re.split('/| |\n|', i)) for i in text]
    #text = [set(re.split('\W', i)) for i in text_list]
    
    text_list_processed = [nltk_process(text=i, stem=stem) for i in text_list]
    
    cleaned_text = []
    for i in text_list_processed:
        cleaned_text += i
        
    if return_string:
        cleaned_text = ' '.join(cleaned_text)
    
    return cleaned_text  



def check_freq(words, tokens):
    """
    Check each given word's freqency in a list of tokens.

    Params:
        words: (list) a list of word strings to check frequency for
        text: (list) a list of tokens to search in

    Returns:
        freq: (dict) frequency counts

    """
    freq = {}

    for word in words:
        freq[word] = tokens.count(word)

    return freq
