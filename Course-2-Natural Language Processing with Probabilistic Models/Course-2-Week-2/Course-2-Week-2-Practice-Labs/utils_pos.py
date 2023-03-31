import numpy as np 
import string 
# Punctuation characters
punct = set(string.punctuation)

# Morphology rules used to assign unknown word tokens
noun_suffix = ["action", "age", "ance", "cy", "dom", "ee", "ence", "er", "hood", "ion", "ism", "ist", "ity", "ling", "ment", "ness", "or", "ry", "scape", "ship", "ty"]
verb_suffix = ["ate", "ify", "ise", "ize"]
adj_suffix = ["able", "ese", "ful", "i", "ian", "ible", "ic", "ish", "ive", "less", "ly", "ous"]
adv_suffix = ["ward", "wards", "wise"]

# Additive smoothing parameter
alpha = 0.001


def initialize_probs(states):
    ''' 
    Input: 
        states: a set of possible parts of speech tags
    Output: 
        trans_probs: a dictionary where the keys are states the values are dictionaries where the keys are states and the 
        values are 0.
        
    This dictionary will be later populated
    '''
    transition_probability = {}    # A dictionay of POS, 
    for state in states:
        transition_probability[state] = 0
    trans_pos = {}
    for state in states:
        trans_pos[state] = transition_probability
        
    return trans_prob


def get_states(tagged_corpus):
    '''
    Input:
        tagged_corpus: a list of sentences 
    Output:
        states: the states in a tuple
        observations: the observations in a tuple
    '''
    states = set()
    observations = set()
    for sent in tagged_corpus: 
        for tup in sent: 
            word, label = tup 
            states.add(label)
            observations.add(word)
    observations.add('<s>')
    states.add('<s>')
    return tuple(states), tuple(observations)

def get_probabilities(states, observations):
    ''' 
    Input: 
        states: a tuple of POS tags
        observations: a tuple of possible words 
    Output: 
        trans_pos: a dictionary where the keys are the POS and the values are dictionaries where the keys are POS and the values are transitions.
        emission_probabilities: a dictionary where the keys are the 
    ''' 
    all_words = {}
    for observation in observations:
        all_words[observation] = 0

    # these are the two dictionaries we will fill.
    transition_probability = {}    # A dictionay of POS, 
    emission_probabilities = {}

    # these are the 
    for state in states:
        transition_probability[state] = 0
        #initializing 
        emission_probabilities[state] = all_words
    trans_pos = {}
    for state in states:
        trans_pos[state] = transition_probability
        
    return trans_pos, emission_probabilities

# GRADED FUNCTION: get_transitions
def get_transitions(tagged_sents, states, transition_probability, emission_probability):
    '''
    Input: 
        train: a list of tuples where each tuple is of this form (word, label)
    Output: 
        transition_probability: a dictionary of dictionaries (maps each word to other transitions)
                                maybe a table.
    '''
    # transition_probability = {}    # A dictionay of POS, 
    # POS dictionary has the same keys and all the values are 0 at first
    
    ### START CODE HERE ### 
    total_count = 0
    # Fill in the dictionary with all the number of times it appears in the 
    
    for sent in tagged_sents:
        prev_state = '<s>'
        for word in sent:
            word, label = word
            cur_dict = transition_probability[prev_state]
            cur_dict[label] += 1   
            total_count += 1
            transition_probability[prev_state] = cur_dict
            prev_state = label
            # Now computing the emission
            emission_probability[label][word] +=1 
    # Convert it into a probability
    for state, dictionary in transition_probability.items():
        total_words = sum(transition_probability[state].values())
        for n_state in dictionary:
            transition_probability[state][n_state] = transition_probability[state][n_state]/total_words
            
    for state, dictionary in emission_probability.items():
        total_words = sum(emission_probability[state].values())
        for word in dictionary:
            emission_probability[state][word] = emission_probability[state][word]/total_words
            
    ### END CODE HERE ### 
    
    return transition_probability, emission_probability

def assign_unk(tok):
    """
    Assign unknown word tokens
    """
    # Digits
    if any(char.isdigit() for char in tok):
        return "--unk_digit--"

    # Punctuation
    elif any(char in punct for char in tok):
        return "--unk_punct--"

    # Upper-case
    elif any(char.isupper() for char in tok):
        return "--unk_upper--"

    # Nouns
    elif any(tok.endswith(suffix) for suffix in noun_suffix):
        return "--unk_noun--"

    # Verbs
    elif any(tok.endswith(suffix) for suffix in verb_suffix):
        return "--unk_verb--"

    # Adjectives
    elif any(tok.endswith(suffix) for suffix in adj_suffix):
        return "--unk_adj--"

    # Adverbs
    elif any(tok.endswith(suffix) for suffix in adv_suffix):
        return "--unk_adv--"

    return "--unk--"

def get_word_tag(line, vocab): 
    if not line.split():
        word = "--n--"
        tag = "--s--"
        return word, tag
    else:
        word, tag = line.split()
        if word not in vocab: 
            # Handle unknown words
            word = assign_unk(word)
        return word, tag
    return None 

def preprocess(vocab, data_fp):
    """
    Preprocess data
    """
    orig = []
    prep = []

    # Read data
    with open(data_fp, "r") as data_file:

        for cnt, word in enumerate(data_file):

            # End of sentence
            if not word.split():
                orig.append(word.strip())
                word = "--n--"
                prep.append(word)
                continue

            # Handle unknown words
            elif word.strip() not in vocab:
                orig.append(word.strip())
                word = assign_unk(word)
                prep.append(word)
                continue

            else:
                orig.append(word.strip())
                prep.append(word.strip())

    assert(len(orig) == len(open(data_fp, "r").readlines()))
    assert(len(prep) == len(open(data_fp, "r").readlines()))

    return orig, prep
# TO be deleted later 
def get_frequency(tagged_corpus):
    '''
    Input: 
        tagged_corpus: a list of tuples where the first element of each tuple is the word 
                       and the second is the POS.
    Ouput: 
        freqs: a dictionary where the keys are words and the values are a list of possible tags.
    '''
    freqs = {} # dictionary to be returned
    curr_words = set()
    ### START CODE HERE ###
    for tup in tagged_corpus:
        word, label = tup
        if word not in curr_words:
            new_dict = {}
            new_dict[label] = 1
            freqs[word] = new_dict
        else:
            cur_dict = freqs[word]
            if label in set(cur_dict.keys()):
                cur_dict[label] += 1
            else:
                cur_dict[label] = 1
            freqs[word] = cur_dict
        curr_words.add(word)
    ### END CODE HERE ###
    return freqs

def predict_pos(prep, y, tagged_counts):
    '''
    Input: 
        data: a list of tuples where each tuple consists of (word, POS)
        freqs: a dictionary where the keys are words and the values are a list of possible tags.
    Output: 
        accuracy: Number of times you classified a word correctly
    '''
    num_correct = 0
    total = len(test_x)
    all_words = set(freqs.keys())
    for x, y in zip(test_x, test_y): 
        _, true_label = y 
        if x in all_words:
            cur_dict = freqs[x]
            pos_final = ''
            freq_final = 0
            for pos, freq in cur_dict.items():
                if freq > freq_final:
                    freq_final = freq
                    pos_final = pos
            if pos_final == true_label:
                num_correct +=1 
    return num_correct/total
#https://github.com/melanietosik/viterbi-pos-tagger/blob/master/scripts/viterbi.py
