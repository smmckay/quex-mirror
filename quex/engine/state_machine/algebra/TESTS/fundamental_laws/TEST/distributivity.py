from quex.engine.state_machine.algebra.TESTS.fundamental_laws.TEST.helper import test3

count = 0

def distributivity(A, B, C):
    first  = union(A, intersection(B, C))
    second = intersection(union(A, B), union(A,C))
    assert identity(first, second)

    first  = intersection(A, union(B, C))
    second = union(intersection(A, B), intersection(A,C))
    assert identity(first, second)

    count += 1

for A, B, C in test3_list:
    test3(A, B, C, distributivity)

print "<terminated: %i>" % count
