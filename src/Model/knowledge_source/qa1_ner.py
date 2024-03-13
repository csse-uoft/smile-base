import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList

    from .knowledge_source import KnowledgeSource
    from ...app.scripts.qa import qa1
    from ..data_level.cids.organization import Organization
    from ..data_level.cids.program import Program
    from ..data_level.cids.beneficial_stakeholder import BeneficialStakeholder
    from ..data_level.cids.outcome import Outcome

    from ..data_level.phrase import Phrase
    from ..data_level.text import Text
    from ..data_level.sentence import Sentence
    from ..data_level.hypothesis import Hypothesis
    from ..controller.ks import Ks
    from ..controller.ks_ar import KSAR
    from ..controller.trace import Trace

# from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer
import tqdm
import time
from ...app.scripts.misc_lib import *


class Qa1Ner(KnowledgeSource):
    """
    A knowledge source class that processes QA1 Ner

    Attributes
    ----------
    description: str
        context description that will be the input of the model
    entity: str
        entity in interest
    qa1s: qa1.QA1
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


    ENTITIES = {
        Organization          : 'program_name',
        Program               : 'program_name',
        # Client                : 'client',
        BeneficialStakeholder : 'client',
        # NeedSatisfier         : 'need_satisfier',
        Outcome               : 'outcome',
        # StakleholderOutcome   : 'stakeholder_outcome',
        # CatchmentArea         : 'catchment_area',
    }

    def __init__(self, hypothesis_ids, ks_ar, trace):
        fields = [v for v in Ks.ALL_KS_FORMATS.values() if v[0] == self.__class__.__name__][0]
        super().__init__(fields[1], fields[2], fields[3], trace, hypothesis_ids, ks_ar)

        self.description = None
        self.entity = None
        self.qa1s = None
        self.output_dic = {}
        # TODO: update below
        
    @classmethod
    def process_ks_ars(cls):
        """
        A class method that processes all the ks_ars with py_name='Qa1Ner' and status=0.

        :param cls: The class itself (implicit parameter).
        :type cls: type
        :return: None
        """
        while True:
            # Hard coded to get the ks_ar with id=4           
            # Get the ks_ar with py_name='Qa1Ner' and status=0
            time.sleep(1)
            kss = Ks.search(props={smile.hasPyName:f"Qa1Ner"}, how='all')
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

            if len(in_hypo_ids) < 2 :
                raise(Exception(f"Bad Input Hypothesis Count {len(in_hypo_ids)}"))

            in_hypos = [Hypothesis(inst_id=hypo_id).cast_to_graph_type() for hypo_id in in_hypo_ids]
            content_hypo = None
            concept_hypo = None
            for in_hypo in in_hypos:
                print(f" in hypo {type(in_hypo)}:{in_hypo}")
                if isinstance(in_hypo, (smile.Sentence, smile.Text)): #check if Phrase
                    content_hypo = in_hypo
                    print('found text', content_hypo)
                elif type(in_hypo) in cls.ENTITIES.keys(): #check if Concept
                    cls.ENTITIES[type(in_hypo)]
                    concept_hypo = in_hypo
                    print('found concept', concept_hypo)
            print(2, concept_hypo, content_hypo)
            if concept_hypo is None or content_hypo is None:
                raise(Exception(f"Bad Input Hypothesis Type {[type(in_hypo) for in_hypo in in_hypos]}"))
            
            # Get the trace from the ks_ar
            trace = Trace(inst_id=ks_ar.trace)
            
            # Construct an instance of the ks_object
            ks_object = cls(hypothesis_ids=in_hypo_ids, ks_ar=ks_ar, trace=trace)
            
            # Call ks_object.set_input() with the necessary parameters
            ks_ar.ks_status = 1
            output_klass = eval(ks.outputs[0])
            ks_object.set_input(description=content_hypo.content, in_hypo=concept_hypo, output_klass=output_klass)

            ks_ar.ks_status = 2
            hypotheses = ks_object.get_outputs()
            ks_ar.keep_db_in_synch = False
            trace.keep_db_in_synch = False
            # for hypo in hypotheses:
            #     ks_ar.hypotheses = hypo.id 
            #     trace.hypotheses = hypo.id
            #     if isinstance(hypo, (smile.Word, smile.Phrase)):
            #         if isinstance(in_hypo, smile.Sentence):
            #             hypo.sentence = in_hypo.id
            #         elif isinstance(in_hypo, smile.Text):
            #             hypo.text = in_hypo.id
            #         if isinstance(hypo, smile.Phrase):
            #             in_hypo.phrases = hypo.id
            #         elif isinstance(hypo, smile.Word):
            #             in_hypo.words = hypo.id
            ks_ar.save()
            trace.save()
            ks_ar.keep_db_in_synch = True
            trace.keep_db_in_synch = True

            LOG_FILE_TEMPLATE = CONFIG.LOG_DIR+'smile_trace_log.txt'
            filename = LOG_FILE_TEMPLATE.replace('.txt', f"_{trace.id}.txt")
            ks_ar.summary(filename=filename)

            ks_ar.ks_status = 3
                
    def set_input(self, description:str, in_hypo, output_klass=None):
        """Run qa1 ner knowledge source with the given description (str).
        :param description: context description
        :return: updated qa1 object
        """
        input_klass = type(in_hypo)
        self.store_hypotheses = []
        self.qa1s = {}
        self.output_results = []
        self.description = description
        entity0 = self.ENTITIES[input_klass]
        entity1 = self.ENTITIES[output_klass]
        
        res_qa1 = qa1.QA1(context=description, entity=entity0)
        tmp_results = []
        res_qa1.update_given_ner(ent_type=entity1, givens={description:in_hypo.certainty})
        tmp_results.append([entity0, in_hypo, res_qa1])

        self.output_results.append(res_qa1.run_qa(ner=False))

        return self.output_results

    def get_outputs(self):
        """
        add newly created hypothese to database
        :return: all the hypotheses created from this ks
        """
        for res_dict in self.output_results:
            print(res_dict)
            for entity,res_qa1 in res_dict.items():
                text = res_qa1["answer"]
                start = res_qa1["start"]
                end = res_qa1["end"]
                certainty = res_qa1["score"]
                if certainty > 0:
                    phrase = Phrase.find_generate(
                        content=text, start=start, end=end,trace_id=self.trace.id, certainty=certainty)
                    phrase.from_ks_ars = self.ks_ar.id

                    klass = [k for k,v in self.ENTITIES.items() if v == entity][0]
                    concept = klass.generate(phrase_id=phrase.id, trace_id=self.trace.id, certainty=certainty)
                    concept.from_ks_ars = self.ks_ar.id
                    phrase.concepts = concept.id
                    self.store_hypotheses.append(phrase)
                    self.store_hypotheses.append(concept)

        return self.store_hypotheses





if __name__ == '__main__':
    print('Qa1Ner script started')

    with smile:
        Qa1Ner.process_ks_ars()
