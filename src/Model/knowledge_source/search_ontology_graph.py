from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing, ThingClass 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from ...app.scripts import nlp_parser
    from ...Model.knowledge_source.knowledge_source import KnowledgeSource
    from ..controller.ks import Ks
    # from ..controller.ks import Trace, Request, KsInput, KsOutput, KSAR
    from ..data_level.text import Text
    from ..data_level.ner import Ner
    from ..data_level.rel import Rel

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from ...app.ontology.ontology_wrapper import OntologyWrapper


class SearchOntologyGraph(KnowledgeSource):

    def __init__(self, ks_ar, trace,hypothesis_ids=None):
        # fields = [v for v in Ks.ALL_KS_FORMATS.values() if v[0] == self.__class__.__name__][0]
        fields = [None, None, None, None]
        super().__init__(fields[1], fields[2], fields[3], trace, hypothesis_ids, ks_ar)

        self.hypotheses = None
        self.tmp_hypotheses = None
        self.ontology = None
        self.onto_G = None

    @classmethod
    def load_ontology_graph(cls):
        """Load and process ontology to be used for controlling ontology-related knowledge sources.
        """
        cls.ontology = OntologyWrapper()

        klass = cls.ontology.get_LogicModel()
        print(">>", klass)
        cls.ontology.collect_klass_properties(klass)
        onto_graph = cls.ontology.klasses
        onto_G = nx.DiGraph()
        for k,v in onto_graph.items():
            for prop,v2 in v.items():
                for child in v2:
                    onto_G.add_edge(k,child, label=prop)

        cls.onto_G = onto_G

        ner_G = nx.DiGraph()
        for k,v in cls.ontology.klass_mapper.items():
            for prop,v2 in v.items():
                for child in v2:
                    ner_G.add_edge(k,child, label=prop)
                    # nx.set_edge_attributes(ner_G,{(k,child):{'prop':prop}})

        cls.ner_G = ner_G
        cls.onto_M = nx.adjacency_matrix(cls.onto_G)
        cls.onto_M_labels = np.array(cls.onto_G.nodes())

    @classmethod
    def draw_graph(cls, figsize=(12,12)):
        if cls.onto_G is None:
            raise("cls.onto_G not set yet. Call load_onto_graph() first.")
            
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(cls.onto_G) # k regulates the distance between nodes
        nx.draw_networkx(cls.onto_G, with_labels=True, node_color='red', node_size=150, edge_cmap=plt.cm.Blues, pos = pos, font_weight='normal')
        nx.draw_networkx_edge_labels(cls.onto_G, pos=pos,edge_labels=nx.get_edge_attributes(cls.onto_G,'label'))
        plt.show()


    @classmethod
    def next_states(cls, current_state):
        try:
            ci = np.where(cls.onto_M_labels == current_state)[0]
            nis = np.where(np.array(cls.onto_M[ci].todense())[0] >0)[0]
            states = np.array(cls.onto_M_labels)[nis]
        except IndexError:
            states = np.array([])
        return states


    def set_input(self, ner):
        # ner.entity
        self.ner = ner


        G = self.ner_G

        ner_G = self.ner_G
        ner_klasses = []
        try:
            ner_klasses += [(n,ner, ner_G[n][ner.entity]) for n in ner_G.predecessors(ner.entity)]
        except nx.exception.NetworkXError:
            pass
        self.tmp_hypotheses = []
        for r1 in ner_klasses:
            klass = r1[0]
            next_klasses = self.next_states(klass)
            for next_klass in next_klasses:
                try:
                    next_ner_klasses = [(n, ner_G[next_klass][n]) for n in list(ner_G.successors(next_klass))]
                except nx.exception.NetworkXError:
                    continue
                for next_ner_klass in next_ner_klasses:
                    rel_ners = Ner.query.filter_by(entity=next_ner_klass[0]).all()
                    if len(rel_ners)>0:
                        # add predicate from next_ner_klass and append to hypotheses
                        self.tmp_hypotheses += [(next_ner_klass[1], rn) for rn in rel_ners]

    def get_outputs(self):
        self.hypotheses = []
        for rel_def, rel_ner in self.tmp_hypotheses:
            pred_str = str(rel_def['label'])
            self.hypotheses.append(Rel.find_generate(
                trace_id=self.trace.id, subject_id=self.ner.id, predicate_onto_rel=pred_str, object_id=rel_ner.id, certainty=0, predicate_id=None,request_id=None, spo_id=None)
            )

        return self.hypotheses

