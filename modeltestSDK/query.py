"""
Classes and functions enabling advanced API queries
"""


class FilterAttribute:
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


class SortAttribute:
    def __init__(self, name):
        self.name = name

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


def class_factory(name: str, method_spec: str, attribute_list: list):
    def init():
        pass

    attr_dict = {'__init__': init}
    if method_spec == 'sort' or method_spec == 'both':
        for attr in attribute_list:
            attr_dict[attr] = SortAttribute(attr)
    if method_spec == 'filter' or method_spec == 'both':
        for attr in attribute_list:
            attr_dict[attr] = FilterAttribute(attr)

    return type(name, (object,), attr_dict)


class Query:
    def __init__(self, method_spec: str = 'both'):
        self.campaign = class_factory(name='Campaign', method_spec=method_spec,
                                      attribute_list=['name',
                                                      'description',
                                                      'date',
                                                      'location',
                                                      'scale_factor',
                                                      'water_depth',
                                                      'read_only',
                                                      'id'])
        self.sensor = class_factory(name="Sensor", method_spec=method_spec,
                                    attribute_list=['name',
                                                    'description',
                                                    'unit',
                                                    'kind', 'area',
                                                    'x',
                                                    'y',
                                                    'z',
                                                    'is_local',
                                                    'campaign_id',
                                                    'read_only',
                                                    'id',
                                                    'tag_name'])
        self.test = class_factory(name="Test", method_spec=method_spec,
                                  attribute_list=['number',
                                                  'description',
                                                  'test_date',
                                                  'campaign_id',
                                                  'type',
                                                  'id'])
        self.timeseries = class_factory(name="Timeseries", method_spec=method_spec,
                                        attribute_list=['sensor_id',
                                                        'test_id',
                                                        'fs',
                                                        'intermittent',
                                                        'default_start_time',
                                                        'default_end_time',
                                                        'read_only',
                                                        'id',
                                                        'datapoints_created_at'])
        self.wave_calibration = class_factory(name="Wavecalibration", method_spec=method_spec,
                                              attribute_list=['number',
                                                              'description',
                                                              'test_date',
                                                              'campaign_id',
                                                              'type',
                                                              'wave_spectrum',
                                                              'wave_height',
                                                              'wave_period',
                                                              'gamma',
                                                              'wave_direction',
                                                              'current_velocity',
                                                              'current_direction',
                                                              'read_only',
                                                              'id'])

        self.wind_calibration = class_factory(name="Windcalibration", method_spec=method_spec,
                                              attribute_list=['number',
                                                              'description',
                                                              'test_date',
                                                              'campaign_id',
                                                              'type',
                                                              'wind_spectrum',
                                                              'wind_velocity',
                                                              'zref',
                                                              'wind_direction',
                                                              ' read_only',
                                                              'id'])
        self.floater_test = class_factory(name="Floatertest", method_spec=method_spec,
                                          attribute_list=['number',
                                                          'description',
                                                          'test_date',
                                                          'campaign_id',
                                                          'type',
                                                          'category',
                                                          'orientation',
                                                          'wave_id',
                                                          'wind_id',
                                                          'floaterconfig_id',
                                                          'read_only',
                                                          'id'])
        self.tags = class_factory(name="Tags", method_spec=method_spec,
                                  attribute_list=['comment',
                                                  'test_id',
                                                  'sensor_id',
                                                  'timeseries_id',
                                                  'read_only',
                                                  'name',
                                                  'id'])
        self.floater_config = class_factory(name="Floaterconfig", method_spec=method_spec,
                                            attribute_list=['name',
                                                            'description',
                                                            'characteristic_length',
                                                            'campaign_id',
                                                            ' draft',
                                                            'read_only',
                                                            'id'])


def create_query_parameters(filter_expressions: list, sorting_expressions: list) -> dict:
    """
    Create query parameters

    Parameters
    ----------
    filter_expressions: List[dict]
        Filtering parameters [{'name': draft, 'op': gt, 'val':30}]
    sorting_expressions: List[dict]
        Sorting parameters [{'name': height, 'op': asc}]

    Returns
    -------
    dict
        Query parameters for URL
    """
    filter_s = ''
    for query_filter in filter_expressions:
        if not filter_s == '':
            filter_s = filter_s + ','
        if not type(query_filter['val']) == str:
            query_filter['val'] = str(query_filter['val'])
        filter_s = filter_s + query_filter['name'] + '[' + query_filter['op'] + ']' + '=' + query_filter['val']

    if sorting_expressions == [] or filter_expressions == []:
        sort_filter = ''
    else:
        sort_filter = ''

    sort_str = ''
    for sort_parameter in sorting_expressions:
        if not sort_str == '':
            sort_str = sort_str + ','
        sort_str = sort_str + sort_parameter['op'] + '(' + sort_parameter['name'] + ')'

    parameters = dict()
    if filter_s != "":
        parameters["filter_by"] = filter_s + sort_filter

    if sort_str != "":
        parameters["sort_by"] = sort_str

    return parameters
