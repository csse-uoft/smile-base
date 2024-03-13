import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)

with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList

class Trace(GraphNode):
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
    klass = 'smile.Trace'
    super_relations = GraphNode.relations
    klass_relations = {
        'hypotheses' : {'pred':smile.hasHypotheses, 'cardinality':'many'},
        # 'requests' : {'pred':smile.hasRequests, 'cardinality':'many'},
    }
    relations = {**klass_relations, **super_relations}

    def __init__(self, inst_id=None, inst=None, keep_db_in_synch=True) -> None:
        super().__init__(inst_id=inst_id, inst=inst, keep_db_in_synch=keep_db_in_synch)
       
    from py2graphdb.utils import db_utils
    def_file_path = os.path.dirname(db_utils.__file__) + '/_model_getters_setters_deleters.py'
    imported_code = open(def_file_path).read()
    exec(imported_code)


    # def __repr__(self):
    #     return 'ID: {}, Hypos: {}'.format(
    #         self.inst_id, len(self.hypotheses))

    def key(self):
        s = self.key_show()
        return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10**8
       
    def key_show(self):
        return f"{self.klass}_{self.inst_id}"


