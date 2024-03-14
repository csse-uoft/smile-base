import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList
from .hypothesis import Hypothesis

class Dep(Hypothesis):
    """
    A db Model class that defines the schema for the Dep data level.
    Base schema is extended from the Hypothesis class.

    ...
    Attributes
    ----------
    __tablename__ : str
        The name of the database table
    dep : SQLAlchemy.Column
        The dependency this data captures.
    from_id: SQLAlchemy.Column
        The ID of the subject word of this dependency
    to_id: SQLAlchemy.Column
        The ID of the object word of this dependency
    from_word : SQLAlchemy.relationship
        Relationship with the associated subject word
    tp_word : SQLAlchemy.relationship
        Relationship with the associated object word
    """
    klass = 'smile.Dep'
    super_relations = Hypothesis.relations    
    klass_relations = {
        'dep' : {'pred':smile.hasDepLabel, 'cardinality':'one'},
        'subject_word' : {'pred':smile.hasSubjectWord, 'cardinality':'one'},
        'object_word' : {'pred':smile.hasObjectWord, 'cardinality':'one'},
    }
    relations = {**klass_relations, **super_relations}

    def __init__(self, inst_id=None, inst=None, keep_db_in_synch=True) -> None:
        super().__init__(inst_id=inst_id, inst=inst, keep_db_in_synch=keep_db_in_synch)
       
    from py2graphdb.utils import db_utils
    def_file_path = os.path.dirname(db_utils.__file__) + '/_model_getters_setters_deleters.py'
    imported_code = open(def_file_path).read()
    exec(imported_code)

    def show(self):
        return self.dep

    @classmethod
    def find(cls, trace_id, dep, subject_id, object_id, request_id=None):
        """Find an existing dep query with the given parameters and return it.

        :param request_id: the trace id for this dep
        :param dep: the dependency this data captures
        :param from_word: word that this dependency has as the subject
        :param to_word: word that this dependency has as the object
        :return: found/generated dep query
        """
        inst =  SPARQLDict._get(klass=cls.klass, props={
            smile.hasTraceID        : trace_id,
            smile.hasDepLabel       : dep,
            smile.hasSubjectWord    : subject_id,
            smile.hasObjectWord    : object_id,
        })
        return cls(inst=inst) if inst else None

    @classmethod
    def generate(cls, trace_id, dep, subject_id, object_id, certainty=0, request_id=None):
        """Generate a new dep query with the given parameters and return it.

        :param request_id: the trace id for this dep
        :param dep: the dependency this data captures
        :param subject_id: word that this dependency has as the subject
        :param object_id: word that this dependency has as the object
        :param certainty: certainty level of this hypothesis
        :return: found/generated dep query
        """
        inst =  SPARQLDict._add(klass=cls.klass, props={
            smile.hasTraceID        : trace_id,
            smile.hasDepLabel       : dep,
            smile.hasSubjectWord    : subject_id,
            smile.hasObjectWord    : object_id,
            smile.hasCertainty      : certainty,
        })

        return cls(inst=inst) if inst else None

    @classmethod
    def find_generate(cls, trace_id, dep, subject_id, object_id, request_id=None, certainty=0):
        """Try to find and return an existing dep query with the given parameters.
         If there is none, generate a new query and return it.

        :param request_id: the trace id for this dep
        :param dep: the dependency this data captures
        :param from_word: word that this dependency has as the subject
        :param to_word: word that this dependency has as the object
        :return: found/generated dep query
        """
        node = cls.find( trace_id=trace_id,request_id = request_id, dep=dep, subject_id=subject_id, object_id=object_id)
        if node is None:
            node = cls.generate( trace_id=trace_id,request_id=request_id, dep=dep, subject_id=subject_id, object_id=object_id, certainty=certainty)
        return node

