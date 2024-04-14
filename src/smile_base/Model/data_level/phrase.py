import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList
    from py2graphdb.ontology.operators import *
from .hypothesis import Hypothesis

class Phrase(Hypothesis):
    """
    A db Model class that defines the schema for the Phrase data level.
    Base schema is extended from the Hypothesis class.

    ...

    Attributes
    ----------
    __tablename__ : str
        The name of the database table
    content : SQLAlchemy.Column
        The lexicon value for this phrase
    start : SQLAlchemy.Column
        Start position of phrase in the Text, starting at 0
    end : SQLAlchemy.Column
        End position of phrase in the Text, starting at 0
    ners : SQLAlchemy.relationship
        The ID of NER queries that are associated with this phrase
    word_ids : SQLAlchemy.relationship
        The ID of the data queries (Words, Taxonomy, etc) that are used to generate this phrase.

    """
    klass = 'smile.Phrase'
    super_relations = Hypothesis.relations    
    klass_relations = {
        'content'   : {'pred':smile.hasContent, 'cardinality':'one'},
        'start'     : {'pred':smile.hasStart, 'cardinality':'one'},
        'end'       : {'pred':smile.hasEnd, 'cardinality':'one'},
        'words'     : {'pred':smile.hasWords, 'cardinality':'many'},
        'sentence'  : {'pred':smile.inSentence, 'cardinality':'one'},
        'text'      : {'pred':smile.inText, 'cardinality':'one'},
        'ners'      : {'pred':smile.hasNers, 'cardinality':'many'},
        'concepts'      : {'pred':smile.hasConcepts, 'cardinality':'many'},
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
    def find(cls,  trace_id,content, start, end, request_id=None):
        """Find an existing phrase query with the given parameters and return it.

        :param request_id: the trace id for this phrase
        :param content: the lexicon value for this phrase
        :param start: start position of phrase in the Text, starting at 0
        :param end: end position of phrase in the Text, starting at 0
        :return: found phrase query
        """
        node = None
        if start is not None and end is not None:
            props = {
                smile.hasTraceID    : trace_id,
                smile.hasContent    : content,
                smile.hasStart      : start,
                smile.hasEnd        : end
            }
            inst =  SPARQLDict._get(klass=cls.klass, props=props)
            if inst is not None:
                node = cls.get(inst_id=inst['ID'])
        else:
            props = {
                smile.hasTraceID    : trace_id,
                smile.hasContent    : content
            }
            if start is None:
                props[notexists(smile.hasStart)] = None
            else:
                props[smile.hasStart] = start

            if end is None:
                props[notexists(smile.hasEnd)] = None
            else:
                props[smile.hasEnd] = end
            insts =  SPARQLDict._search(klass=cls.klass, props=props, how='first')
            if len(insts)>0:
                node = cls.get(insts[0]['ID'])
            else:
                node = None
        return node

    @classmethod
    def generate(cls, trace_id, content, start, end, request_id=None, certainty=1):
        """Generate a new phrase query with the given parameters and return it.

        :param request_id: the trace id for this phrase
        :param content: the lexicon value for this phrase
        :param start: start position of phrase in the Text, starting at 0
        :param end: end position of phrase in the Text, starting at 0
        :param certainty: certainty level in float
        :return: generated phrase query
        """
        inst =  SPARQLDict._add(klass=cls.klass, props={
            smile.hasTraceID    : trace_id,
            smile.hasContent    : content,
            smile.hasStart      : start,
            smile.hasEnd        : end,
            smile.hasCertainty  : certainty,
        })

        return cls(inst=inst) if inst else None

    @classmethod
    def find_generate(cls, trace_id, content, start=None, end=None, request_id=None, certainty=1):
        """Try to find and return an existing phrase query with the given parameters.
         If there is none, generate a new query and return it.

        :param request_id: the trace id for this phrase
        :param content: the lexicon value for this phrase
        :param start: start position of phrase in the Text, starting at 0
        :param end: end position of phrase in the Text, starting at 0
        :param certainty: certainty level in float
        :return: found/generated phrase query
        """
        node = cls.find(trace_id=trace_id,request_id=request_id, content=content, start=start, end=end)
        if node is None:
            node = cls.generate(trace_id=trace_id,request_id=request_id, content=content, start=start, end=end, certainty=certainty)
        else:
            if node.certainty is not None:
                node.certainty = max(node.certainty, certainty)
            else:
                node.certainty = certainty
            node.save()

        return node
