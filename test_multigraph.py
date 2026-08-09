from multigraph import Edge, Multigraph

def test_multigraph_degrees_with_multiplicity():
    g = Multigraph([Edge(0, 1, 2), Edge(1, 2, 1)], {0: 3, 1: 3, 2: 2})
    assert g.degrees() == {0: 2, 1: 3, 2: 1}