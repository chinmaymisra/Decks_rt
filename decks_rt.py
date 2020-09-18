import pandas as pd
from bs4 import BeautifulSoup
import urllib.request

#funciton no.6
def deck_sum(df,filename="deckreadtime.xlsx"):
    """Function to generate find sum of cards of each deck and return results

    Args:
        df (Dataframe): Dataframe of concept summary decks data
        filename (str, optional): Name you want to assign to the file where Deck Read Time will be saved. Defaults to "deckreadtime.xlsx".

    Returns:
        lists: first list contains all unique deck numbers, second list contains corresponding read time sums.
    """

    
    lnew=[]
    idl=[]
    curid=df.iloc[1,0]
    idl=set(list(df["DECK ID"]))
    decksum=0
    for i in range(len(df)):
        nextid=df.iloc[i,0]
        if nextid==curid:
            decksum+=df.iloc[i,7]
        else:
            lnew.append(decksum)
            print("deck id ",curid," is done")
            curid=df.iloc[i,0]
            decksum=df.iloc[i,7]
        if i==len(df)-1:
            print("deck id ",curid," is done")
            lnew.append(decksum)
    dfnew=pd.DataFrame()
    dfnew["DECK ID"]=idl
    dfnew["READ TIME IN MINUTES"]=lnew
    dfnew.to_excel(filename)

    return idl,lnew
    
#function no.5
def read_time(df):
    """To calculate read time of each individual card of a deck

    Args:
        df (Dataframe): Dataframe containing all the individual cards

    Returns:
        Dataframe: Returns Dataframe with added column for read times
    """

    df["READING TIME"]=""
    for i in range(len(df)):
        df.iloc[i,7]=float(df.iloc[i,5])/128
    return df



#function no.4
def is_image(df):
    """To check whether the card was an image or not, if less than 10 words were fetched, we deem it as an image.

    Args:
        df (Dataframe):Datafram containing decks card data

    Returns:
        Dataframe: Retruns Dataframe with added column as image or not.
    """


    df["IMG_COUNT"]=""
    imglist=[]
    for i in range(len(df)):
        if df.iloc[i,5]<=10:
            df.iloc[i,6]="YES"
        else:
            df.iloc[i,6]="NO"


    return df
    




#function no.3
def word_count(df):
    """Calculate word count of each card

    Args:
        df (Dataframe): Dataframe containing all decks data

    Returns:
        Dataframe: Returns Dataframe with added column of word count for each concept card 
    """


    df["WORDCOUNT"]=""
    wc=[]
    for i in range(len(df)):
        txt=df.iloc[i,4]
        w=txt.split(" ")
        count=0
        for j in w:
            if len(j)>1:
                count+=1
        wc.append(count)
    try:
        df["WORDCOUNT"]=wc
    except:
        print("Wordcounts obtained list length not matching with Dataframe length")
    return wc


#function no.1
def fetch_data(file_name):
    """Fetch data from each link in given file 

    Args:
        file_name (csv file): csv file containing decks concept summary data

    Returns:
        dataframe,list: returns read dataframe along with fetched data from urls, also returns content of urls as a list
    """


    df=pd.read_csv(filename)
    df["CONTENT"]=""
    li=[]
    for i in range(len(df)):
        print("FETCHING URL ",i)
        url=df.iloc[i,2]
        try:
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html)
            strips = list(soup.stripped_strings)
            doc=""
            for l in strips:
                doc=doc+" "+l
            li.append(doc)
        except:
            li.append("NAN")
    try:
        df["CONTENT"]=li
    except:
        print("Fetched items list length doesn't match Dataframe length")
    return df,li



#function no.2
def clean_data(df):

    """Function to clean the fetched data

    Returns:
        Dataframe: Returns dataframe containing cleaned data in the same column
    """


    for i in range(len(df)):
        txt=df.iloc[i,4]
        txt=txt.replace(u'\xa0',u' ')
        txt=txt.replace('$\\',' ')
        txt=txt.replace(u'u\\',u' ')
        txt=txt.replace(u'uv\\',u' ')
        txt=txt.replace(u'v\\',u' ')
        txt=txt.replace(u'$',u' ')
        txt=txt.replace(u'\\',u' ')
        df.iloc[i,4]=txt

    return df


    