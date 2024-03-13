import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList
from .hypothesis import Hypothesis

class CoRef(Hypothesis):
    """
    A db Model class that defines the schema for the Ner data level.
    Base schema is extended from the Hypothesis class.

    ...

    Attributes
    ----------
    __tablename__ : str
        The name of the database table
    word_id : SQLAlchemy.Column
        The ID of the Word that has a coreference (e.g. "he").
    ref_word_id : SQLAlchemy.Column
        The ID of the Word that references that linked to word_id(e.g. "Bob")
    word : SQLAlchemy.relationship
        Relationship with the associated word
    ref_word : SQLAlchemy.relationship
        Relationship with the associated coreference word

    """
    klass = 'smile.CoRef'
    super_relations = Hypothesis.relations
    klass_relations = {
        'coref_word' : {'pred':smile.hasCoRefWord, 'cardinality':'one'},
        'ref_word' : {'pred':smile.hasRefWord, 'cardinality':'one'},
    }
    relations = {**klass_relations, **super_relations}

    def __init__(self, inst_id=None, inst=None, keep_db_in_synch=True) -> None:
        super().__init__(inst_id=inst_id, inst=inst, keep_db_in_synch=keep_db_in_synch)
       
    from py2graphdb.utils import db_utils
    def_file_path = os.path.dirname(db_utils.__file__) + '/_model_getters_setters_deleters.py'
    imported_code = open(def_file_path).read()
    exec(imported_code)

    def show(self):
        coref = Hypothesis(inst_id=self.coref_word).cast_to_graph_type() if self.coref_word else ''
        ref = Hypothesis(inst_id=self.coref_word).cast_to_graph_type() if self.ref_word else ''
        return f"{coref} {ref}"

    @classmethod
    def find(cls, 
        trace_id,
        coref_word_id, ref_word_id,
        request_id=None):
        """Find an existing coref query with the given parameters and return it.

        :param request_id: the trace id for this phrase
        :param word: the word object that this hypothesis refers to
        :param ref_word: the word object this hypothesis co-refers to
        :return: found/generated coref query
        """
        inst =  SPARQLDict._get(klass=cls.klass, props={
            smile.hasTraceID:trace_id,
            smile.hasCoRefWord:coref_word_id,
            smile.hasRefWord:ref_word_id,
            # cls.relations['request']['pred']:request_id,
        })
        return cls(inst=inst) if inst else None

    @classmethod
    def generate(cls, 
        trace_id,
        coref_word_id, ref_word_id, certainty=0,request_id=None, ):
        """Generate a new coref query with the given parameters and return it.

        :param request_id: the trace id for this phrase
        :param word: the word object that this hypothesis refers to
        :param ref_word: the word object this hypothesis co-refers to
        :param certainty: certainty level in float
        :return: found/generated coref query
        """
        inst =  SPARQLDict._add(klass=cls.klass, props={
            smile.hasTraceID:trace_id,
            smile.hasCoRefWord:coref_word_id,
            smile.hasRefWord:ref_word_id,
            smile.hasCertainty:certainty,
            # cls.relations['request']['pred']:request_id,
        })

        return cls(inst=inst) if inst else None

    @classmethod
    def find_generate(cls, trace_id, coref_word_id, ref_word_id, certainty=0, request_id=None):
        """Try to find and return an existing coref query with the given parameters.
         If there is none, generate a new query and return it.

        :param request_id: the trace id for this phrase
        :param word: the word object that this hypothesis refers to
        :param ref_word: the word object this hypothesis co-refers to
        :param certainty: certainty level in float
        :return: found/generated coref query
        """
        node = cls.find(
            request_id=request_id,  trace_id=trace_id,
            coref_word_id=coref_word_id, ref_word_id=ref_word_id)
        if node is None:
            node = cls.generate(
                request_id=request_id,  trace_id=trace_id,
                coref_word_id=coref_word_id, ref_word_id=ref_word_id, certainty=certainty)
        return node

