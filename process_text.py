#from string import digits
#from nltk import word_tokenize
import re
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
        # Since some number could be missing due to errors in scraping, 
        # handle exception here to ensure error free
        try:
            text_list.append(postings_dict[str(i)]['posting'])
        except:
            continue        
    
    return text_list



def remove_digits(token):
    """
    Remove digits from a token

    Params:
        token: (str) a string token

    Returns:
        cleaned_token: (str) the cleaned token

    """
    # Remove digits from the token
    remove_digits = str.maketrans('', '', digits)
    token = token.translate(remove_digits)
    return token
    


def tokenize_text(text, stem=False):
    """
    Tokenize, stem and remove stop words for the given text
    
    Parameters:
        text: a text string
    
    Returns:
        tokens: the processed text as a list of tokens
    """
    stop_words = set(stopwords.words('english')) 
    #tokens = word_tokenize(text.lower())

    # Change "C++" to "Cpp" to avoid being removed below
    #tokens = ['cpp' if token=='c++' else token for token in tokens]
    # Same with C#
    #tokens = ['csharp' if token=='c#' else token for token in tokens]
    # Remove digits
    #tokens = [remove_digits(token) for token in tokens]
    # Remove non-alphabetic tokens and stopwords
    #tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
  
    # Use Regex to tokenize
    # Replace any non word characters except .+# with space
    text = re.sub("[^\w.+#]", " ", text)
    # Twe cases to replace with space
    # Case 1: \d+\.?\d+\s -- any number of digits followed by a space with or without
    # a dot in between
    # Case 2: \d+\+ -- any number of digits followed by a plus sign
    text = re.sub("\d+\.?\d+\s|\d+\+", " ", text) 
    tokens = text.lower().split()
    tokens = [token for token in tokens if token not in stop_words]

    # Stem tokens
    if stem:
        stemmer = SnowballStemmer("english")
        tokens = [stemmer.stem(i) for i in tokens]
                    
    return tokens 



def tokenize_list(text_list, stem=False, return_string=False):
    """
    Tokenize the given list of text and then combine list of tokens into text for plotting
    
    Parameters:
        text_list -- list of job posting strings
        
    Returns:
        text -- a text string for word cloud plot
    """
    # Split the text based on slash, space and newline, then take set     
    #text = [set(re.split('/| |\n|', i)) for i in text]
    #text = [set(re.split('\W', i)) for i in text_list]
    
    text_list_tokenized = [tokenize_text(text=i, stem=stem) for i in text_list]
    
    tokens = []
    # Combine all token lists into one big list of tokens
    for i in text_list_tokenized:
        tokens += i
        
    if return_string:
        text = ' '.join(tokens)
        return text
    
    # Return the list of all tokens
    return tokens  



def check_freq(dict_to_check, text_list):
    """
    Checks each given word's freqency in a list of posting strings.

    Params:
        words: (dict) a dict of word strings to check frequency for, format:
            {'languages': ['Python', 'R'..],
            'big data': ['AWS', 'Azure'...],
             ..}
        text_list: (list) a list of posting strings to search in

    Returns:
        freq: (dict) frequency counts

    """
    freq = {}

    # Join the text together and convert words to lowercase 
    text = ' '.join(text_list).lower()

    for category, skill_list in dict_to_check.items():
        # Initialize each category as a dictionary
        freq[category] = {}
        for skill in skill_list:
            if len(skill) == 1: # pad single letter skills such as "R" with spaces
                skill_name = ' ' + skill.lower() + ' '
            else:
                skill_name = skill.lower()    
            freq[category][skill] = text.count(skill_name)

    return freq
