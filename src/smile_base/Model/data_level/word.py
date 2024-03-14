import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList
from .hypothesis import Hypothesis

class Word(Hypothesis):
    """
    A db Model class that defines the schema for the Word data level.
    Base schema is extended from the Hypothesis class.

    ...

    Attributes
    ----------
    __tablename__ : str
        The name of the database table
    content : SQLAlchemy.Column
        The string value of this term (e.g. “The main service” has the value(s) “The”, “main”, and “service”)
    content_label : SQLAlchemy.relationship
        The label of this term from the original hypothesis (e.g. “The main service” has value_label(s) as tokens 
        “The-0”, “main-1”, and “service-2” with content_label(s) “0”, “1”, and “2”)
    start : SQLAlchemy.Column
        Start position of word in the Text, starting at 0
    end : SQLAlchemy.Column
        End position of word in the Text, starting at 0
    phrases : SQLAlchemy.relationship
        Phrases that are associated with this Word
    poses : SQLAlchemy.relationship
        POSes that are associated with this Word

    """
    klass = 'smile.Word'
    super_relations = Hypothesis.relations
    klass_relations = {
        'content'   : {'pred':smile.hasContent, 'cardinality':'one'},
        'content_label'   : {'pred':smile.hasContentLabel, 'cardinality':'one'},
        'start'     : {'pred':smile.hasStart, 'cardinality':'one'},
        'end'       : {'pred':smile.hasEnd, 'cardinality':'one'},
        'phrases'   : {'pred':smile.hasPhrases, 'cardinality':'many'},
        'pos'       : {'pred':smile.hasPos, 'cardinality':'one'},
        'sentence'  : {'pred':smile.inSentence, 'cardinality':'one'},
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
    def find(cls, trace_id, content, request_id=None, content_label=None, start=None, end=None):
        """Find an existing word query with the given parameters and return it.

        :param request_id: the trace id for this phrase
        :param content: the lexicon value for this phrase, e.g. hello, in "hello there"
        :param content_label: the lexicon value for this phrase, with its index, e.g. hello-1, in "hello there"
        :param start: start position of phrase in the Text, starting at 
        :param end: end position of phrase in the Text, starting at 0
        :return: found/generated word query
        """
        inst = None
        if content_label is not None:
            inst =  SPARQLDict._get(klass=cls.klass, props={
                smile.hasTraceID:trace_id,
                smile.hasContent:content,
                smile.hasContentLabel:content_label,
                            })

        elif start is not None and end is not None:
            inst =  SPARQLDict._get(klass=cls.klass, props={
                smile.hasTraceID:trace_id,
                smile.hasContent:content,
                smile.hasStart:start,
                smile.hasEnd:end,
                            })
        elif content is not None:
            inst =  SPARQLDict._get(klass=cls.klass, props={
                smile.hasTraceID:trace_id,
                smile.hasContent:content,
            })

        return cls(inst=inst) if inst else None

    @classmethod
    def generate(cls, trace_id, content, request_id=None,  content_label=None, 
                 start=None, end=None, certainty=0, phrase=None):
        """Generate a new word query with the given parameters and return it.

        :param request_id: the trace id for this phrase
        :param content: the lexicon value for this phrase, e.g. hello, in "hello there"
        :param content_label: the lexicon value for this phrase, with its index, e.g. hello-1, in "hello there"
        :param start: start position of phrase in the Text, starting at 0
        :param end: end position of phrase in the Text, starting at 0
        :param certainty: certainty level in float
        :return: found/generated word query
        """
        if content is None:
            return None

        inst =  SPARQLDict._add(klass=cls.klass, props={
            smile.hasTraceID:trace_id,
            smile.hasContent:content,
            smile.hasContentLabel:content_label,
            smile.hasStart:start,
            smile.hasEnd:end,
            smile.hasCertainty:certainty,
        })

        return cls(inst=inst) if inst else None

    @classmethod
    def find_generate(cls, trace_id, content, request_id=None, content_label=None,
                      start=None, end=None, certainty=0, phrase=None):
        """Try to find and return an existing word query with the given parameters.
         If there is none, generate a new query and return it.

        :param request_id: the trace id for this phrase
        :param content: the lexicon value for this phrase
        :param start: start position of phrase in the Text, starting at 0
        :param end: end position of phrase in the Text, starting at 0
        :param certainty: certainty level in float
        :param phrase: associated phrase
        :return: found/generated word query
        """
        object = cls.find(request_id=request_id, content=content, content_label=content_label, start=start, end=end, trace_id=trace_id)
        if object is None:
            object = cls.generate(request_id=request_id, content=content, content_label=content_label, start=start, end=end, certainty=certainty, phrase=phrase, trace_id=trace_id)
        return object

