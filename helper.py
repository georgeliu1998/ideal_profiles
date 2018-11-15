import json
import re, csv
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt
from process_text import *
import pandas as pd
import numpy as np



def load_data(file_name):
    """
    Open the saved json data file and load the data into a dict.
    
    Parameters:
        file_name: the saved file name, e.g. "machine_learning_engineer.json"
    
    Returns:
        postings_dict: data in dict format   
    
    """

    with open(file_name, 'r') as f:
        postings_dict = json.load(f)
        return postings_dict



def plot_wc(text, max_words=200, stopwords_list=[], to_file_name=None):
    """
    Make a word cloud plot using the given text.
    
    Parameters:
        text -- the text as a string
    
    Returns:
        None    
    """
    wordcloud = WordCloud().generate(text)
    stopwords = set(STOPWORDS)
    stopwords.update(stopwords_list)

    wordcloud = WordCloud(background_color='white',
                         stopwords=stopwords,
                         #prefer_horizontal=1,
                         max_words=max_words, 
                         min_font_size=6,
                         scale=1,
                         width = 800, height = 800, 
                         random_state=8).generate(text)
    
    plt.figure(figsize=[16,16])
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    
    if to_file_name:
        to_file_name = to_file_name + ".png"
        wordcloud.to_file(to_file_name)



def plot_profile(title, 
    first_n_postings, 
    max_words=200, 
    return_posting=False, 
    return_tokens=False,
    return_text_list=False):
    """
    Loads the corresponding json file, extracts the first_n job postings and plot the wordcloud profile.
    
    Parameters:
        title: the job title such as "data scientist"
        first_n_postings: int, the first n job postings to use for the plot.
    
    Returns:
        nth_posting: the nth job posting as a string. This helps to verify the first_n_postings param used.
    
    """
    # Convert title to full file name then load the data
    file_name = '_'.join(title.split()) + '.json'
    data = load_data(file_name)
    
    # Only of the two can be True
    if (return_posting + return_tokens + return_text_list) >= 2:
        print('You can only return one of these: a posting, tokens, text list! \nPlease try again.')
        return None

    if return_posting:
        n_posting = data[str(first_n_postings)]
        return n_posting
    
    text_list = make_text_list(data, first_n_postings)

    if return_text_list:
        return text_list
    elif return_tokens:
        tokens = tokenize_list(text_list, return_string=False)
        return tokens
    else:
        # Get the tokens joined as a string
        text = tokenize_list(text_list, return_string=True)
        # Get the stop words to use
        with open('stopwords.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            stop_list = list(reader)[0]
        to_file_name = '_'.join(title.split())
        plot_wc(text, max_words, stopwords_list=stop_list, to_file_name=to_file_name)



def plot_title(df, title, save_figure=False):
    """
    Plots the skill frequencies of all skill categories for a given title.
    
    Params:
        df: (pandas df) the frequency df
        title: (str) one of the three job titles
            ['data scientist', 'machine learning engineer', 'data engineer']
    
    Returns:
        None
    
    """
    titles = ['data scientist', 'machine learning engineer', 'data engineer']
    if title in titles:
        title = title.title()
    else:
        print('Title invalid. Please try again!')
    
    # Subset df to the given title
    df_title = df.query('title==@title')

    # Set up the parameters for the plotting grid
    nrows=4
    ncols=2
    figsize = (15, 20)
    # Add a dummy category name to match the grid
    categories = np.append(df_title.category.unique(), 'Empty').reshape(4, 2)
    
    # Generate the plotting objects
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    
    # Loop thru the axis of the figure
    for row in range(nrows):
        for col in range(ncols):
            cat = categories[row, col]
            # Subset to one category for each subplot
            df_cat = df_title.query('category==@cat')
            df_cat = df_cat.sort_values(by='frequency', ascending=False)
            # Find the correspoinding axis in axes
            ax = axes[row, col]
            # Handle errors for the empty last subplot
            try:
                df_cat.plot(x='skill', y='frequency', kind='bar', ax=ax)
                ax.set(title=cat, xlabel='', ylabel='Frequency')
                for tick in ax.get_xticklabels():
                    tick.set_rotation(60)
            except:
                pass

    # Add the figure title
    fig_title = title + ' Skill Frequencies'
    fig.suptitle(fig_title, y=0.9, verticalalignment='bottom', fontsize=30)
    plt.subplots_adjust(hspace=0.8) # make sure the figure title doesn't overlap with subplot titles
    plt.show()

    if save_figure:
        figure_name = fig_title + '.png'
        fig.savefig(figure_name)


