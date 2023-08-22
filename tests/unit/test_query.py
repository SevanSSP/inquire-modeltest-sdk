from modeltestSDK import query


def test_filter_attributes():
    flt_attr = query.FilterAttribute('name')

    assert (flt_attr == 1) == dict(name='name', op='eq', val=1)
    assert (flt_attr < 1) == dict(name='name', op='lt', val=1)
    assert (flt_attr <= 1) == dict(name='name', op='lte', val=1)
    assert (flt_attr > 1) == dict(name='name', op='gt', val=1)
    assert (flt_attr >= 1) == dict(name='name', op='gte', val=1)
    assert flt_attr.contains(1) == dict(name='name', op='co', val=1)


def test_sort_attributes():
    sort_attr = query.SortAttribute('name')

    assert sort_attr.ascending == dict(name='name', op='asc')
    assert sort_attr.asc == dict(name='name', op='asc')
    assert sort_attr.descending == dict(name='name', op='desc')
    assert sort_attr.desc == dict(name='name', op='desc')


def test_class_factory():
    class Foo:
        pass

    foo = query.class_factory(name='Foo', method_spec='filter', attribute_list=['name'])

    assert (foo.name == 1) == dict(name='name', op='eq', val=1)


def test_query_parameters():
    flt_attr_1 = query.FilterAttribute('name')
    flt_attr_2 = query.FilterAttribute('type')
    sort_attr_1 = query.SortAttribute('name')
    sort_attr_2 = query.SortAttribute('type')

    flt_exp = [flt_attr_1 == 1, flt_attr_2 >= 1]
    sort_exp = [sort_attr_1.asc, sort_attr_2.desc]

    assert query.create_query_parameters(flt_exp, sort_exp) == {'filter_by': 'name[eq]=1,type[gte]=1',
                                                                'sort_by': 'asc(name),desc(type)'}
    assert query.create_query_parameters(flt_exp, []) == {'filter_by': 'name[eq]=1,type[gte]=1'}
    assert query.create_query_parameters([], sort_exp) == {'sort_by': 'asc(name),desc(type)'}
    assert query.create_query_parameters([], []) == {}
