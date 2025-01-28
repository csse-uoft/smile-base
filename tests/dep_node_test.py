from py2graphdb.config import config as CONFIG
from py2graphdb.utils.misc_lib import *
import tqdm, os


from owlready2 import default_world, onto_path
onto_path.append('input/ontology_cache/')

smile = default_world.get_ontology(CONFIG.NM)
rdf_nm =  default_world.get_namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

CONFIG.STORE_LOCAL = False

LOG_FILE = CONFIG.LOG_DIR+f"logging_{CONFIG.RUN_LABEL}.txt"    # Log file used to log errors or warnings that should not stop the processing (e.g. invalid address is found)
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

TESTS_N = 8
TEST_I = 0

with smile:
    from pprint import pprint
    import re, hashlib
    import numpy as np
    from src.smile_base.Model.data_level.dep import Dep, SPARQLDict
    from src.smile_base.Model.controller.trace import Trace
    print()

test_name = os.path.basename(__file__).rpartition(r'.')[0]
p_bar = tqdm.tqdm(range(TESTS_N), desc=f"Tests{test_name.rjust(20)}")


with smile:
    trace = Trace.generate()
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    test_inst0 = Dep()
    test_inst0.dep = 'nsubj'
    test_inst0.subject_word = rr1
    test_inst0.object_word = rr2
    assert test_inst0._dep == 'nsubj'
    assert test_inst0._subject_word == f"smile.{rr1}"
    assert test_inst0._object_word == f"smile.{rr2}"
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test certainty property
    test_inst0 = Dep()
    test_inst0.certainty = 0.123
    test_inst0.certainty = 0.456
    assert test_inst0._certainty == 0.456
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()


with smile:
    # test Hypothesis.find on null
    rr = f"{int(np.random.rand()*10**10)}"
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    node = Dep.find(trace_id=rr, dep='two', subject_id=rr1, object_id=rr2)
    assert node is None
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Hypothesis.generate then find on conent
    rr = f"{int(np.random.rand()*10**10)}"
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    node_add = Dep.generate(trace_id=rr, dep='nobj', subject_id=rr1, object_id=rr2)
    node_found = Dep.find(trace_id=rr, dep='nobj', subject_id=rr1, object_id=rr2)
    inst = SPARQLDict._get(klass="smile.Dep", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    assert node_add.trace == inst[smile.hasTraceID][0]
    assert node_add.trace == f"smile.{rr}"
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Hypothesis.generate then find on content_label
    rr = f"{int(np.random.rand()*10**10)}"
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    node_add = Dep.generate(trace_id=rr, dep='ref', subject_id=rr1, object_id=rr2)
    node_found = Dep.find(trace_id=rr, dep='ref', subject_id=rr1, object_id=rr2)
    inst = SPARQLDict._get(klass="smile.Dep", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    assert node_add.subject_word == node_found.subject_word
    assert node_add.object_word == node_found.object_word
    assert node_add.trace == inst[smile.hasTraceID][0]
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Hypothesis.generate then find on start and end
    rr = f"{int(np.random.rand()*10**10)}"
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    start = int(np.random.rand()*10**10)
    end = start + 30
    node_add = Dep.generate(trace_id=rr, dep='ref', subject_id=rr1, object_id=rr2)
    node_found = Dep.find(trace_id=rr, dep='ref', subject_id=rr1, object_id=rr2)
    inst = SPARQLDict._get(klass="smile.Dep", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    assert node_add.subject_word == node_found.subject_word
    assert node_add.object_word  == node_found.object_word
    assert node_add.trace == inst[smile.hasTraceID][0]
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Hypothesis.find_generate on new
    rr = f"{int(np.random.rand()*10**10)}"
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    node_add = Dep.find(trace_id=rr, dep='comm', subject_id=rr1, object_id=rr2)
    node_found = Dep.find_generate(trace_id=rr, dep='comm', subject_id=rr1, object_id=rr2)
    inst = SPARQLDict._get(klass="smile.Dep", inst_id=node_found.inst_id)

    assert node_add is None
    assert node_found.inst_id == inst['ID']
    assert node_found.subject_word == f"smile.{rr1}"
    assert node_found.object_word == f"smile.{rr2}"
    assert node_found.trace == inst[smile.hasTraceID][0]
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Hypothesis.find_generate on existing
    rr = f"{int(np.random.rand()*10**10)}"
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    node_add = Dep.generate(trace_id=rr, dep='sub2', subject_id=rr1, object_id=rr2)
    node_found = Dep.find_generate(trace_id=rr, dep='sub2', subject_id=rr1, object_id=rr2)
    inst = SPARQLDict._get(klass="smile.Dep", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    assert node_found.inst_id == inst['ID']
    assert node_found.trace == inst[smile.hasTraceID][0]
    assert node_found.trace == f"smile.{rr}"
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = f"{int(np.random.rand()*10**10)}"
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    node_add = Dep.generate(trace_id=rr, dep='sub3', subject_id=rr1, object_id=rr2)
    node_found = Dep.find_generate(trace_id=rr, dep='sub3', subject_id=rr1, object_id=rr2)
    inst = SPARQLDict._get(klass="smile.Dep", inst_id=node_add.inst_id)
    hypo = Dep()
    hypo.inst_id = inst['ID']
    hypo.load()
    key_show = f"Dep_{hypo.inst_id}"
    key = int(hashlib.sha256(key_show.encode('utf-8')).hexdigest(), 16) % 10**8
    assert node_add.key_show() == key_show
    assert node_add.key() == key

assert TESTS_N == TEST_I

print("\n\n")

