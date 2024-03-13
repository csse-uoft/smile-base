import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList
from .hypothesis import Hypothesis

class Sentence(Hypothesis):
    """
    A db Model class that defines the schema for the Sentence data level.
    Base schema is extended from the Hypothesis class.

    ...

    Attributes
    ----------
    __tablename__ : str
        The name of the database table
    content : SQLAlchemy.Column
        The lexicon value for this sentence
    start : SQLAlchemy.Column
        Start position of sentence in the Text, starting at 0
    end : SQLAlchemy.Column
        End position of sentence in the Text, starting at 0
    word_ids : SQLAlchemy.relationship
        The ID of the data queries (Words, Taxonomy, etc) that are used to generate this sentence.

    """
    klass = 'smile.Sentence'
    super_relations = Hypothesis.relations    
    klass_relations = {
        'index'     : {'pred':smile.hasIndex,'cardinality':'one'},
        'content'   : {'pred':smile.hasContent, 'cardinality':'one'},
        'start'     : {'pred':smile.hasStart, 'cardinality':'one'},
        'end'       : {'pred':smile.hasEnd, 'cardinality':'one'},
        'words'     : {'pred':smile.hasWords, 'cardinality':'many'},
        'phrases'   : {'pred':smile.hasPhrases, 'cardinality':'many'},
        'text'      : {'pred':smile.inText, 'cardinality':'one'},
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
    def find(cls,  trace_id, index, content, start, end, request_id=None):
        """Find an existing sentence query with the given parameters and return it.

        :param request_id: the trace id for this sentence
        :param content: the lexicon value for this sentence
        :param start: start position of sentence in the Text, starting at 0
        :param end: end position of sentence in the Text, starting at 0
        :return: found sentence query
        """
        inst =  SPARQLDict._get(klass=cls.klass, props={
            smile.hasTraceID    : trace_id,
            smile.hasIndex      : index,
            smile.hasContent    : content,
            smile.hasStart      : start,
            smile.hasEnd        : end,
            # cls.relations['request']['pred']:request_id,
        })
        return cls(inst=inst) if inst else None

    @classmethod
    def generate(cls, trace_id, index, content, start, end, request_id=None, certainty=1):
        """Generate a new sentence query with the given parameters and return it.

        :param request_id: the trace id for this sentence
        :param content: the lexicon value for this sentence
        :param start: start position of sentence in the Text, starting at 0
        :param end: end position of sentence in the Text, starting at 0
        :param certainty: certainty level in float
        :return: generated sentence query
        """
        inst =  SPARQLDict._add(klass=cls.klass, props={
            smile.hasTraceID    : trace_id,
            smile.hasIndex      : index,
            smile.hasContent    : content,
            smile.hasStart      : start,
            smile.hasEnd        : end,
            smile.hasCertainty  : certainty,
            # cls.relations['request']['pred']:request_id,
        })

        return cls(inst=inst) if inst else None

    @classmethod
    def find_generate(cls, trace_id, index, content, start=None, end=None, request_id=None, certainty=1):
        """Try to find and return an existing sentence query with the given parameters.
         If there is none, generate a new query and return it.

        :param request_id: the trace id for this sentence
        :param content: the lexicon value for this sentence
        :param start: start position of sentence in the Text, starting at 0
        :param end: end position of sentence in the Text, starting at 0
        :param certainty: certainty level in float
        :return: found/generated sentence query
        """
        node = cls.find( trace_id=trace_id,request_id=request_id, index=index, content=content, start=start, end=end)
        if node is None:
            node = cls.generate( trace_id=trace_id,request_id=request_id, index=index, content=content, start=start, end=end)
        return node
