import itertools
from flask import url_for


class Pagination(object):
    def __init__(self, request, default_limit=20):
        self.get_args = request.args.to_dict()
        self.limit = max(int(self.get_args.get("limit", default_limit)), 0)
        self.offset = max(int(self.get_args.get("offset", 0)), 0)
        self.request = request

    def url_next_page(self, query_count=None):
        if query_count == self.limit or query_count is None:
            self.get_args["offset"] = self.offset + self.limit
            return url_for(self.request.endpoint, **dict(self.request.view_args.items() + self.get_args.items()))
        else:
            return None

    def url_prev_page(self):
        if self.offset > 0:
            self.get_args["offset"] = max(self.offset - self.limit, 0)
            return url_for(self.request.endpoint, **dict(self.request.view_args.items() + self.get_args.items()))
        else:
            return None


def diff(lhs_seq, rhs_seq, eq=None):
    '''
    Computes a diff of two sequences.

    Algorithm is based on Longest Common Subsequence problem.

    Returns a list of pairs. Each pair consists from either a value from the
    first sequence and None or from None and a value from the second sequence
    or values from both sequences.

    >>> diff(banana, ananas)
    [('b', None), ('a', 'a'), ('n', 'n'), ('a', 'a'), ('n', 'n'), ('a', 'a'), (None, 's')]
    '''
    if not eq:
        eq = lambda x, y: x == y

    result = list()
    l = 0
    l_e = len(lhs_seq) - 1
    r = 0
    r_e = len(rhs_seq) - 1
    # handle common prefix
    while l <= l_e and r <= r_e and eq(lhs_seq[l], rhs_seq[r]):
        result.append((lhs_seq[l], rhs_seq[r]))
        l += 1
        r += 1

    end_result = list()
    # handle common suffix
    while l <= l_e and r <= r_e and eq(lhs_seq[l_e], rhs_seq[r_e]):
        end_result.append((lhs_seq[l_e], rhs_seq[r_e]))
        l_e -= 1
        r_e -= 1

    matrix_row_len = (r_e - r) + 2
    # build matrix which has one more column and line than rhs x lhs
    m = list(itertools.repeat(0, ((l_e - l) + 2) * matrix_row_len))

    # skip first row because it contains only 0
    pos = matrix_row_len

    # in case where strings are the same l has value len(left) == l_e + 1
    i = l_e
    # in case where strings are the same r has value len(right) == r_e + 1
    j = r_e

    for i in xrange(l, l_e + 1):
        pos += 1 # skip first column which is always 0
        for j in xrange(r, r_e + 1):
            if eq(lhs_seq[i], rhs_seq[j]):
                res = m[pos - matrix_row_len - 1] + 1
            else:
                res = max(m[pos - matrix_row_len], m[pos - 1])
            m[pos] = res
            pos += 1

    pos -= 1 # current value is len(m)
    i += 1   # current value is last of xrange(l, l_e + 1)
    j += 1   # current value is last of xrange(r, r_e + 1)
    while i != l and j != r:
        if m[pos] == m[pos - 1]:
            pos -= 1
            j -= 1
            end_result.append((None, rhs_seq[j]))
        elif m[pos] == m[pos - matrix_row_len]:
            pos -= matrix_row_len
            i -= 1
            end_result.append((lhs_seq[i], None))
        else:
            pos -= matrix_row_len
            pos -= 1
            i -= 1
            j -= 1
            end_result.append((lhs_seq[i], rhs_seq[j]))

    while i != l:
        i -= 1
        end_result.append((lhs_seq[i], None))

    while j != r:
        j -= 1
        end_result.append((None, rhs_seq[j]))

    end_result.reverse()
    return result + end_result