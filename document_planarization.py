import copy


def document_planarization(document: dict) -> list:
    """                                     
    data = {
        "a": "a",
        "b": [{"b1": "b1", }, {"b2": "b2"}],
        "c": [{"c1": "c1", }, {"c2": "c2"}],
        "d": ["d1", "d2"]
    }
    ---->
    data = [
        {'a': 'a', 'b': {'b1': 'b1'}, 'c': {'c1': 'c1'}, 'd': 'd1'}
        {'a': 'a', 'b': {'b1': 'b1'}, 'c': {'c1': 'c1'}, 'd': 'd2'}
        {'a': 'a', 'b': {'b1': 'b1'}, 'c': {'c2': 'c2'}, 'd': 'd1'}
        {'a': 'a', 'b': {'b1': 'b1'}, 'c': {'c2': 'c2'}, 'd': 'd2'}
        {'a': 'a', 'b': {'b2': 'b2'}, 'c': {'c1': 'c1'}, 'd': 'd1'}
        {'a': 'a', 'b': {'b2': 'b2'}, 'c': {'c1': 'c1'}, 'd': 'd2'}
        {'a': 'a', 'b': {'b2': 'b2'}, 'c': {'c2': 'c2'}, 'd': 'd1'}
        {'a': 'a', 'b': {'b2': 'b2'}, 'c': {'c2': 'c2'}, 'd': 'd2'}
    ]
    """

    def has_list_value(data_dict_or_list) -> bool:
        """判断一个列表或字典中是否存在值为list.
        Tips: 列表中只能为字典元素！！！
        """
        if isinstance(data_dict_or_list, dict):
            return True in [
                isinstance(v, list)
                for v in data_dict_or_list.values()
            ]
        elif isinstance(data_dict_or_list, list):
            _has_list_value = []
            for d in data_dict_or_list:
                for v in d.values():
                    _has_list_value.append(isinstance(v, list))
            return True in _has_list_value

    target_fields = [
        field
        for field, value in document.items()
        if isinstance(value, list) and value
    ]

    if not target_fields: return [document, ] if isinstance(document, dict) else document

    target_fields_one = target_fields[0]

    copy_document = copy.deepcopy(document)
    copy_document.pop(target_fields_one)

    data_list = []
    for d in document[target_fields_one]:
        diction = copy.deepcopy(copy_document)
        diction[target_fields_one] = d

        data_list.append(diction)

    if not has_list_value(data_list):
        return data_list
    else:
        children_data_list = []
        for i in data_list:
            children_data_list += document_planarization(i)

        return children_data_list


data = {
    "a": "a",
    # "b": [{"b1": "b1", }, {"b2": "b2"}],
    # "c": [{"c1": "c1", }, {"c2": "c2"}],
    # "d": ["d1", "d2"]
}
s = document_planarization(data)
print(s)
