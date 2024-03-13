import re, os, tqdm
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList

    from .knowledge_source import KnowledgeSource
    from ...app.scripts.qa import qa0
    from ..data_level.cids.organization import Organization
    from ..data_level.cids.program import Program
    from ..data_level.cids.beneficial_stakeholder import BeneficialStakeholder
    from ..data_level.cids.outcome import Outcome
    # from ..data_level.CatchmentArea"         : 'catchment_area',

    from ..data_level.phrase import Phrase
    from ..data_level.text import Text
    from ..data_level.sentence import Sentence
    from ..data_level.hypothesis import Hypothesis
    from ..controller.ks import Ks
    from ..controller.ks_ar import KSAR
    from ..controller.trace import Trace

from py2graphdb.ontology.operators import *

# from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer
import time
from ...app.scripts.misc_lib import *

class Qa0Ner(KnowledgeSource):
    """
    A knowledge source class that processes QA0 Ner

    Attributes
    ----------
    description: str
        context description that will be the input of the model
    entity: str
        entity in interest
    qa0s: qa1.QA1
        qa1 use case module instance that keeps track of all qa flow
    output_dic: dict
        dictionary representation of the knowledge source outputs

    Methods
    -------
    set_input(description)
        set inputs to the model class, preparing to run the model
    get_outputs()
        run the model to get the formatted outputs

    """

    # TODO: update below
    ENTITIES = {
        Organization          : 'program_name',
        Program               : 'program_name',
        # 'Client'                : 'client',
        BeneficialStakeholder : 'client',
        # 'NeedSatisfier'         : 'need_satisfier',
        Outcome               : 'stakeholder_outcome',
        # 'StakleholderOutcome'   : 'stakeholder_outcome',
        # "CatchmentArea"         : 'catchment_area',
    }

    def __init__(self, hypothesis_ids, ks_ar, trace):
        fields = [v for v in Ks.ALL_KS_FORMATS.values() if v[0] == Ks(ks_ar.ks).py_name][0]
        # fields = [v for v in Ks.ALL_KS_FORMATS.values() if v[0] == self.__class__.__name__][0]
        super().__init__(fields[1], fields[2], fields[3], trace, hypothesis_ids, ks_ar)

        self.description = None
        self.entity = None
        self.qa0s = None
        self.output_dic = {}

        
    @classmethod
    def process_ks_ars(cls):
        """
        A class method that processes all the ks_ars with py_name='Qa0Ner' and status=0.

        :param cls: The class itself (implicit parameter).
        :type cls: type
        :return: None
        """
        while True:
            # Hard coded to get the ks_ar with id=4           
            # Get the ks_ar with py_name='Qa0Ner' and status=0
            time.sleep(1)
            kss = Ks.search(props={smile.hasPyName:f"Qa0Ner"}, how='all')
            ks_ar = None
            for ks in kss:
                print(4,'ks', ks)
                ks_ars = KSAR.search(props={smile.hasKS:ks.id, smile.hasKSARStatus:0}, how='first')
                print(5, ks_ars)
                if len(ks_ars) > 0:
                    ks_ar = ks_ars[0]
                    print(6, ks_ar)
                    break
                    
            print(7, ks_ar)
            if ks_ar is None:
                continue

            print(8, ks_ar)
            print(f"Processing ks_ar with id: {ks_ar.id}")

            # Get the hypothesis ids from the ks_ar
            in_hypo_ids = ks_ar.input_hypotheses

            if len(in_hypo_ids) != 1:
                raise(Exception(f"Bad Input Hypothesis Count {len(in_hypo_ids)}"))

            in_hypo = Hypothesis(inst_id=in_hypo_ids[0])
            in_hypo.cast_to_graph_type()
            if not isinstance(in_hypo, (smile.Sentence, smile.Text)): #check if Phras
                raise(Exception(f"Bad Input Hypothesis Type {type(in_hypo)}"))
            
            # Get the trace from the ks_ar
            trace = Trace(inst_id=ks_ar.trace)
            
            # Construct an instance of the ks_object
            ks_object = cls(hypothesis_ids=in_hypo_ids, ks_ar=ks_ar, trace=trace)
            
            # Call ks_object.set_input() with the necessary parameters
            ks_ar.ks_status = 1
            output_klass = eval(ks.outputs[0])
            ks_object.set_input(description=in_hypo.content, output_klass=output_klass)

            ks_ar.ks_status = 2
            hypotheses = ks_object.get_outputs()
            ks_ar.keep_db_in_synch = False
            trace.keep_db_in_synch = False
            for hypo in hypotheses:
                ks_ar.hypotheses = hypo.id 
                trace.hypotheses = hypo.id
                if isinstance(hypo, (smile.Word, smile.Phrase)):
                    if isinstance(in_hypo, smile.Sentence):
                        hypo.sentence = in_hypo.id
                    elif isinstance(in_hypo, smile.Text):
                        hypo.text = in_hypo.id
                    if isinstance(hypo, smile.Phrase):
                        in_hypo.phrases = hypo.id
                    elif isinstance(hypo, smile.Word):
                        in_hypo.words = hypo.id
            ks_ar.save()
            trace.save()
            ks_ar.keep_db_in_synch = True
            trace.keep_db_in_synch = True

            LOG_FILE_TEMPLATE = CONFIG.LOG_DIR+'smile_trace_log.txt'
            filename = LOG_FILE_TEMPLATE.replace('.txt', f"_{trace.id}.txt")
            ks_ar.summary(filename=filename)

            ks_ar.ks_status = 3
            
    def set_input(self, description:str, output_klass):
        """Run qa0 ner knowledge source with the given description (str).
        :param description: context description
        :return: updated qa0 object
        """
        self.store_hypotheses = []
        self.qa0s = {}
        self.output_results = []
        self.description = description
        tmp_results = []
        for sent_start, sent_end in PunktSentenceTokenizer().span_tokenize(description):
            sent = description[sent_start:sent_end]
            entity = self.ENTITIES[output_klass]
            print(10, sent, type(sent))
            print(11, entity, type(entity))
            res_qa0 = qa0.QA0(context=sent, entity=entity)
            tmp_results.append([entity, res_qa0, sent_start])

        for entity, res_qa0, sent_start in tmp_results:
            self.output_results.append([res_qa0.run_qa(), sent_start])

        return self.output_results

    def get_outputs(self):
        """
        add newly created hypothese to database
        :return: all the hypotheses created from this ks
        """
        for res_dict, sent_start in self.output_results:
            for entity,res_qa0 in res_dict.items():
                text = res_qa0["answer"]
                start = res_qa0["start"] + sent_start
                end = res_qa0["end"] + sent_start
                certainty = res_qa0["score"]
                if certainty > 0:
                    phrase = Phrase.find_generate(
                        content=text, start=start, end=end,trace_id=self.trace.id, certainty=certainty)
                    phrase.from_ks_ars = self.ks_ar.id
                    klass = [k for k,v in self.ENTITIES.items() if v == entity][0]
                    concept = klass.generate(phrase_id=phrase.id, trace_id=self.trace.id, certainty=certainty)
                    concept.from_ks_ars = self.ks_ar.id
                    phrase.concepts = concept.id
                    # concept.phrases = phrase.id
                    self.store_hypotheses.append(phrase)
                    self.store_hypotheses.append(concept)

        return self.store_hypotheses





if __name__ == '__main__':
    print('Qa0Ner script started')

    with smile:
        Qa0Ner.process_ks_ars()
