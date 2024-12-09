import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
from ....ontology.namespaces import ic, geo, cids, org, time, schema, sch, activity, landuse_50872, i72, owl

with smile:
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from ..phrase import Phrase
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList
from .stakeholder import Stakeholder

class BeneficialStakeholder(Stakeholder,cids.BeneficialStakeholder):
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
    klass = 'smile.BeneficialStakeholder'
    super_relations = Stakeholder.relations
    klass_relations = {}

    relations = {**klass_relations, **super_relations}

    def __init__(self, inst_id=None, inst=None, keep_db_in_synch=True) -> None:
        super().__init__(inst_id=inst_id, inst=inst, keep_db_in_synch=keep_db_in_synch)
       
    from py2graphdb.utils import db_utils
    def_file_path = os.path.dirname(db_utils.__file__) + '/_model_getters_setters_deleters.py'
    imported_code = open(def_file_path).read()
    exec(imported_code)


    def show(self):
        phrase = ''
        if self.phrase:
            node = Phrase.get(self.phrase)
            if node:
                phrase = node.show()
        return phrase if phrase is not None else (f"{self.klass}" or '')


