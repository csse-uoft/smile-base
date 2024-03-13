import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList

class Request(GraphNode):
    """
        A db Model class that defines the schema for Hypothesis Request.
        Instances of this class are created whenever a new request for a hypothesis is created.

        ...

        Attributes
        ----------
        __tablename__ : str
            The name of the database table
        id : SQLAlchemy.Column
            A unique ID for the knowledge source type
        created_at : SQLAlchemy.Column
            The date and time when an instantiated
        output : str
            The output hypothesis type being requested
        certainty : float
            The highest certainty
        hypothesis : SQLAlchemy.relationship
            Relationship with the hypothesis data level
    """
    klass = 'smile.Request'
    super_relations = GraphNode.relations
    klass_relations = {
        'trace' : {'pred':smile.hasTraceID, 'cardinality':'one'},
        'hypotheses': {'pred':smile.hasHypotheses, 'cardinality':'many'},
        'status': {'pred':smile.hasKSARStatus, 'cardinality':'one'},
        'input': {'pred':smile.hasInput, 'cardinality':'one'},
        'output': {'pred':smile.hasOutput, 'cardinality':'one'},
    }
    relations = {**klass_relations, **super_relations}

    def __init__(self, inst_id=None, inst=None, keep_db_in_synch=True) -> None:
        super().__init__(inst_id=inst_id, inst=inst, keep_db_in_synch=keep_db_in_synch)
       
    from py2graphdb.utils import db_utils
    def_file_path = os.path.dirname(db_utils.__file__) + '/_model_getters_setters_deleters.py'
    imported_code = open(def_file_path).read()
    exec(imported_code)



    def __repr__(self):
        return 'ID: {}, PKS.ID:{}, Input level: {}, Output level: {}'.format(
            self.id, self.parent_ks_ar_id, self.input, self.output)

    def key_show(self):
        return f"{self.__class__.__name__}_{self.id}_{[self.input,self.output]}"
    def key(self):
        import hashlib
        s = self.key_show()
        return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10**8


