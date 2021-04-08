from thespian.actors import *
from thespian.troupe import troupe
import os
import spacy
import datetime

@troupe(idle_count=3, max_count=5)
class DocProcess(Actor):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def receiveMessage(self, message, sender):
        self.process_doc(message["filename"])

    def process_doc(self, filelocation):
        doctext = None
        with open(filelocation, "r") as f:
            doctext = f.read()
        analyzed_text = self.nlp(doctext)
        sentence_process = self.createActor(SentenceProcessor, globalName="sentence_process")
        sentences = [sent.text for sent in analyzed_text.sents]
        message = {}
        message["sentences"] = sentences
        self.send(sentence_process, message)

class SentenceProcessor(Actor):
    def receiveMessage(self, message, sender):
        self.process_sentence(message)

    def process_sentence(self, sentence):
        for sentence in sentence["sentences"]:
            print(sentence)



if __name__ == "__main__":
    print("Running")
    now = datetime.datetime.now()
    print("Start: ", now)
    asys = ActorSystem("multiprocTCPBase")
    docprocess = ActorSystem("multiprocTCPBase").createActor(DocProcess, globalName="doc_process")
    #sentprocess = asys.createActor(SentenceProcessor)
    
    
    base = "/Users/Shared/s21_ds_nlp/homeworks/homework_1/data/"
    files = os.listdir(base)
    for infile in files:
        full_file = os.path.join(base, infile)
        asys.tell(docprocess, {"filename": full_file})
    now = datetime.datetime.now()
    print("End: ", now)
    