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

TESTS_N = 6
TEST_I = 0

with smile:
    from pprint import pprint
    import re
    import numpy as np
    from pyscript.Model.data_level.pos import Pos, SPARQLDict, hashlib
    from pyscript.Model.controller.trace import Trace
    print()

test_name = os.path.basename(__file__).rpartition(r'.')[0]
p_bar = tqdm.tqdm(range(TESTS_N), desc=f"Tests{test_name.rjust(20)}")

# with smile:
#     test_inst0 = Hypothesis()
#     test_inst0.trace = 678
#     test_inst0.trace = '456'
#     assert test_inst0._trace == smile.456
#     p_bar.n = TEST_I = TEST_I + 1
#     p_bar.refresh()

with smile:
    trace = Trace.generate()
    test_inst0 = Pos()
    words = [
        f"{int(np.random.rand()*10**10)}",
        f"{int(np.random.rand()*10**10)}"
    ]
    test_inst0.tag = 'one'
    test_inst0.words = words[0]
    test_inst0.words = words[1]
    assert test_inst0._tag == 'one'
    assert len(test_inst0._words) == 2
    assert f"smile.{words[0]}" in test_inst0._words
    assert f"smile.{words[1]}" in test_inst0._words
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test certainty property
    test_inst0 = Pos()
    test_inst0.certainty = 0.123
    test_inst0.certainty = 0.456
    assert test_inst0._certainty == 0.456
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()


with smile:
    # test Hypothesis.find on null
    rr = f"{int(np.random.rand()*10**10)}"
    words = [
        f"{int(np.random.rand()*10**10)}",
        f"{int(np.random.rand()*10**10)}"
    ]
    node = Pos.find(trace_id=rr, pos_tag='NN', word_ids=[w.id for w in words])
    assert node is None
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Hypothesis.generate then find on conent
    rr = f"{int(np.random.rand()*10**10)}"
    words = [
        f"{int(np.random.rand()*10**10)}",
        f"{int(np.random.rand()*10**10)}"
    ]
    node_add = Pos.generate(trace_id=rr, pos_tag='NN', word_ids=[w.id for w in words])
    node_found = Pos.find(trace_id=rr, pos_tag='NN', word_ids=[w.id for w in words])
    inst = SPARQLDict._get(klass="smile.Pos", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    assert node_add.trace == inst[smile.hasTraceID][0]
    assert node_add.trace == f"smile.{rr}"
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()


with smile:
    # test Hypothesis.generate then find on start and end
    rr = f"{int(np.random.rand()*10**10)}"
    words = [
        f"{int(np.random.rand()*10**10)}",
        f"{int(np.random.rand()*10**10)}"
    ]
    node_add = Pos.generate(trace_id=rr, pos_tag='NN', word_ids=[w.id for w in words])
    node_found = Pos.find(trace_id=rr, pos_tag='NN', word_ids=[w.id for w in words])
    inst = SPARQLDict._get(klass="smile.Pos", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    assert len(node_add.words) == 2
    assert node_add.words[0] in [f"smile.{w}" for w in words]
    assert node_add.words[1] in [f"smile.{w}" for w in words]
    assert node_add.tag == 'NN'
    assert node_add.trace == inst[smile.hasTraceID][0]
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Hypothesis.find_generate on existing
    rr = f"{int(np.random.rand()*10**10)}"
    words = [
        f"{int(np.random.rand()*10**10)}",
        f"{int(np.random.rand()*10**10)}"
    ]
    node_add = Pos.generate(trace_id=rr, pos_tag='NN', word_ids=[w.id for w in words])
    node_found = Pos.find_generate(trace_id=rr, pos_tag='NN', word_ids=[w.id for w in words])
    inst = SPARQLDict._get(klass="smile.Pos", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    assert node_found.inst_id == inst['ID']
    assert node_found.trace == inst[smile.hasTraceID][0]
    assert node_found.trace == f"smile.{rr}"
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = f"{int(np.random.rand()*10**10)}"
    words = [
        f"{int(np.random.rand()*10**10)}",
        f"{int(np.random.rand()*10**10)}"
    ]
    node_add = Pos.generate(trace_id=rr, pos_tag='NN', word_ids=[w.id for w in words])
    node_found = Pos.find_generate(trace_id=rr, pos_tag='NN', word_ids=[w.id for w in words])
    inst = SPARQLDict._get(klass="smile.Pos", inst_id=node_add.inst_id)
    hypo = Pos()
    hypo.inst_id = inst['ID']
    hypo.load()
    key_show = f"Pos_{hypo.inst_id}"
    key = int(hashlib.sha256(key_show.encode('utf-8')).hexdigest(), 16) % 10**8
    assert node_add.key_show() == key_show
    assert node_add.key() == key

assert TESTS_N == TEST_I

print("\n\n")

