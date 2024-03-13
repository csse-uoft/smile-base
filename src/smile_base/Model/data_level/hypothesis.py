import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList

class Hypothesis(GraphNode):
    """
    A db Model class that defines the base schema for all hypotheses.
    Due to SQLAlchemy abstract classes, the class properties are defined in Hyppthesis
    are replicated in each subclass of Hyppthesis, and the Hyppthesis class is
    not defined as abstract.

    However, this creating subclasses of Hypothesis allows each subclass to be 
    references as hypotheses from the Trace class using trace.hypotheses.
    ...

    Attributes
    ----------
    id : SQLAlchemy.Column
        A unique ID for the data value
    trace : SQLAlchemy.Relationship
        Relationship to the trace of the search process that generated this hypothesis
    ks_id : SQLAlchemy.Column
        ID of the knowledge source that generated this hypothesis
    input_id : SQLAlchemy.Column
        ID of the data-level instance used as input for this Hypothesis
    input_level : SQLAlchemy.Column
        String to identify the input level for input_id
    certainty : SQLAlchemy.Column
        Certainty of the hypothesis in float

    """
    klass = 'smile.Hypothesis'
    super_relations = GraphNode.relations
    klass_relations = {
        'trace' : {'pred':smile.hasTraceID, 'cardinality':'one'},
        'for_ks_ars'  : {'pred':smile.inputForKSARs, 'cardinality':'many'},
        'from_ks_ars' : {'pred':smile.outputOfKSARs, 'cardinality':'many'},
        'certainty' : {'pred':smile.hasCertainty, 'cardinality':'one'},
    }
    relations = {**klass_relations, **super_relations}

    def __init__(self, inst_id=None, inst=None, keep_db_in_synch=True) -> None:
        super().__init__(inst_id=inst_id, inst=inst, keep_db_in_synch=keep_db_in_synch)
       
    from py2graphdb.utils import db_utils
    def_file_path = os.path.dirname(db_utils.__file__) + '/_model_getters_setters_deleters.py'
    imported_code = open(def_file_path).read()
    exec(imported_code)


    def show(self):
        return ""

    @classmethod
    def find(cls, trace_id, request_id=None):
        """Find an existing text query with the given parameters and return it.

        :param request_id: the trace id for this text
        :param content: the lexicon value for this text
        :return: found/generated text query
        """
        inst =  SPARQLDict._get(klass=cls.klass, props={
            cls.relations['trace']['pred']:trace_id,
        })

        return cls(inst=inst) if inst else None

    @classmethod
    def generate(cls, trace_id, request_id=None, certainty=1):
        """Generate a new text query with the given parameters and return it.

        :param request_id: the trace id for this text
        :param content: the lexicon value for this text
        :param certainty: certainty level in float
        :return: found/generated text query
        """
        inst =  SPARQLDict._add(klass=cls.klass, props={
            smile.hasTraceID:trace_id, 
            smile.hasCertainty:certainty})

        return cls(inst=inst) if inst else None

    @classmethod
    def find_generate(cls, trace_id, request_id=None, certainty=0):
        """Try to find and return an existing Text query with the given parameters.
         If there is none, generate a new query and return it.

        :param request_id: the trace id for this dep
        :param content: text to be stored
        :return: found/generated dep query
        """
        object = cls.find(trace_id=trace_id, request_id = request_id)
        if object is None:
            object = cls.generate(trace_id=trace_id, request_id=request_id, certainty=certainty)
        return object
