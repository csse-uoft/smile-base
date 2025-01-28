from __main__ import *
from ..Model.graph_node import GraphNode
from .unit_test_extra import *
# from .db_utils import smile, rdf_nm,  SPARQLDict
from .db_utils import PropertyList, SPARQLDict, resolve_nm_for_ttl, resolve_nm_for_dict, Thing, smile

import re, hashlib
class UnitTestNode(GraphNode):
    """
        A db Model class that defines the schema for Traces.
        Instances of this class are created whenever a new hypothesis is created.

        ...

        Attributes
        ----------
        __tablename__ : str
            The name of the database table
        id : SQLAlchemy.Column
            A unique ID for the knowledge source type
        created_at : SQLAlchemy.Column
            The date and time when an instantiated
        hypothesis : SQLAlchemy.relationship
            Relationship with the hypothesis data level
    """
    klass = 'smile.UnitTestNode'
    relations = {
        'list_of_ints' : {'pred':smile.hasListOfInts, 'cardinality':'many'},
        'list_of_floats' : {'pred':smile.hasListOfFloats, 'cardinality':'many'},
        'list_of_strs' : {'pred':smile.hasListOfStrs, 'cardinality':'many'},
        'list_of_uris' : {'pred':smile.hasListOfURIs, 'cardinality':'many'},
        'one_int' : {'pred':smile.hasOneInt, 'cardinality':'one'},
        'one_float' : {'pred':smile.hasOneFloat, 'cardinality':'one'},
        'one_str' : {'pred':smile.hasOneStr, 'cardinality':'one'},
        'one_uri' : {'pred':smile.hasOneURI, 'cardinality':'one'},
    }

    def __init__(self, inst_id=None, inst=None, keep_db_in_synch=True) -> None:
        super().__init__(inst_id=inst_id, inst=inst, keep_db_in_synch=keep_db_in_synch)

        

    imported_code = open('pyscript/Model/_model_getters_setters_deleters.py').read()
    exec(imported_code)

