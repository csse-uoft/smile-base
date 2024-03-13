import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList
from .hypothesis import Hypothesis

class Pos(Hypothesis):
    """
    A db Model class that defines the schema for the POS (Parts-of-Speech) data level.
    Base schema is extended from the Hypothesis class.

    ...

    Attributes
    ----------
    __tablename__ : str
        The name of the database table
    words : SQLAlchemy.relationship
        Relationship with the associated words
    poses : SQLAlchemy.Column
        Parts-of-speech assigned to text (e.g. "NN", "VBG", etc)

    """
    klass = 'smile.Pos'
    super_relations = Hypothesis.relations    
    klass_relations = {
        'words'     : {'pred':smile.hasWords, 'cardinality':'many'},
        'tag'       : {'pred':smile.hasTag, 'cardinality':'one'},
    }
    relations = {**klass_relations, **super_relations}

    def __init__(self, inst_id=None, inst=None, keep_db_in_synch=True) -> None:
        super().__init__(inst_id=inst_id, inst=inst, keep_db_in_synch=keep_db_in_synch)
       
    from py2graphdb.utils import db_utils
    def_file_path = os.path.dirname(db_utils.__file__) + '/_model_getters_setters_deleters.py'
    imported_code = open(def_file_path).read()
    exec(imported_code)


    def show(self):
        return self.tag or ''

    @classmethod
    def find(cls, trace_id, word_ids, pos_tag, request_id=None):
        """Find an existing word query with the given parameters and return it.

        :param request_id: the trace id for this phrase
        :param word: the word object associated to this hypothesis
        :param pos_tag: part of speech tag of this hypothesis
        :return: found/generated pos query
        """
        inst =  SPARQLDict._get(klass=cls.klass, props={
            smile.hasTraceID    : trace_id,
            smile.hasTag        : pos_tag,
            smile.hasWords      : word_ids,
            # cls.relations['request']['pred']:request_id,
        })

        return cls(inst=inst) if inst else None


    @classmethod
    def generate(cls, trace_id, word_ids, pos_tag, request_id=None, certainty=0):
        """Generate a new word query with the given parameters and return it.

        :param request_id: the trace id for this phrase
        :param word: the word object associated to this hypothesis
        :param pos_tag: part of speech tag of this hypothesis
        :param certainty: certainty level in float
        :return: found/generated pos query
        """
        inst =  SPARQLDict._add(klass=cls.klass, props={
            smile.hasTraceID    : trace_id,
            smile.hasTag        : pos_tag,
            smile.hasWords      : word_ids,
            smile.hasCertainty  : certainty,
            # cls.relations['request']['pred']:request_id,
        })
        return cls(inst=inst) if inst else None

    @classmethod
    def find_generate(cls, trace_id, word_ids, pos_tag, request_id=None, certainty=0):
        """Try to find and return an existing word query with the given parameters.
         If there is none, generate a new query and return it.

        :param request_id: the trace id for this phrase
        :param word: the word object associated to this hypothesis
        :param pos_tag: part of speech tag of this hypothesis
        :param certainty: certainty level in float
        :return: found/generated pos query
        """
        pos = cls.find( trace_id=trace_id, request_id=request_id, word_ids=word_ids, pos_tag=pos_tag)
        if pos is None:
            pos = cls.generate( trace_id=trace_id, word_ids=word_ids, pos_tag=pos_tag, certainty=certainty)
        return pos
