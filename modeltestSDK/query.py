class CompAttribute:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return dict(name=self.name, op='eq', val=other)

    def __lt__(self, other):
        return dict(name=self.name, op='lt', val=other)

    def __le__(self, other):
        return dict(name=self.name, op='lte', val=other)

    def __gt__(self, other):
        return dict(name=self.name, op='gt', val=other)

    def __ge__(self, other):
        return dict(name=self.name, op='gte', val=other)

    @property
    def ascending(self):
        return dict(name=self.name, op='asc')

    @property
    def asc(self):
        return self.ascending

    @property
    def descending(self):
        return dict(name=self.name, op='desc')

    @property
    def desc(self):
        return self.descending


def class_factory(name: str, attribute_list: list):
    def init(self, name, **kwargs):
        self.name = name
        for kwarg in kwargs:
            if kwarg in attribute_list:
                setattr(self, kwarg, CompAttribute(kwarg))

    attr_dict = {'__init__': init}
    for attr in attribute_list:
        attr_dict[attr] = CompAttribute(attr)
    return type(name, (object,), attr_dict)


class Query:
    def __init__(self):
        self.campaign = class_factory(name='Campaign', attribute_list=['name',
                                                                       'description',
                                                                       'date',
                                                                       'location',
                                                                       'scale_factor',
                                                                       'water_depth',
                                                                       'read_only',
                                                                       'id'])
        # TODO: add the others
        self.sensor = class_factory(name="Sensor", attribute_list=['name',
                                                                   'description',
                                                                   'value'])