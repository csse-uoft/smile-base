from __future__ import annotations
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing, ThingClass 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from .knowledge_source import KnowledgeSource
    from ..controller.ks import Ks
    # from ..controller.request import Request
    from ..data_level.text import Text

class SearchTextGraph(KnowledgeSource):

    def __init__(self, hypothesis_ids, ks_ar, trace):
        # fields = [v for v in Ks.ALL_KS_FORMATS.values() if v[0] == self.__class__.__name__][0]
        fields = [None, None, ]
        super().__init__(fields[1], fields[2], fields[3], trace, hypothesis_ids, ks_ar)

        self.input_klass = None
        self.requests = None

    TEXT_GRAPH = {
        'Text': {'hasPart': ['Word', 'Phrase']},
        'Word': {'hasPart': ['Pos'], 'partOf': ['Phrase']},
        'Pos': {'hasPart': ['Deo'], 'partOf': ['CoRef']},
        'CoRef': {'connects': ['Word']},
        'Dep': {'hasPart':['Word'], 'translates': ['Phrase', 'Spo']},
        'Phrase': {'hasPart': ['Ner', 'Word']},
        'Spo': {'hasPart': ['Ner']},
        'Ner': {'partOf': ['Rel']},
        'Rel': {},
    }

    @classmethod
    def draw_graph(cls, figsize=(12,12)):
        G = cls.text_G
        if G is None:
            raise("cls.text_G not set yet. Call load_text_graph() first.")
            
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(G) # k regulates the distance between nodes
        nx.draw_networkx(G, with_labels=True, node_color='red', node_size=150, edge_cmap=plt.cm.Blues, pos = pos, font_weight='normal')
        nx.draw_networkx_edge_labels(cls.text_G, pos=pos,edge_labels=nx.get_edge_attributes(G,'label'))
        plt.show()

    @classmethod
    def load_text_graph(cls):
        """Load and process text-parsing graph, to be used as controlling text-related knowledge sources.
        """
        # klass = 'Text'
        text_G = nx.DiGraph()
        for k,v in cls.TEXT_GRAPH.items():
            for prop,v2 in v.items():
                for child in v2:
                    text_G.add_edge(k,child, label=prop)

        cls.text_G = text_G
        cls.text_M = nx.adjacency_matrix(cls.text_G)
        cls.text_M_labels = np.array(cls.text_G.nodes())

    @classmethod
    def next_states(cls, current_state):
        ci = np.where(cls.text_M_labels == current_state)[0]
        nis = np.where(np.array(cls.text_M[ci].todense())[0] >0)[0]
        states = np.array(cls.text_M_labels)[nis]
        return states

    def set_input(self, input_klass, ks_ar, hypothesis=None, request=None):
        
        self.input_klass = input_klass
        self.request = request
        self.hypothesis = hypothesis
        self.ks_ar = ks_ar
        self.ks_ar.attributes['object'] = self

    def get_outputs(self):
        self.requests = []
        # for child in self.text_G.neighbors(self.input_klass):
        #     self.requests.append(Request(input=self.input_klass, output=child, trace=self.trace, parent_ks_ar_id=self.ks_ar.id).add())
        return self.requests