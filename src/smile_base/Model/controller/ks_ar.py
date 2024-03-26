import re, os, datetime, numpy as np

from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG

smile = default_world.get_ontology(CONFIG.NM)
with smile:
    from ...ontology.extra import *
    from py2graphdb.Models.graph_node import GraphNode, SPARQLDict, _resolve_nm
    from py2graphdb.utils.db_utils import resolve_nm_for_dict, PropertyList
    from .ks import Ks
    from .trace import Trace
    from ..data_level.hypothesis import Hypothesis
    from ..data_level.coref import CoRef
    from ..data_level.text import Text
    from ..data_level.word import Word
    from ..data_level.phrase import Phrase
    from ..data_level.pos import Pos
    from ..data_level.ner import Ner
    from ..data_level.spo import Spo
    from ..data_level.dep import Dep
    from ..data_level.rel import Rel

class KSAR(GraphNode):
    """
        A db Model class that defines the schema for knowledge source instances.
        Instances of this class are created when a knowledge source is called to
        create a hypothesis, for some request.

        ...

        Attributes
        ----------
        __tablename__ : str
            The name of the database table
        id : SQLAlchemy.Column
            A unique ID for the knowledge source input type
        ks_id : SQLAlchemy.Column
            knowledge source ralation's IDs that have this data level as an output type
        ks : SQLAlchemy.relationship
            Relationship with the ks data level
        data_level : SQLAlchemy.Column
            String representation of output data level
        created_at : SQLAlchemy.Column
            The date and time when an instantiated

    """

    klass = 'smile.KSAR'
    super_relations = GraphNode.relations
    klass_relations = {
        'trace' : {'pred':smile.hasTraceID, 'cardinality':'one'},
        'ks' : {'pred':smile.hasKS, 'cardinality':'one'},
        'ks_status': {'pred':smile.hasKSARStatus, 'cardinality':'one'},
        'input_hypotheses': {'pred':smile.hasInputHypotheses, 'cardinality':'many'},
        'hypotheses': {'pred':smile.hasOutputHypotheses, 'cardinality':'many'},
        'request': {'pred':smile.hasRequest, 'cardinality':'one'},
        'cycle':    {'pred':smile.hasCycle, 'cardinality':'one'},
        'trigger_event' :{'pred':smile.hasTriggerDescription, 'cardinality':'one'},

        # # Holds pickle version of KnowledgeSource object
        'object_pickle_path': {'pred':smile.hasKSObjectPicklePath, 'cardinality':'one'},
    }
    relations = {**klass_relations, **super_relations}

    def __init__(self, inst_id=None, inst=None, keep_db_in_synch=True) -> None:
        super().__init__(inst_id=inst_id, inst=inst, keep_db_in_synch=keep_db_in_synch)
       
    from py2graphdb.utils import db_utils
    def_file_path = os.path.dirname(db_utils.__file__) + '/_model_getters_setters_deleters.py'
    imported_code = open(def_file_path).read()
    exec(imported_code)




    def summary(self, filename):
        """
        Generate  log entry for this Knowledge Source
        ID
        Name
        Trigger cycle
        Trigger event
        Tiggering decision
        Pre-condition-values
        Condition-values
        Scheduling-values
        Ratings
        Priority
        
        """
        ks = Ks(inst_id=self.ks)
        in_hypos = [Hypothesis(hypo).cast_to_graph_type() for hypo in self.input_hypotheses]
        out_hypos = [Hypothesis(hypo).cast_to_graph_type() for hypo in self.hypotheses]
        rating = np.mean([hypo.certainty for hypo in out_hypos if hypo.certainty])

        text = []
        text += [f"ID:\t{self.id}"]
        text += [f"KS Name:\t{ks.py_name}" + f"\tPyName:\t{ks.name}" + f"\tKS ID:\t{ks.id}"]
        text += [f"Trace:\t{self.trace}"]
        text += [f"Triggering Event:\t{self.trigger_event}"]
        text += [f"Cycle:\t{self.cycle}"]
        text += [f"Input Hypotheses:"]
        for hypo in in_hypos:
            text += [f"\t{hypo.klass}\t\"{hypo.show()}\"\t{hypo.id.split('-')[0]}"]

        text += ["Expected Outputs:"]
        for output in ks.outputs:
            text += [f"\tOutput Type:\t{output}"]

        text += ["Obtained Outputs:"]
        for hypo in out_hypos:
            if isinstance(hypo, smile.Ner):
                phrase = Hypothesis(inst_id=hypo.phrase).cast_to_graph_type()
                text += [f"\t{hypo.klass}\t\"{hypo.entity}({phrase.content})\"\t{round(hypo.certainty,5)}\t{hypo.id.split('-')[0]}"]
            else:
                text += [f"\t{hypo.klass}\t\"{hypo.show()}\"\t{round(hypo.certainty,5)}\t{hypo.id.split('-')[0]}"]

        text += [f"Rating:\t{round(rating, 5)}"]



        file_object = open(filename, 'a')
        # Append 'hello' at the end of file
        file_object.write("\n".join([str(datetime.datetime.today().strftime("%y:%m:%d %H:%M:%S")) + "\t" + str(t) for t in text]) + "\n\n\n")
        # Close the file
        file_object.close()
