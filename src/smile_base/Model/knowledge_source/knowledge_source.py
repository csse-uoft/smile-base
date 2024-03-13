import sys
import os


from owlready2 import default_world, onto_path
onto_path.append('input/ontology_cache/')
# from py2graphdb.config import config as CONFIG
from py2graphdb.config import config as CONFIG
# if os.path.exists(CONFIG.LOG_FILE): os.remove(CONFIG.LOG_FILE)

import time
# from config import config
from py2graphdb.config import config as CONFIG
from py2graphdb.utils.db_utils import SPARQLDict
from py2graphdb.ontology import *
from py2graphdb.ontology.operators import *

from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing, ThingClass 
smile = default_world.get_ontology(CONFIG.NM)
CONFIG.STORE_LOCAL = False

with smile:
    from ...app.ontology.extra import *
    # from ...Model.data_level.cids.properties import hasService
    from py2graphdb.utils.db_utils import SPARQLDict
    from py2graphdb.utils.db_utils import PropertyList, SPARQLDict, resolve_nm_for_dict, Thing
    print()


    from ..controller.ks import Ks
    from ..controller.trace import Trace
    from ..controller.ks_input import KsInput
    from ..controller.ks_output import KsOutput
    from ..controller.ks_ar import KSAR
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
    from ..data_level.cids.characteristic import Characteristic
    from ..data_level.cids.code import Code
    from ..data_level.cids.input import Input
    from ..data_level.cids.logic_model import LogicModel
    from ..data_level.cids.organization import Organization
    from ..data_level.cids.outcome import Outcome
    from ..data_level.cids.output import Output
    from ..data_level.cids.program import Program
    from ..data_level.cids.service import Service
    from ..data_level.cids.stakeholder import Stakeholder


from abc import ABC


class KnowledgeSource(ABC):
    """
    An abstract class that defines default common use cases for knowledge source classes.

    ...

    Attributes
    ----------
    input_level: str
        String representation of input data level of the knowledge source
    output_level: str
        String representation of output data level of the knowledge source
    Methods
    ----------
    request()
        A common functionality of knowledge source classes to run the relevant functions to fetch the result
    get_outputs(request)
        Reformat outputs for better usability and return them

    """

    def __init__(self, group_input_levels, input_level, output_level, trace, hypothesis_ids, ks_ar):
        """
        :param group_input_levels: data level of the parent data_level of all inputs 
        :param input_level: data level of the input
        :param output_level: data level of the output
        """
        # self.request = request
        self.hypothesis_ids = hypothesis_ids
        self.ks_ar = ks_ar
        self.trace = trace
        self.trace_id = trace.id if trace else None
        self.group_input_levels = group_input_levels
        self.input_level = input_level
        self.output_level = output_level
        self.trace = trace

    def set_input(self):
        self.status = 1 # processing
        raise NotImplementedError

    def get_outputs(self):
        self.status = 1 # processing
        self.status = 2 # done
        raise NotImplementedError

    @classmethod
    def logger(cls, text, trace_id, filename=None):
        import datetime
        """
        logs errors and warnings to the file at filename
        :param text : string value of text to write to log
        :param trace_id: string for id of trace, used to create log filename
        :param filename : string value of log's filename
        """
        if filename is None:
            LOG_FILE_TEMPLATE = CONFIG.LOG_DIR+'smile_trace_log.txt'
            filename = LOG_FILE_TEMPLATE.replace('.txt', f"_{trace_id}.txt")

        # Open a file with access mode 'a'
        file_object = open(filename, 'a')
        # Append 'hello' at the end of file
        file_object.write(str(datetime.datetime.today().strftime("%y:%m:%d %H:%M:%S")) + "\t" + str(text) + "\n")
        # Close the file
        file_object.close()
            
