Koanbot
=======

The Koanbot project is a sandbox environment for learning about natural language processing, python programming, and the nltk python package. The Koanbot employs a simple sentence analysis system that relies on n-gram generation and input/output filters.

To interact with it on a surface level, visit the Koanbot  [here](http:/ec2-54-187-163-101.us-west-2.compute.amazonaws.com/). For those who wish to dig deeper, read on!

###Download Instructions
To start playing with the project immediately:
 * Clone the project onto your local computer.
 * While in the project's root directory, run 'pip install -r requirements.txt'.
 * Still in root, run 'python views.py'.
 * You now have a copy of Koanbot running on your local machine at 'localhost:8000'!

#Input Filters

The input filters take user input as a list of words and use some algorithm to reduce this list to a *hopefully* shorter list of possible *seed words*. Current filters include: a length filter that removes all words with fewer than three characters, and a content filter that removes all non-content words (e.g. words that are not tagged as noun, verb, or adjective). Tagging, done using the nltk package, is discussed below. The input filters can be found in the input_filters.py file.

Adding more filters is quite simple. First write a filter in the input_filters.py file. It should take a list of strings (words) and return a list of strings (words) after this, add the 'add_func_to_dict' decorator with the name of your filter as the argument.

That's it!

Your filter is now tied in with the project and will be selectable on the website.

#The Brain

The Brain randomly chooses a seed from the seed words that make it through the input filters. It then uses this seed to generate a sentence of some kind; currently we are implementing bi- and tri-gram generation. It then repeats this process to make a large list (currently 200) of possible sentences.

The process for writing your own brain function is the same as for the input filters. The file to write them in is brains.py. For input they take an instance of the current chatbot, followed by the list of remaining seed words. For output they should give a list of possible sentences.

Don't forget to decorate!

#Output Filters

The Output filter is the final step. The list of sentences generated by the brain enter into the chosen output filters. Each filter attempts to reduce the number of possible sentences based on some criteria. We have implemented output filters that include: limiting the length of the sentence, sentence must contain at least one noun, adjective, or verb, and several versions of basic syntactic filters.

Again, the process for creating and decorating output filters is quite similar. For input they take a list of possible sentences and a dictionary. The four current dictionaries are discussed below. The output is a reduced list of sentences.

#Finally

If more than one sentence remains after the output filter, one is chosen at random from the remainder and returned to the user. In the event that no sentences remain, the Koanbot will let you know that it doesn't know what to say.

#Extra Info

##NLTK

The Natural Language Tool Kit is an immense python package that we really only brushed the surface of here. We used it to tag our training data with parts of speech and to analyze the syntax of the output sentences. One large area for imporovment in our project is finding more ways to utilize this valuable resource.

##Training the Koanbot

###New Material
If you wish to add new material to the Koanbot, this is a very easy process. 
 * Add the text file to the projects root directory.
 * From the root directory, run 'python trainbot.py <textfile>'.
 * A new set of dictionaries has been created!
 
###The Dictionaries

Training the Koanbot involves constructing four dictionaries that the Koanbot can access as it processes user input.
####Word to POS Dictionary
This dictionary contains every word in the training text as a key, with a list of all the parts of speech that the word was tagged as throughout the text.
####POS to Word Dictionary
This dictionary is the inverse of the previous one. It contains all the parts of speech that occur in the training text as a key, with a list of all the words that were tagged as that part of speech as a value.
####Bigram Dictionary
This dictionary contains every word as a key, with a list of every word that ever followed the key as a value.
####Trigram Dictionary
This dictionary contains every pair of words as a key, with a list of every word that ever followed the pair of words as a value.
