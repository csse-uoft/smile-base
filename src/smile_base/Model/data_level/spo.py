import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList
from .hypothesis import Hypothesis

class Spo(Hypothesis):
    """
    A db Model class that defines the schema for the SPO data level.
    Base schema is extended from the Hypothesis class.

    ...

    Attributes
    ----------
    __tablename__ : str
        The name of the database table
    subject_id : SQLAlchemy.Column
        The ID of the Word used as the subject of this SPO.
    predicate_id : SQLAlchemy.Column
        The ID of the Word used as the predicate of this SPO.
    object_id : SQLAlchemy.Column
        The ID of the Word used as the object of this SPO.

    """
    klass = 'smile.Spo'
    super_relations = Hypothesis.relations
    klass_relations = {
        'subject'   : {'pred':smile.hasSubject, 'cardinality':'one'},
        'predicate' : {'pred':smile.hasPredicate, 'cardinality':'one'},
        'object'    : {'pred':smile.hasObject, 'cardinality':'one'},
        'rels'       : {'pred':smile.hasRels, 'cardinality':'many'},
    }
    relations = {**klass_relations, **super_relations}

    def __init__(self, inst_id=None, inst=None, keep_db_in_synch=True) -> None:
        super().__init__(inst_id=inst_id, inst=inst, keep_db_in_synch=keep_db_in_synch)
       
    from py2graphdb.utils import db_utils
    def_file_path = os.path.dirname(db_utils.__file__) + '/_model_getters_setters_deleters.py'
    imported_code = open(def_file_path).read()
    exec(imported_code)

    def show(self):
        return self.rels or ''

    @classmethod
    def find(cls, trace_id, subject_id, predicate_id, object_id, request_id=None):
        """Find an existing spo query with the given parameters and return it.

        :param request_id: the trace id for this SPO
        :param subject_id: the ID of the Word used as the subject of this SPO.
        :param predicate_id: the ID of the Word used as the predicate of this SPO.
        :param object_id: the ID of the Word used as the object of this SPO.
        :return: found/generated spo query
        """
        inst =  SPARQLDict._get(klass=cls.klass, props={
            smile.hasTraceID    : trace_id,
            smile.hasSubject    : subject_id,
            smile.hasPredicate  : predicate_id,
            smile.hasObject     : object_id,
        })
        return cls(inst=inst) if inst else None

    @classmethod
    def generate(cls, trace_id, subject_id, predicate_id, object_id, request_id=None, certainty=0):
        """Generate a new spo query with the given parameters and return it.

        :param request_id: the trace id for this SPO
        :param subject_id: the ID of the Word used as the subject of this SPO.
        :param predicate_id: the ID of the Word used as the predicate of this SPO.
        :param object_id: the ID of the Word used as the object of this SPO.
        :param certainty: certainty level of this hypothesis
        :return: found/generated spo query
        """
        inst =  SPARQLDict._add(klass=cls.klass, props={
            smile.hasTraceID    : trace_id,
            smile.hasSubject    : subject_id,
            smile.hasPredicate  : predicate_id,
            smile.hasObject     : object_id,
            smile.hasCertainty  : certainty,
        })
        return cls(inst=inst) if inst else None

    @classmethod
    def find_generate(cls, trace_id, subject_id, predicate_id, object_id, request_id=None, certainty=0):
        """Try to find and return an existing spo query with the given parameters.
         If there is none, generate a new query and return it.

        :param request_id: the trace id for this SPO
        :param subject_id: the ID of the Word used as the subject of this SPO.
        :param predicate_id: the ID of the Word used as the predicate of this SPO.
        :param object_id: the ID of the Word used as the object of this SPO.
        :param certainty: certainty level of this hypothesis
        :return: found/generated spo query
        """
        node = cls.find(trace_id=trace_id, subject_id=subject_id, predicate_id=predicate_id, object_id=object_id, request_id=request_id)
        if node is None:
            node = cls.generate( trace_id=trace_id, request_id=request_id, subject_id=subject_id, predicate_id=predicate_id, object_id=object_id, certainty=certainty)
        else:
            node.certainty = max(node.certainty, certainty)
            node.save()
        return node