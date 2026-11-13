from agent_os.graph import build_graph


def test_graph_compiles():
    graph = build_graph(max_cycles=2)
    assert graph is not None
