from __main__ import *
from py2graphdb.config import config as CONFIG
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing , onto_path
from src.smile_base.Model.data_level.cids import Organization, LogicModel, Program, Service, Outcome

onto_path.append('input/ontology_cache/')
import os
if os.path.exists(CONFIG.LOG_FILE): 
  os.remove(CONFIG.LOG_FILE)
CONFIG.STORE_LOCAL = False
from py2graphdb.ontology.operators import *

smile = default_world.get_ontology(CONFIG.NM)
import unittest
from py2graphdb.utils.misc_lib import *

with smile:
    from src.smile_base.ontology.namespaces import cids
    from py2graphdb.utils.db_utils import PropertyList, SPARQLDict, resolve_nm_for_dict, Thing, _resolve_nm

def delete_test_nodes():
    Organization(inst_id=f'smile.1000', keep_db_in_synch = True).delete()
    LogicModel(inst_id=f'smile.1001', keep_db_in_synch = True).delete()
    Program(inst_id=f'smile.1002', keep_db_in_synch = True).delete()
    Service(inst_id=f'smile.1003', keep_db_in_synch = True).delete()
    Outcome(inst_id=f'smile.1004', keep_db_in_synch = True).delete()

class TestConfig():
    def __init__(self):
        self.init_impact_model()

    def init_impact_model(self):
        with smile:
            delete_test_nodes()
            organization = Organization(inst_id=f'smile.1000', keep_db_in_synch = True)
            logic_model = LogicModel(inst_id=f'smile.1001', keep_db_in_synch = True)
            program = Program(inst_id=f'smile.1002', keep_db_in_synch = True)
            service = Service(inst_id=f'smile.1003', keep_db_in_synch = True)
            outcome = Outcome(inst_id=f'smile.1004', keep_db_in_synch = True)

            logic_model.organization = organization.inst_id
            logic_model.program = program.inst_id
            program.service = service.inst_id
            service.outcome = outcome.inst_id
            
            #organization <- logic_model -> program -> service -> outcome

class TestImpactModel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #save classes and methods in graph
        from graphdb_importer import import_and_wait, set_config
        TMP_DIR = './tmp/'
        _ = os.makedirs(TMP_DIR) if not os.path.exists(TMP_DIR) else None
        owl_file = f'{TMP_DIR}unit_test_impact.owl'
        smile.save(owl_file)
        set_config(CONFIG.SERVER_URL, CONFIG.REPOSITORY, username='admin', password='admin')
        import_and_wait(owl_file, replace_graph=True)

        SPARQLDict._clear_graph(graph=CONFIG.GRAPH_NAME)

        self.config = TestConfig()
    
    def test_path_basic(self):
        with smile:
            start = 'smile.1001'
            end = 'smile.1004'
            preds = [smile.forOrganization, smile.hasProgram, smile.hasService, smile.hasStakeholderOutcome]
            res = SPARQLDict._process_path_request(start, end, action='collect', preds=preds, direction='children', how='all')
            print("TEST 1")
            print(res)
            self.assertEqual(res, [{'start': 'smile.1001', 'end': 'smile.1004', 'path': ['smile.1002', 'smile.1003']}])

    def test_path_no_end(self):
        with smile:
            start = 'smile.1001'
            preds = [smile.forOrganization, smile.hasProgram, smile.hasService, smile.hasStakeholderOutcome]
            res = SPARQLDict._process_path_request(start, None, action='collect', preds=preds, direction='children', how='all')
            print("TEST 2")
            print(res)
            self.assertEqual(res, [
                {'start': 'smile.1001', 'end': 'smile.1004', 'path': ['smile.1002', 'smile.1003']}, 
                {'start': 'smile.1001', 'end': 'smile.1003', 'path': ['smile.1002']}, 
                {'start': 'smile.1001', 'end': 'smile.1002', 'path': []}, 
                {'start': 'smile.1001', 'end': 'smile.1000', 'path': []}])

    def test_path_reverse(self):
        with smile:    
            start = 'smile.1004'
            end = 'smile.1001'
            preds = [smile.forOrganization, smile.hasProgram, smile.hasService, smile.hasStakeholderOutcome]
            res = SPARQLDict._process_path_request(start, end, action='collect', preds=preds, direction='parents', how='all')
            self.assertEqual(res, [{'start': 'smile.1004', 'end': 'smile.1001', 'path': ['smile.1003', 'smile.1002']}])


    def test_path_not_exist(self):
        with smile:    
            start = 'smile.1004'
            end = 'smile.1002'
            preds = [smile.forOrganization, smile.hasProgram, smile.hasService, smile.hasStakeholderOutcome]
            res = SPARQLDict._process_path_request(start, end, action='ask', preds=preds, direction='children', how='all')
            self.assertFalse(res)

    def test_path_distance(self):
        with smile:
            start = 'smile.1001'
            end = 'smile.1004'
            preds = [smile.forOrganization, smile.hasProgram, smile.hasService, smile.hasStakeholderOutcome]
            res = SPARQLDict._process_path_request(start, end, action='distance', preds=preds, direction='children', how='all')
            self.assertEqual(res, [{'start': 'smile.1001', 'end': 'smile.1004', 'distance': 3}])


    
