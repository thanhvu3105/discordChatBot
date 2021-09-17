import nltk
#stem the word 
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle

from tensorflow.python.framework import ops


with open("intents.json") as file:
    data = json.load(file)

try: 
    #pickle on words labels docs_x docs_y
    with open("data.pickle","rb") as f:
        #save 4 variables in pickles file
        words,label,training,output = pickle.loads(f)

except:
    words = []
    labels = []
    docs_x = []  #pattern
    docs_y = []  #tag


    for intent in data["intents"]:
        patterns = intent["patterns"]
        for pattern in patterns:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(pattern)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    #convert all to lower cases
    words = [stemmer.stem(w.lower()) for w in words]
    #remove duplicate
    words = sorted(list(set(words)))

    #sort labels(tag)
    labels = sorted(labels)

    #bag of words to train model
    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]
    #if the tag exist, set to 1
    for x, doc in enumerate(docs_x):
        doc=nltk.word_tokenize(doc)
        bag = []
        # wrds = [stemmer.stem() for w in doc]
        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            # wrds = [stemmer.stem(w)]
            #if the word exist in current pattern
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)


        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    ouput = np.array(output)

    with open("data.pickle", "wb") as f:
        #write all variables to pickle files
        pickle.dump((words,labels,training,output),f)

#classifed data
#reset underline data graph
ops.reset_default_graph()

#define expected input for model
#input layer
#each training input is gonna be the same len, model expects how many words we have 
                 
net = tflearn.input_data(shape=[None,len(training[0])])
#add layer to neural network with start as input data 

#have 8 neurons for the fully connected hidden layer to neural netwrok
net = tflearn.fully_connected(net, 20)
#have another hidden layer with 8 neural
net = tflearn.fully_connected(net, 20)

#get probability for each output    represent labels    #softmax function
net = tflearn.fully_connected(net, len(output[0]),activation ="softmax")

#apply regression the provided layer
net = tflearn.regression(net)

#train model, DNN is type of neural network
model = tflearn.DNN(net)


try:
    model.load("model.tflearn")
except:
    #pass training data, n_epoch is amount to see the same data
    model.fit(training,output,n_epoch=3000,batch_size=10,show_metric = True)
    model.save("model.tflearn")

def bag_of_words(s,words):
    #size of bags equal length of words, set it all to 0 
    bag = [0 for _ in range(len(words))]
    
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    #generate bag list
    for se in s_words:
        for i,w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return np.array(bag)





def chat():
    print("Start talking with the bot(type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break
                                #call bag of words
        results = model.predict([bag_of_words(inp,words)])[0]
        results_index = np.argmax(results)
        tag = labels[results_index]

        if(results[results_index] > 0.7):
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg["responses"]


            print(random.choice(responses))
        else:
            print("Can't fucking understand you! Ask a real fucking question")


chat()
