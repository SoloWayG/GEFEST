import copy

from gefest.core.algs.geom.validation import out_of_bound, self_intersection, too_close, intersection, unclosed_poly, \
    is_contain, distance_between_points
from gefest.core.structure.structure import Structure


def check_constraints(structure: Structure, is_lightweight: bool = False, domain=None, model_func=None) -> bool:
    try:
        if any([(poly is None or
                 len(poly.points) == 0 or
                 any([pt is None for pt in poly.points]))
                for poly in structure.polygons]):
            print('Wrong structure - problems with points')
            return False

        cts = [out_of_bound(structure, domain),
               too_close(structure, domain),
               is_contain(structure, domain),
               self_intersection(structure),
               intersection(structure, domain),
               unclosed_poly(structure, domain),
               distance_between_points(structure, domain)]
        structurally_correct = not any(cts)

        if not structurally_correct:
            return structure
    except Exception as ex:
        print(ex)
        import traceback
        print(traceback.format_exc())
        return False

    return structure
