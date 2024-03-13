import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList

    from .knowledge_source import KnowledgeSource
    from ..data_level.ner import Ner
    from ..data_level.phrase import Phrase
    from ..data_level.text import Text
    from ..data_level.query import Query
    from ..data_level.hypothesis import Hypothesis
    from ..controller.ks import Ks
    from ..controller.ks_ar import KSAR
    from ..controller.trace import Trace

# from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer
import tqdm
import time

class ControllerKS(KnowledgeSource):
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

    MAPPING = {'pr':'program_name', 'cl':'client', 'ns':'need_satisfier', 'no':'stakeholder_outcome', 'ca':'catchment_area'}

    def __init__(self, hypothesis_ids, ks_ar, trace):
        fields = [v for v in Ks.ALL_KS_FORMATS.values() if v[0] == self.__class__.__name__][0]
        super().__init__(fields[1], fields[2], fields[3], trace, hypothesis_ids, ks_ar)

        # self.description = None
        # self.entity = None
        # self.qa0s = None
        # self.output_dic = {}
        # TODO: update below
        # self.entity_abb = {"pr": "program", "ns": "need satisfier", "cl": "client", "no": "need"}
        
    @classmethod
    def process_ks_ars(cls):
        pass
                
    def set_input(self, description:str):

        return self.output_results

    def get_outputs(self):
        return self.store_hypotheses





if __name__ == '__main__':
    print('Controller KS script started')

    with smile:
        ControllerKS.process_ks_ars()
