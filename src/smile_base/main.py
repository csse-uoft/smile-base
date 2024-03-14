import re, os, glob
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)

with smile:
    from .ontology.namespaces import ic, geo, cids, org, time, schema, sch, activity, landuse_50872, i72, owl
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList

    from .ontology.extra import *
    
    from .Model.knowledge_source.knowledge_source import KnowledgeSource
    
    from .Model.controller.ks import Ks
    from .Model.controller.ks_ar import KSAR
    from .Model.controller.ks_input import KsInput
    from .Model.controller.ks_output import KsOutput
    from .Model.controller.trace import Trace

    from .Model.data_level.hypothesis import Hypothesis
    from .Model.data_level.coref import CoRef
    from .Model.data_level.dep import Dep
    from .Model.data_level.ner import Ner
    from .Model.data_level.phrase import Phrase
    from .Model.data_level.pos import Pos
    from .Model.data_level.query import Query
    from .Model.data_level.rel import Rel
    from .Model.data_level.sentence import Sentence
    from .Model.data_level.spo import Spo
    from .Model.data_level.text import Text
    from .Model.data_level.word import Word

    from .Model.data_level.cids.beneficial_stakeholder import BeneficialStakeholder
    from .Model.data_level.cids.characteristic import Characteristic
    from .Model.data_level.cids.code import Code
    from .Model.data_level.cids.input import Input
    from .Model.data_level.cids.logic_model import LogicModel
    from .Model.data_level.cids.organization import Organization
    from .Model.data_level.cids.outcome import Outcome
    from .Model.data_level.cids.output import Output
    from .Model.data_level.cids.program import Program
    from .Model.data_level.cids.service import Service
    from .Model.data_level.cids.stakeholder import Stakeholder
    