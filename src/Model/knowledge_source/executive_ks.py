import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList

    from .knowledge_source import KnowledgeSource
    from ...app.scripts.qa import qa0
    from ..data_level.ner import Ner
    from ..data_level.phrase import Phrase
    from ..data_level.text import Text
    from ..data_level.hypothesis import Hypothesis
    from ..controller.ks import Ks
    from ..controller.ks_ar import KSAR
    from ..controller.trace import Trace

# from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer
import tqdm
import time

class ExecutivePlane(KnowledgeSource):
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


    def __init__(self, ks_ar, trace,hypothesis_ids=None):
        # fields = [v for v in Ks.ALL_KS_FORMATS.values() if v[0] == self.__class__.__name__][0]
        fields = [None, None, None, None]
        super().__init__(fields[1], fields[2], fields[3], trace, hypothesis_ids, ks_ar)

        self.description = None
        self.entity = None
        self.qa0s = None
        self.output_dic = {}
        # TODO: update below
        self.entity_abb = {"pr": "program", "ns": "need satisfier", "cl": "client", "no": "need"}
        
    @classmethod
    def get_inputs(cls):
        """
        A class method that processes all the ks_ars with py_name='Qa0Ner' and status=0.

        :param cls: The class itself (implicit parameter).
        :type cls: type
        :return: None
        """
        print('Starting process_ks_ars method in Qa0Ner class')
        print('----------------------------------------------')
        while True:
            # Hard coded to get the ks_ar with id=4
            # ks_ar = KSAR.query.filter_by(status=0, ks_id=4).first()
            
            # Get the ks_ar with py_name='Qa0Ner' and status=0
            time.sleep(1)
            ks = Ks.search(props={smile.hasPyName:'Qa0Ner'}, how='first')
            if len(ks) >0:
                ks = ks[0]
            else:
                continue
            ks_ar = KSAR.search(props={smile.hasKS:ks.id, smile.hasKSARStatus:0}, how='first')
            if len(ks_ar) > 0:
                ks_ar = ks_ar[0]
                print(f"Processing ks_ar with id: {ks_ar.id}")

                # Get the hypothesis ids from the ks_ar
                hypo_ids = ks_ar.input_hypotheses

                if len(hypo_ids) != 1:
                    raise(Exception(f"Bad Input Hypothesis Count {len(hypo_ids)}"))

                hypo = Hypothesis(inst_id=hypo_ids[0])
                hypo.cast_to_graph_type()
                if not isinstance(hypo, smile.Text): #check if Phras
                    raise(Exception(f"Bad Input Hypothesis Type {type(hypo)}"))
             
                # Get the trace from the ks_ar
                trace = Trace(inst_id=ks_ar.trace)
                
                # Construct an instance of the ks_object
                ks_object = cls(hypothesis_ids=hypo_ids, ks_ar=ks_ar, trace=trace)
                
                # Call ks_object.set_input() with the necessary parameters
                ks_object.set_input(description=hypo.content)

                ks_ar.ks_status = 2
                # ks_ar.update(ignore_object=False)
                # print(f'finished processing instances set_input')
                
                # Call ks_object.get_outputs()
                hypotheses = ks_object.get_outputs()
                # ks_ar = ks_ar.reload()
                # ks_ar.attributes['object'] = ks_object
                # ks_ar.object = ks_object
                ks_ar.ks_status = 3
                # ks_ar.update(ignore_object=False)
                # print(f'finished processing instances get_outputs')
                
                print(f'finished processing ks_ar with id: {ks_ar.id}')
                
            

    def set_input(self, description:str):#, entity:str):
        """Run qa0 ner knowledge source with the given description (str).
        :param description: context description
        :return: updated qa0 object
        """
        self.hypotheses = []
        self.qa0s = {}
        self.output_results = []
        self.description = description

        # print('start1')
        tmp_results = []
        for sent_start, sent_end in PunktSentenceTokenizer().span_tokenize(description):
            sent = description[sent_start:sent_end]
            for entity in ["pr", "cl", "ns", "no", "ca"]:
                res_qa0 = qa0.QA0(context=sent, entity=entity)
                tmp_results.append([entity, res_qa0, sent_start])

        # print('start2')
        # for entity, res_qa0, sent_start in tqdm.tqdm(tmp_results, total=len(tmp_results)):
        for entity, res_qa0, sent_start in tmp_results:
            self.output_results.append([res_qa0.run_qa(), sent_start])
        # print('end9')
        return self.output_results
        # for entity, QA0 in self.qa0s.items():
        #     self.output_dic.update(QA0.run_qa())
        # return self.output_dic

    def get_outputs(self):
        """
        add newly created hypothese to database
        :return: all the hypotheses created from this ks
        """
        # self.ks_ar._hypotheses_ids'] = []
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
                    # phrase.update()
                    print(f'We have phrase with id {phrase.id} and words + content {[(w.id, w.content) for w in phrase.words]}')
                    ner = Ner.generate(phrase_id=phrase.id, entity=self.MAPPING[entity],trace_id=self.trace.id, certainty=certainty)
                    ner.from_ks_ars = self.ks_ar.id
                    # ner.update()
                    self.hypotheses.append(phrase)
                    self.hypotheses.append(ner)

        # self.ks_ar.attributes['output_hypotheses_ids'] = [[hypo.id, hypo.__class__.__name__] for hypo in self.hypotheses]
        # self.ks_ar.update()
        return self.hypotheses


if __name__ == '__main__':
    print('Qa0Ner script started')
    # db = Model.db

    with smile:
        Qa0Ner.process_ks_ars()
