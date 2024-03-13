import re, os, pandas as pd
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList

    from pyscript.app.scripts import nlp_parser
    from .knowledge_source      import KnowledgeSource
    from ..data_level.hypothesis import Hypothesis
    from ..data_level.word      import Word
    from ..data_level.text      import Text
    from ..data_level.sentence  import Sentence
    from ..controller.ks   import Ks
    from ..controller.ks_ar   import KSAR
    from ..controller.trace    import Trace


import time
from collections import defaultdict


class TextToSentences(KnowledgeSource):
    """
    A knowledge source class that processes QA1 Ner

    Attributes
    ----------
    description: str
        String of description to be parsed
    annotation: Dict
        Formatted annotation for each task
    corenlp_output: Dict
        Annotated output of StanfordCoreNLP parser
    """

    def __init__(self, hypothesis_ids, ks_ar, trace):
        fields = [v for v in Ks.ALL_KS_FORMATS.values() if v[0] == self.__class__.__name__][0]
        super().__init__(fields[1], fields[2], fields[3], trace, hypothesis_ids, ks_ar)


        self.description        = None
        self.annotation         = {"Word": None, "Sentence": None}
        self.store_hypotheses = []

    @classmethod
    def process_ks_ars(cls):
        """
        A class method that processes all the ks_ars with py_name='TextToSentences' and status=0.

        :param cls: The class itself (implicit parameter).
        :type cls: type
        :return: None
        """
        while True:
            
            ks = Ks.search(props={smile.hasPyName:'TextToSentences'}, how='first')
            if len(ks) >0:
                ks = ks[0]
            else:
                continue
            ks_ar = KSAR.search(props={smile.hasKS:ks.id, smile.hasKSARStatus:0}, how='first')
            if len(ks_ar) > 0:
                ks_ar = ks_ar[0]
                cls.logger(trace_id=ks_ar.trace, text=f"Processing ks_ar with id: {ks_ar.id}")

                # Get the hypothesis ids from the ks_ar
                in_hypo_ids = ks_ar.input_hypotheses
                if len(in_hypo_ids) != 1:
                    raise(Exception(f"Bad Input Hypothesis Count {len(in_hypo_ids)}"))

                in_hypo = Hypothesis(inst_id=in_hypo_ids[0])
                in_hypo.cast_to_graph_type()
                if not isinstance(in_hypo, smile.Text): #check if Phras
                    raise(Exception(f"Bad Input Hypothesis Type {type(in_hypo)}"))

                # Get the trace from the ks_ar
                trace = Trace(inst_id=ks_ar.trace)
                
                # Construct an instance of the ks_object
                ks_object = cls(hypothesis_ids=in_hypo_ids, ks_ar=ks_ar, trace=trace)
                
                # Call ks_object.set_input() with the necessary parameters
                ks_ar.ks_status = 1
                ks_object.set_input(description=in_hypo.content)
                
                ks_ar.ks_status = 2               
                hypotheses = ks_object.get_outputs()
                ks_ar.keep_db_in_synch = False
                trace.keep_db_in_synch = False
                for hypo in hypotheses:
                    ks_ar.hypotheses = hypo.id 
                    trace.hypotheses = hypo.id
                    if isinstance(hypo, smile.Sentence):
                        in_hypo.sentences = hypo.id
                        hypo.text = in_hypo.id
                ks_ar.save()
                trace.save()
                ks_ar.keep_db_in_synch = True
                trace.keep_db_in_synch = True
                # log output
                LOG_FILE_TEMPLATE = CONFIG.LOG_DIR+'smile_trace_log.txt'
                filename = LOG_FILE_TEMPLATE.replace('.txt', f"_{trace.id}.txt")
                ks_ar.summary(filename=filename)

                ks_ar.ks_status = 3                                

            time.sleep(1)        

    def set_input(self, description):
        # import shutil, os
        # if os.path.exists('pyscript/app/scripts/scroll/data/'): shutil.rmtree('pyscript/app/scripts/scroll/data/')
        # if os.path.exists('pyscript/app/scripts/scroll/models/'): shutil.rmtree('pyscript/app/scripts/scroll/models/')
        # if os.path.exists('pyscript/app/scripts/scroll/res/'): shutil.rmtree('pyscript/app/scripts/scroll/res/')
        # if os.path.exists('pyscript/app/scripts/scroll/stats/'): shutil.rmtree('pyscript/app/scripts/scroll/stats/')

        self.store_hypotheses = []
        print('a', len(self.store_hypotheses))
        self.set_basics(description=description)
        print('g', len(self.store_hypotheses))

    def get_outputs(self):
        print('1', len(self.store_hypotheses))
        self.get_basics()
        print('7', len(self.store_hypotheses))

        return self.store_hypotheses

    def set_basics(self, description):
        data_levels=("Sentence", "Word")

        """Run corenlp parsing functions of the requested output data levels.

        :param data_levels: output data levels that the contoller requests.
                            default is set to all possible output levels.
                            it could be both a string or a list.
        :return: updated corenlp output
        """
        self.description = description
        self.corenlp_output = nlp_parser.parse(self.description, requests=data_levels)

        _ = nlp_parser.build_prolog_from_output(id1=self.trace.id, id2=self.ks_ar.id, text=self.description, corenlp_output=self.corenlp_output)



        if ("Word" in data_levels):  # get a list of word information
            if self.annotation["Word"] is None:
                self.annotation["Word"] = nlp_parser.get_words(self.corenlp_output)

        # if ("Sentence" in data_levels):  # get a list of word information
        #     if self.annotation["Sentence"] is None:
        #         self.annotation["Sentence"] = nlp_parser.get_sentences(self.corenlp_output)

        print("\t1.7", len(self.annotation.keys()))
        for k,v in self.annotation.items():
            print("\t1.71", k)
            print("\t\t1.72", v)

        return self.annotation


    def get_basics(self):
        rel_word_queries = {}
        # self.ks_ar
        print("\tg1.1", len(self.store_hypotheses))
        sentences = defaultdict(list)
        for token in self.annotation["Word"]:
            print("\tg1.2", len(self.store_hypotheses))

            certainty = 1
            word = Word.find_generate(
                trace_id=self.trace.id,
                content=token["content"],
                content_label = token["content_label"],
                start=token["start"],
                end=token["end"],
                certainty=certainty)
            word.from_ks_ars = self.ks_ar.id
            self.store_hypotheses.append(word)
            sentences[token['sindex']].append(word)

        certainty = 1.0
        for sindex, words in sentences.items():
            content = ' '.join([word.content for word in words])
            start = min([word.start for word in words])
            end = max([word.end for word in words])
            sentence = Sentence.find(
                trace_id=self.trace.id,
                index=sindex,
                content=content,
                start=start,
                end=end)
            if sentence is None:
                sentence = Sentence.generate(
                    trace_id=self.trace.id,
                    index=sindex,
                    content=content,
                    start=start,
                    end=end,
                    certainty=certainty)
                hold_keep_db_in_synch = sentence.keep_db_in_synch
                sentence.keep_db_in_synch = False
                for word in words:
                    sentence.words = word.id 
                sentence.save()
                sentence.keep_db_in_synch = hold_keep_db_in_synch

            for word in words:
                word.sentence = sentence.id

            sentence.certainty = certainty
            sentence.from_ks_ars = self.ks_ar.id
            self.store_hypotheses.append(sentence)
            
        return self.store_hypotheses


    def set_spos(self):
        self.df_spos = nlp_parser.generate_spos(id1=self.trace.id, id2=self.ks_ar.id, corenlp_output=self.corenlp_output)

    def get_spos(self):
        for spo_id in self.df_spos["spo_id"].unique():
            this_spo_df = self.df_spos[self.df_spos["spo_id"] == spo_id]
            this_spo = {"s": None, "p": None, "o": None}
            for i, row in this_spo_df.iterrows():
                content_label = row.token
                words = Word.search(props={smile.hasContentLabel:content_label, smile.hasTraceID:self.trace.id}, how='first')
                if len(words)>0:
                    word = words[0]
                    this_spo[row["slot"]] = word.id

            spo = Spo.find_generate(subject_id=this_spo["s"], predicate_id=this_spo["p"], object_id=this_spo["o"], trace_id=self.trace.id)
            spo.from_ks_ars = self.ks_ar.id
            self.store_hypotheses.append(spo)

    def set_r_t(self):
        if self.df_spos is None:
            self.set_spos()

    def get_r_t(self):
        for spo_id in self.df_spos["spo_id"].unique():
            this_spo_df = self.df_spos[self.df_spos["spo_id"] == spo_id]
            this_spo = {"s": None, "p": None, "o": None}
            for i, row in this_spo_df.iterrows():
                content_label = row.token
                words = Word.search(props={smile.hasContentLabel:content_label,smile.hasTraceID:self.trace.id}, how='first')
                if len(words)>0:
                    this_spo[row["slot"]] = words[0].id
            # TODO: check this call params
            spo = Spo.find_generate(subject_id=this_spo["s"], predicate_id=this_spo["p"], object_id=this_spo["o"], trace_id=self.trace.id)
            spo.from_ks_ars = self.ks_ar.id
            self.store_hypotheses.append(spo)


    def set_r_e(self):
        if self.df_phrases is None:
            self.df_phrases = nlp_parser.gen_phrase_pos_rank(id1=self.trace.id, id2=self.ks_ar.id)

        # self.annotation_objects = nlp_parser.generate_annotations(id1=self.trace.id, id2=self.ks_ar.id, text=self.description, rule_weights=self.RULE_WEIGHTS)
        self.ner_objects = nlp_parser.collect_ner_tokens(id1=self.trace.id, id2=self.ks_ar.id, text=self.description, rule_weights=self.RULE_WEIGHTS)


    def get_r_e(self):

        for entity_type, matches in self.ner_objects.items():
            for tokens in matches:
                words = Word.search(props={smile.hasTraceID:self.trace_id, has(smile.hasContent):(tokens)}, how='all')
                entity_text = ' '.join([w.content for w in words])
                start = min([w.start for w in words])
                end = min([w.end for w in words])
                
                ner_certainty = float(self.RULE_WEIGHTS[(self.RULE_WEIGHTS["rule"] == "Aggregate") &
                                                    (self.RULE_WEIGHTS["cat"] == entity_type)]["accuracy"])

                assoc_phrase = Phrase.find_generate(content=entity_text, trace_id=self.trace.id, start=start,end=end)
                assoc_phrase.from_ks_ar_id = self.ks_ar.id
                # Add words one by one if they don't exist in assoc_phrase.words
                for word in words:
                    if word.id not in assoc_phrase.words:
                        assoc_phrase.words = word.id
                # assoc_phrase.words += words
                
                ner = Ner.generate(phrase_id=assoc_phrase.id,entity=self.MAPPING[entity_type],trace_id=self.trace.id, certainty=ner_certainty)
                ner.from_ks_ars = self.ks_ar.id
                self.store_hypotheses.append(ner)
        return self.store_hypotheses



    def set_phrases(self):
        self.df_phrases = nlp_parser.gen_phrase_pos_rank(id1=self.trace.id, id2=self.ks_ar.id)

    def get_phrases(self):
        for phrase_id in self.df_phrases["phrase_id"].unique():
            this_phrase_df = self.df_phrases[self.df_phrases["phrase_id"] == phrase_id]
            this_phrase_words = []
            this_phrase_texts = []
            this_phrase_starts = []
            this_phrase_ends = []
            for i, row in this_phrase_df.iterrows():
                content_label = row.token
                words = Word.search({smile.hasContentLabel:content_label,smile.hasTraceID:self.trace.id}, how='first')

                if len(words) > 0:
                    # word = word_db.Word.find_generate(content_label=content_label,trace_id=self.trace.id).first()
                    word = words[0]
                    word.from_ks_ars = self.ks_ar.id

                    this_phrase_words.append(word)
                    this_phrase_texts.append(word.content)
                    this_phrase_starts.append(word.start)
                    this_phrase_ends.append(word.end)

            if len(this_phrase_texts) >0:
                phrase_text = " ".join(this_phrase_texts)
                phrase_start = min(this_phrase_starts)
                phrase_end = max(this_phrase_ends)
                phrase = Phrase.find_generate(content=phrase_text, start=phrase_start, end=phrase_end,trace_id=self.trace.id)
                phrase.from_ks_ars = self.ks_ar.id
                phrase.words = this_phrase_words
                self.store_hypotheses.append(phrase)

        return self.store_hypotheses


if __name__ == '__main__':
    print('TextToSentences started')

    with smile:
        TextToSentences.process_ks_ars()

