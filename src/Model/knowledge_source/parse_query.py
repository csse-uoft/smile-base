import re, os, pandas as pd
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList

    from .knowledge_source      import KnowledgeSource
    from ..data_level.hypothesis import Hypothesis
    from ..data_level.query      import Query
    from ..data_level.text      import Text
    from ..controller.ks   import Ks
    from ..controller.ks_ar   import KSAR
    from ..controller.trace    import Trace


import time


class ParseQuery(KnowledgeSource):
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

        self.query = None
        self.store_hypotheses = []

    @classmethod
    def process_ks_ars(cls):
        """
        A class method that processes all the ks_ars with py_name='ParseTokenize' and status=0.

        :param cls: The class itself (implicit parameter).
        :type cls: type
        :return: None
        """
        while True:
            
            ks = Ks.search(props={smile.hasPyName:'ParseQuery'}, how='first')
            if len(ks) >0:
                ks = ks[0]
            else:
                continue
            ks_ar = KSAR.search(props={smile.hasKS:ks.id, smile.hasKSARStatus:0}, how='first')
            if len(ks_ar) > 0:
                ks_ar = ks_ar[0]
                cls.logger(trace_id=ks_ar.trace, text=f"Processing ks_ar with id: {ks_ar.id}")

                # Get the hypothesis ids from the ks_ar
                hypo_ids = ks_ar.input_hypotheses
                if len(hypo_ids) != 1:
                    raise(Exception(f"Bad Input Hypothesis Count {len(hypo_ids)}"))

                hypo = Hypothesis(inst_id=hypo_ids[0])
                hypo.cast_to_graph_type()
                if not isinstance(hypo, smile.Query): #check if Phrase
                    raise(Exception(f"Bad Input Hypothesis Type {type(hypo)}"))

                # Get the trace from the ks_ar
                trace = Trace(inst_id=ks_ar.trace)
                
                # Construct an instance of the ks_object
                ks_object = cls(hypothesis_ids=hypo_ids, ks_ar=ks_ar, trace=trace)
                
                # Call ks_object.set_input() with the necessary parameters
                ks_ar.ks_status = 1
                ks_object.set_input(query=hypo.content)
                
                ks_ar.ks_status = 2               
                hypotheses = ks_object.get_outputs()
                ks_ar.keep_db_in_synch = False
                trace.keep_db_in_synch = False
                for hypo in hypotheses:
                    ks_ar.hypotheses = hypo.id 
                    trace.hypotheses = hypo.id
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

    def clean_input(self, content):
        text = re.sub(r'([a-z])\.([A-Z])', r'\1. \2', content)
        # replace acronyms with ABC
        for match in re.findall(r'\b(?:[A-Z]\.+\s+){2,}',text):   # "A. B. C."
            text = re.sub(match, match.replace('. ','')+' ', text)
        for match in re.findall(r'\b(?:[A-Z]\.+){2,}',text):      # "A.B.C."
            text = re.sub(match, match.replace('.','')+' ', text)
        for match in re.findall(r'\b(?:[A-Z]\s+){2,}',text):      # "A B C"
            text = re.sub(match, match.replace(' ','')+' ', text)

        # make misc replacements
        text = text.strip().                \
                replace('as well as','and').\
                replace("&amp;", " and ").  \
                replace("–", ' ').          \
                replace('-',' ').           \
                replace('%',' percent ').   \
                replace('+',' plus ').      \
                replace("“","'").          \
                replace("”","'").          \
                replace("\"","'").          \
                replace("\n",". ").          \
                replace("\r",". ").          \
                strip()

        text = re.sub(r'\.+', '.', text)                
        return text

    def set_input(self, query):
        self.query = query

    def get_outputs(self):
        content = self.clean_input(content=self.query)
        text = Text.find_generate(content=content, trace_id=self.trace.id)
        text.from_ks_ars = self.ks_ar.id
        self.store_hypotheses = [text]

        return self.store_hypotheses


if __name__ == '__main__':
    print('ParseQuery started')

    with smile:
        ParseQuery.process_ks_ars()

