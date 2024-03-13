import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList


class KsInput(GraphNode):
    """
        A db Model class that defines the schema for knowledge source inputs.
        Instances of this class are created only once when the database is created.
        ...

        Attributes
        ----------
        __tablename__ : str
            The name of the database table
        id : SQLAlchemy.Column
            A unique ID for the knowledge source input type
        ks : SQLAlchemy.relationship
            Relationship with the ks data level
        data_level : SQLAlchemy.Column
            String representation of input data level
        created_at : SQLAlchemy.Column
            The date and time when an instantiated

    """
    klass = 'smile.KsInput'
    super_relations = GraphNode.relations
    klass_relations = {
        'ks' : {'pred':smile.hasKS, 'cardinality':'one'},
        'data_level': {'pred':smile.hasDataLevel, 'cardinality':'one'},
        'hypotheses': {'pred':smile.hasHypotheses, 'cardinality':'many'}
    }
    relations = {**klass_relations, **super_relations}

    def __init__(self, inst_id=None, inst=None, keep_db_in_synch=True) -> None:
        super().__init__(inst_id=inst_id, inst=inst, keep_db_in_synch=keep_db_in_synch)
       
    from py2graphdb.utils import db_utils
    def_file_path = os.path.dirname(db_utils.__file__) + '/_model_getters_setters_deleters.py'
    imported_code = open(def_file_path).read()
    exec(imported_code)

    # def __repr__(self):
    #     return super().__repr__() + \
    #            'ID: {}, data_level: {}'.format(self.inst_id, self.data_level)
