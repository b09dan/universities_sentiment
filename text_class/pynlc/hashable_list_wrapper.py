class HashableListWrapper(object):
    """
    Wrapper for "list" object that can calculate hash
    """
    def __init__(self, data):
        """
        Initialize wrapper
        :param data: source list
        :type data: list
        """
        super(HashableListWrapper, self).__init__()
        self._data = data
        self._hash = sum([item.__hash__() for item in data])

    def append(self, *args, **kwargs):
        return self._data.append(*args, **kwargs)

    def clear(self, *args, **kwargs):
        return self._data.clear(*args, **kwargs)

    def copy(self, *args, **kwargs):
        return self._data.copy(*args, **kwargs)

    def count(self, *args, **kwargs):
        return self._data.count(*args, **kwargs)

    def extend(self, *args, **kwargs):
        return self._data.extend(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self._data.index(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self._data.insert(*args, **kwargs)

    def pop(self, *args, **kwargs):
        return self._data.pop(*args, **kwargs)

    def remove(self, *args, **kwargs):
        return self._data.remove(*args, **kwargs)

    def reverse(self, *args, **kwargs):
        return self._data.reverse(*args, **kwargs)

    def sort(self, *args, **kwargs):
        return self._data.sort(*args, **kwargs)

    def __add__(self, *args, **kwargs):
        return self._data.__add__(*args, **kwargs)

    def __contains__(self, *args, **kwargs):
        return self._data.__contains__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        return self._data.__delitem__(*args, **kwargs)

    def __eq__(self, *args, **kwargs):
        return self._data.__eq__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        return self._data.__getitem__(*args, **kwargs)

    def __ge__(self, *args, **kwargs):
        return self._data.__ge__(*args, **kwargs)

    def __gt__(self, *args, **kwargs):
        return self._data.__gt__(*args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        return self._data.__iadd__(*args, **kwargs)

    def __imul__(self, *args, **kwargs):
        return self._data.__imul__(*args, **kwargs)

    def __iter__(self, *args, **kwargs):
        return self._data.__iter__(*args, **kwargs)

    def __len__(self, *args, **kwargs):
        return self._data.__len__(*args, **kwargs)

    def __le__(self, *args, **kwargs):
        return self._data.__le__(*args, **kwargs)

    def __lt__(self, *args, **kwargs):
        return self._data.__lt__(*args, **kwargs)

    def __mul__(self, *args, **kwargs):
        return self._data.__mul__(*args, **kwargs)

    def __ne__(self, *args, **kwargs):
        return self._data.__ne__(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return self._data.__repr__(*args, **kwargs)

    def __reversed__(self, *args, **kwargs):
        return self._data.__reversed__(*args, **kwargs)

    def __rmul__(self, *args, **kwargs):
        return self._data.__rmul__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        return self._data.__setitem__(*args, **kwargs)

    def __sizeof__(self, *args, **kwargs):
        return self._data.__sizeof__(*args, **kwargs)

    def __hash__(self):
        return self._hash
