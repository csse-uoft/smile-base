import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList
from .hypothesis import Hypothesis

class Query(Hypothesis):
    """
    A db Model class that defines the schema for the Text data level.
    Base schema is extended from the Hypothesis class.

    ...

    Attributes
    ----------
    __tablename__ : str
        The name of the database table
    content : SQLAlchemy.Column
        String value of this term

    """
    klass = 'smile.Query'
    super_relations = Hypothesis.relations
    klass_relations = {
         'content'   : {'pred':smile.hasContent, 'cardinality':'one'},
    }
    relations = {**klass_relations, **super_relations}

    def __init__(self, inst_id=None, inst=None, keep_db_in_synch=True) -> None:
        super().__init__(inst_id=inst_id, inst=inst, keep_db_in_synch=keep_db_in_synch)
       
    from py2graphdb.utils import db_utils
    def_file_path = os.path.dirname(db_utils.__file__) + '/_model_getters_setters_deleters.py'
    imported_code = open(def_file_path).read()
    exec(imported_code)

    def show(self):
        return self.content or ''

    @classmethod
    def find(cls, trace_id, content, request_id=None):
        """Find an existing text query with the given parameters and return it.

        :param request_id: the trace id for this text
        :param content: the lexicon value for this text
        :return: found/generated text query
        """
        inst =  SPARQLDict._get(klass=cls.klass, props={
            smile.hasTraceID    : trace_id,
            smile.hasContent    : content,
        })

        return cls(inst=inst) if inst else None

    @classmethod
    def generate(cls, trace_id, content, request_id=None, certainty=1):
        """Generate a new text query with the given parameters and return it.

        :param request_id: the trace id for this text
        :param content: the lexicon value for this text
        :param certainty: certainty level in float
        :return: found/generated text query
        """
        inst =  SPARQLDict._add(klass=cls.klass, props={
            smile.hasTraceID    : trace_id,
            smile.hasContent    : content,
            smile.hasCertainty  : certainty,
        })

        return cls(inst=inst) if inst else None

    @classmethod
    def find_generate(cls, trace_id, content, request_id=None, certainty=0):
        """Try to find and return an existing Text query with the given parameters.
         If there is none, generate a new query and return it.

        :param request_id: the trace id for this dep
        :param content: text to be stored
        :return: found/generated dep query
        """
        node = cls.find( trace_id=trace_id, request_id = request_id, content=content)
        if node is None:
            node = cls.generate(trace_id=trace_id, request_id=request_id, content=content, certainty=certainty)
        return node

