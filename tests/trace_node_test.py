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

TESTS_N = 5
TEST_I = 0

with smile:
    from pprint import pprint
    import re
    import numpy as np
    from pyscript.Model.graph_node import GraphNode
    from pyscript.Model.data_level.hypothesis import Hypothesis, SPARQLDict, hashlib
    from pyscript.Model.controller.trace import Trace, SPARQLDict, hashlib
    print()

test_name = os.path.basename(__file__).rpartition(r'.')[0]
p_bar = tqdm.tqdm(range(TESTS_N), desc=f"Tests{test_name.rjust(20)}")

with smile:
    rr = f"smile:{int(np.random.rand()*10**10)}"
    trace_object1 = Trace(inst_id=rr)
    hypos = []
    hypos.append(Hypothesis().generate(trace_id=trace_object1.inst_id))
    hypos.append(Hypothesis().generate(trace_id=trace_object1.inst_id))
    trace_object1.hypotheses = hypos[0].inst_id
    trace_object1.hypotheses = hypos[1].inst_id
    assert trace_object1.hypotheses == [hypo.inst_id for hypo in hypos]
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()


with smile:
    # test Trace.find on null
    rr = f"{int(np.random.rand()*10**10)}"
    node = Trace.find(inst_id=rr)
    assert node is None
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Trace.find_generate on new
    rr = f"{int(np.random.rand()*10**10)}"
    node_add = Trace.generate(inst_id=rr)
    node_found = Trace.find(inst_id=rr)
    inst = SPARQLDict._get(klass="smile.Trace", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()


with smile:
    # test Trace.find_generate on new
    rr = f"{int(np.random.rand()*10**10)}"
    node_found = Trace.find_generate(inst_id=rr)
    inst = SPARQLDict._get(klass="smile.Trace", inst_id=node_found.inst_id)

    assert node_add is not None
    assert node_found.inst_id == inst['ID']
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Trace.find_generate on existing
    rr = f"{int(np.random.rand()*10**10)}"
    node_add = Trace.generate(inst_id=rr)
    node_found = Trace.find(inst_id=rr)
    node_generated_found = Trace.find_generate(inst_id=rr)
    inst = SPARQLDict._get(klass="smile.Trace", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    assert node_found.inst_id == inst['ID']
    assert node_generated_found.inst_id == inst['ID']
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = f"{int(np.random.rand()*10**10)}"
    node_add = Trace.generate(inst_id=rr)
    hypos = [
        Hypothesis.generate(trace_id=node_add.inst_id), 
        Hypothesis.generate(trace_id=node_add.inst_id), 
        Hypothesis.generate(trace_id=node_add.inst_id)]
    node_add.hypotheses = hypos[0].inst_id
    node_add.hypotheses = hypos[1].inst_id
    node_add.hypotheses = hypos[2].inst_id
    node_found = Trace.find_generate(inst_id=rr)
    inst = SPARQLDict._get(klass="smile.Trace", inst_id=node_add.inst_id)
    trace = Trace()
    trace.inst_id = inst['ID']
    trace.load()
    key_show = f"smile.Trace_{trace.inst_id}"
    key = int(hashlib.sha256(key_show.encode('utf-8')).hexdigest(), 16) % 10**8
    assert node_add.key_show() == key_show
    assert node_add.key() == key
    assert len(node_add.hypotheses) == 3

assert TESTS_N == TEST_I

print("\n\n")

