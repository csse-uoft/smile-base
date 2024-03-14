import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
from ....ontology.namespaces import ic, geo, cids, org, time, schema, sch, activity, landuse_50872, i72, owl
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList
from ..hypothesis import Hypothesis

class Characteristic(Hypothesis,cids.Characteristic):
    """
    A db Model class that defines the schema for the Ner data level.
    Base schema is extended from the Hypothesis class.

    ...

    Attributes
    ----------
    __tablename__ : str
        The name of the database table
    phrase_id : SQLAlchemy.Column
        The ID of the Phrase used as the subject of the NER hypothesis
    phrase : SQLAlchemy.relationship
        Relationship with the associated phrase

    """
    klass = 'smile.Characteristic'
    super_relations = Hypothesis.relations
    klass_relations = {
        'phrase' : {'pred':smile.hasPhrase, 'cardinality':'one'},
        'name'  : {'pred':org.hasName,'cardinality':'many'},
        'desc': {'pred':cids.hasDescription, 'cardinality':'many'},
        'code': {'pred':cids.hasCode, 'cardinality':'many'},
        'time': {'pred':time.hasTime, 'cardinality':'one'},
    }

    relations = {**klass_relations, **super_relations}

    def __init__(self, inst_id=None, inst=None, keep_db_in_synch=True) -> None:
        super().__init__(inst_id=inst_id, inst=inst, keep_db_in_synch=keep_db_in_synch)
       
    from py2graphdb.utils import db_utils
    def_file_path = os.path.dirname(db_utils.__file__) + '/_model_getters_setters_deleters.py'
    imported_code = open(def_file_path).read()
    exec(imported_code)


    def show(self):
        return self.klass or ''


    @classmethod
    def find(cls, trace_id, phrase_id, request_id=None):
        """Find an existing Ner query with the given parameters and return it.

        :param trace_id: the trace id for this phrase
        :param phrase: the phrase query that is associated with the ner query in search
        :return: found/generated phrase query
        """
        inst =  SPARQLDict._get(klass=cls.klass, props={
            smile.hasTraceID   : trace_id,
            smile.hasPhrase     : phrase_id,
        })
        return cls(inst=inst) if inst else None

    @classmethod
    def generate(cls,  trace_id, phrase_id, certainty=0, request_id=None):
        """Generate a new Ner query with the given parameters and return it.

        :param trace_id: the trace id for this phrase
        :param phrase: the phrase query that is associated with the ner query in search
        :param certainty: certainty level in float
        :return: found/generated phrase query
        """
        inst =  SPARQLDict._add(klass=cls.klass, props={
            smile.hasTraceID   : trace_id,
            smile.hasPhrase     : phrase_id,
            smile.hasCertainty  : certainty,
        })
        return cls(inst=inst) if inst else None

    @classmethod
    def find_generate(cls, trace_id, phrase_id, request_id=None, certainty=0):
        """Try to find and return an existing ner query with the given parameters.
         If there is none, generate a new query and return it.

        :param trace_id: the trace id for this phrase
        :param phrase: the phrase query that is associated with the ner query in search
        :param certainty: certainty level in float
        :return: found/generated phrase query
        """
        node = cls.find( trace_id=trace_id,phrase_id=phrase_id, request_id=request_id)
        if node is None:
            node = cls.generate( trace_id=trace_id,request_id=request_id, phrase_id=phrase_id, certainty=certainty)
        return node
