import os
def init_db():
    from py2graphdb.config import config as CONFIG
    from owlready2 import default_world
    nm = default_world.get_ontology(CONFIG.NM)

    with nm:
        from py2graphdb.utils import init_db
        from smile_base.Model.controller.ks import Ks

        init_db.init_db()
        Ks.initialize_ks_db()


def load_owl(owl_file, graph_name=None):
    from py2graphdb.config import config as CONFIG
    from owlready2 import default_world
    nm = default_world.get_ontology(CONFIG.NM)
    with nm:
        from py2graphdb.utils import init_db
        init_db.load_owl(owl_file)
