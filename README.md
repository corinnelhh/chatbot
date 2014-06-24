chatbot
=======


##Potential Resources

   * [A detailed description of creating an IRC chatbot](http://eflorenzano.com/blog/2008/11/17/writing-markov-chain-irc-bot-twisted-and-python/)
   * [documentation for Natural Language Toolkit](http://www.nltk.org/)
   * [Parsing English with 500 lines of Python](https://honnibal.wordpress.com/2013/12/18/a-simple-fast-algorithm-for-natural-language-dependency-parsing/)
     * [Redshift Github](https://github.com/syllog1sm/redshift) This is the program described by the above link
   * [Any tutorials for developing chatbots?](http://stackoverflow.com/questions/9706769/any-tutorials-for-developing-chatbots)
   * [Therapist.py ("a cheezy little Eliza knock-off by Joe Strout")](http://www.strout.net/info/coding/python/ai/therapist.py)
   * [Howie the Chatterbot](http://howie.sourceforge.net/)
   * [Computational Linguistics & Psycholinguistics Research Center](http://www.clips.ua.ac.be/)

##Similar projects
* [thebot 0.1.1](https://github.com/svetlyak40wt/thebot)
* [Videogrep](http://lav.io/2014/06/videogrep-automatic-supercuts-with-python/) (not that similar, but uses CLiPS packages to search for sentence structure)

##Possible packages:
   
* [Textblob] (https://textblob.readthedocs.org/en/dev/) is a python package that provides an api for the NLTK. 


##Sections of Project:

#Mission Statement:

We are trying to create a *simple* chatbot with a basic *sense of self*. It will have the following capabilities:

* Interact on live website

* Generates original grammatically correct sentences

* Can perform basic semantic analysis on user input
 
* Can appropriately answer basic questions regardless of form:
  * What is your name?, Who are you?, What are you called?
  
* Generates original grammatically correct sentences
  * Knowledge of parts of speech
  * Understanding of what makes a valid sentence
    * Syntactically valid sentence
    * Semantically valid sentence
  * Be able to generate stylistically appropriate sentence based on training materialshould I refer to you?
  * Where do you live?, Where is your home?, What city do you reside in?, Where are you?, Where are you from?
  * How are you?, How are you feeling?, How's it going? How are things?, What's up?
* Respond to statements (non-questions)


##Workflow (Stages):
 
###Stage 1
* Generates original grammatically correct sentences
  * Knowledge of parts of speech
  * Understanding of what makes a valid sentence
    * Syntactically valid sentence
    * Semantically valid sentence
  * Be able to generate stylistically appropriate sentence based on training materials
  * 

##Milestones for Tuesday 6/17:

* Research and identify POS tagger (Nathan)
* Draft plan for web interface (Josh)
* Outline next steps and research potential packages (Corinne)


###Stage 2 (Ephemeral Stage)
* Can perform basic semantic analysis on user input
  * Identify question versus statement. Hard code vs soft code?

###Stage 3 (Nebulous Stage)
* Can appropriately answer basic questions regardless of form:

###Stage 4 (Profit)


****************

###User Stories

 * 1) As an anonymous user, when I enter a single sentence into the text field the bot generates a single sentence response. 
 * 2) As an anonymous user, when I select a filter in the checklist the filter is applied to the next response. 
 * 3) As an anonymous user, when I click the "show me" button I see a log of the steps to generate the output. 
 * 4) As an anonymous user, when I visit the page I see a "Tweet" button to share the response. 
 * 5) An an anonymous user, when I visit the website I see the chatbot page. 
 * 6) As an anonymous user, when I visit the website I see a "Contact Us" link that takes me to the project email address and a link to the GitHub page. 
 * 7) As an anonymous user, when I have a noteworthy interaction with the bot I can click on a button to add that interaction to a "Best Of" page. 



[here](http://ec2-54-186-154-203.us-west-2.compute.amazonaws.com/) is the bot!









