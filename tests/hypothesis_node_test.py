from config import config as CONFIG
from .scripts.misc_lib import *
import tqdm


from owlready2 import default_world, onto_path
onto_path.append('input/ontology_cache/')

smile = default_world.get_ontology(CONFIG.NM)
rdf_nm =  default_world.get_namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

CONFIG.STORE_LOCAL = False

LOG_FILE = CONFIG.LOG_DIR+f"logging_{CONFIG.RUN_LABEL}.txt"    # Log file used to log errors or warnings that should not stop the processing (e.g. invalid address is found)
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

TESTS_N = 10
TEST_I = 0

with smile:
    from pprint import pprint
    import re
    import numpy as np
    from pyscript.Model.data_level.hypothesis import Hypothesis, SPARQLDict, hashlib
    from pyscript.Model.graph_node import GraphNode
    print()

test_name = os.path.basename(__file__).rpartition(r'.')[0]
p_bar = tqdm.tqdm(range(TESTS_N), desc=f"Tests{test_name.rjust(30)}")

with smile:
    test_inst0 = Hypothesis()
    test_inst0.ks_ar = '112233'
    test_inst0.ks_ar = '445566'
    assert test_inst0._ks_ar == 'smile.445566'
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    test_inst0 = Hypothesis()
    test_inst0.certainty = 0.123
    test_inst0.certainty = 0.456
    assert test_inst0._certainty == 0.456
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()


with smile:
    # test Hypothesis.find on null
    rr = f"{int(np.random.rand()*10**10)}"
    node = Hypothesis.find(trace_id=rr)
    assert node is None
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Hypothesis.find_generate on new
    rr = f"{int(np.random.rand()*10**10)}"
    node_add = Hypothesis.generate(trace_id=rr)
    node_found = Hypothesis.find(trace_id=rr)
    inst = SPARQLDict._get(klass="smile.Hypothesis", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    assert node_add.trace == inst[smile.hasTraceID][0]
    assert node_add.trace == f"smile.{rr}"
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()


with smile:
    # test Hypothesis.find_generate on new
    rr = f"{int(np.random.rand()*10**10)}"
    node_add = Hypothesis.find(trace_id=rr)
    node_found = Hypothesis.find_generate(trace_id=rr)
    inst = SPARQLDict._get(klass="smile.Hypothesis", inst_id=node_found.inst_id)

    assert node_add is None
    assert node_found.inst_id == inst['ID']
    assert node_found.trace == inst[smile.hasTraceID][0]
    assert node_found.trace == f"smile.{rr}"
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Hypothesis.find_generate on existing
    rr = f"{int(np.random.rand()*10**10)}"
    node_add = Hypothesis.generate(trace_id=rr)
    node_found = Hypothesis.find_generate(trace_id=rr)
    inst = SPARQLDict._get(klass="smile.Hypothesis", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    assert node_found.inst_id == inst['ID']
    assert node_found.trace == inst[smile.hasTraceID][0]
    assert node_found.trace == f"smile.{rr}"
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = f"{int(np.random.rand()*10**10)}"
    node_add = Hypothesis.generate(trace_id=rr)
    node_found = Hypothesis.find_generate(trace_id=rr)
    inst = SPARQLDict._get(klass="smile.Hypothesis", inst_id=node_add.inst_id)
    hypo = Hypothesis()
    hypo.inst_id = inst['ID']
    hypo.load()
    key_show = f"Hypothesis_{hypo.inst_id}"
    key = int(hashlib.sha256(key_show.encode('utf-8')).hexdigest(), 16) % 10**8
    assert node_add.key_show() == key_show
    assert node_add.key() == key
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()


with smile:
    insts = SPARQLDict._search(klass=GraphNode.klass,how='all')
    nodes = GraphNode.search(how='all')
    assert len(insts) == len(nodes)
    assert len(insts) == 0
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    insts = SPARQLDict._search(klass=GraphNode.klass,how='all', subclass=True)
    nodes = GraphNode.search(how='all', subclass=True)
    assert len(insts) == len(nodes)
    assert len(insts) > 0
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = f"{int(np.random.rand()*10**10)}"
    node_add = Hypothesis.generate(trace_id=rr)
    nodes = GraphNode.search(how='all', subclass=True)
    matches = [node for node in nodes if node.inst_id == node_add.inst_id]
    assert len(matches) == 1
    assert matches[0].inst_id == node_add.inst_id
    assert matches[0].trace == node_add.trace
    assert isinstance(node_add, Hypothesis)
    assert isinstance(matches[0], Hypothesis)
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()



assert TESTS_N == TEST_I

print("\n\n")

