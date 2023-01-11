import spacy
import pandas as pd

nlp = spacy.load("ja_core_news_sm")

class Preprocessing():

    def __init__(self, text):
        self.sentlist = []
        self.text = text

    def get_sentlist(self):
        paragraphs = self.text.split("\n")
        for i in paragraphs:
            i = i.split("。")
        for j in i:
            if len(j) > 0:
                self.sentlist.append(j)

        return self.sentlist

    def get_rdf_tuples(self, sents:str):
        self.sents = sents
        a = []  #list of subject-transitive verbs-object triplet
        b = []  #list of subject-intransitive verbs-oblique nominal triplet
        ent1 = "" 
        ent2 = ""
        ent3 = ""
        rel1 = ""
        rel2 = ""

        prv_tok_dep = ""
        prv_tok_text = ""
        prv_tok_pos = ""

        prefix = ""
        modifier = ""
        prefix = ""

        for tok in nlp(self.sents):
            if tok.dep_ != "punct":
            
            # Get prefix
                if tok.dep_ == "compound":
                    prefix = tok.text

                    if prv_tok_dep == "compound":
                        prefix = prv_tok_text + tok.text
                
                    if prv_tok_text == "や":
                        prefix = modifier + "や" + tok.text
            
                # Get modifier
                if tok.dep_.endswith("mod") == True:
                    modifier = tok.text

                    if prv_tok_dep == "compound":
                        modifier = prefix + tok.text
            
                # Get compound verbs or normal verbs
                if tok.pos_ == "VERB" and tok.tag_ == "動詞-非自立可能" or tok.tag_ == "名詞-普通名詞-サ変可能":
                    if ent1 and ent2:
                        if prv_tok_pos == "VERB":
                            rel1 = prv_tok_text + tok.lemma_
                        else:
                            rel1 = tok.lemma_
                    if ent1 and ent3:
                        if prv_tok_pos == "VERB":
                            rel2 = prv_tok_text + tok.lemma_
                        else:
                            rel2 = tok.lemma_
            
                # Get oblique nominal
                if tok.dep_ == "obl":
                    if prv_tok_dep == "compound":
                        ent3 = prefix + tok.text
                    else:
                        ent3 = modifier  + tok.text
                    prefix = ""
                    modifier = ""
                    prv_tok_dep = ""
                    prv_tok_text = ""
            
                # Get subject
                if tok.dep_ == "nsubj":
                    if prv_tok_dep == "compound":
                        ent1 = prefix + tok.text
                    else:
                        ent1 = modifier  + tok.text
                    prefix = ""
                    modifier = ""
                    prv_tok_dep = ""
                    prv_tok_text = ""
            
                # Get object
                if tok.dep_ == "obj":
                    if prv_tok_dep == "compound":
                        ent2 = prefix + tok.text
                    else:
                        ent2 = modifier  + tok.text
                    prefix = ""
                    modifier = ""
                    prv_tok_dep = ""
                    prv_tok_text = ""

                prv_tok_dep = tok.dep_
                prv_tok_text = tok.text
                prv_tok_pos = tok.pos_

                if ent1 and ent2 and rel1:
                    if [ent1, rel1, ent2] not in a:
                        a.append([ent1, rel1, ent2])
                        ent2 = None

                if ent1 and ent3 and rel2:
                
                    if [ent1, rel2, ent3] not in b:
                        b.append([ent1, rel2, ent3])
                        ent3 = None
            
                # Restart the check of entities after each conversation finishes.
                if tok.dep_ == "case" and tok.text == "と" and prv_tok_text.endswith("」"):
                    ent1 = None
                    ent2 = None
                    ent3 = None
            
        return a, b

    def get_all_tuples(self, pairs1, pairs2):
        self.pairs1 = pairs1
        self.pairs2 = pairs2
        all_pairs = []
        for i in self.pairs1:
            all_pairs.append(i)
        for i in self.pairs2:
            all_pairs.append(i)
        
        return all_pairs

    def get_kg_dataset(self, rdf_triplet:list):
        self.triplet = rdf_triplet

        heads = [i[0] for i in self.triplet]
        relationships = [i[1] for i in self.triplet]
        tails = [i[2] for i in self.triplet]
        kg_dataset = pd.DataFrame({'head':heads, 'tail':tails, 'edge':relationships})
        
        self.kg_dataset = kg_dataset

        return self.kg_dataset