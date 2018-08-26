from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import configparser
import logging

# def cleanup(text):
# word_list = text.split()
# stop_words = set(stopwords.words("english"))
# filtered_words = ' '.join(word for word in word_list if word not in stop_words)
# translator = str.maketrans('','', string.punctuation)
# filtered_words_no_punctuation = filtered_words.translate(translator)
# return filtered_words

logger = logging.getLogger('scanner')


def tag_text(text):
    config = configparser.ConfigParser()
    config.read('config.properties')

    logger.info('The path to the classifier : %s', config['NLPSection']['nlp.classifier.path']  )
    logger.info('The path to the nlp jar : %s', config['NLPSection']['nlp.jar.path']  )

    try:
        st = StanfordNERTagger(config['NLPSection']['nlp.classifier.path'], config['NLPSection']['nlp.jar.path'])
    except:
        print('Unable to initialise the tagger because of wrong paths')
        raise

    tokenize_text = word_tokenize(text)
    tagged_text = st.tag(tokenize_text)
    return tagged_text


def get_organizations(text):
    tagged_text = tag_text(text)

    org_flag = False
    org_str = ''
    org_list = []
    for i in tagged_text:
        if i[1] == "ORGANIZATION":
            if not org_flag:
                org_str = ''
                org_flag = True
            org_str = org_str + ' ' + i[0]
        elif org_flag:
            org_list.append(org_str)
            org_flag = False

    return org_list
