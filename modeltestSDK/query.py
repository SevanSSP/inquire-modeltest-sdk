import urllib.parse

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
        self.test = class_factory(name="Test", attribute_list=['number',
                                                               'description',
                                                               'test_date',
                                                               'campaign_id',
                                                               'type',
                                                               'id'])
        self.timeseries = class_factory(name="Timeseries", attribute_list=['sensor_id',
                                                                           'test_id',
                                                                           'fs',
                                                                           'intermittent',
                                                                           'default_start_time',
                                                                           'default_end_time',
                                                                           'read_only',
                                                                           'id',
                                                                           'datapoints_created_at'])
        self.wave_calibration = class_factory(name="Wavecalibration", attribute_list=['number',
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

        self.wind_calibration = class_factory(name="Windcalibration", attribute_list=['number',
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
        self.floater_test = class_factory(name="Floatertest", attribute_list=['number',
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
        self.tags = class_factory(name="Tags", attribute_list=['comment',
                                                               'test_id',
                                                               'sensor_id',
                                                               'timeseries_id',
                                                               'read_only',
                                                               'name',
                                                               'id'])
        self.floater_config = class_factory(name="Floaterconfig", attribute_list=['name',
                                                                                  'description',
                                                                                  'characteristic_length',
                                                                                  'campaign_id',
                                                                                  ' draft',
                                                                                  'read_only',
                                                                                  'id'])


def query_dict_to_url(query_filters: list, query_sort_parameters: list) -> str:
    """
    :param query_filters: List of dicts with filtering parameters [{'name': draft, 'op': gt, 'val':30}]
    :param query_sort_parameters: list of dicts with sorting parameters [{'name': height, 'op': asc}]
    :return: query string for url-request
    """

    filter_s = ''
    for query_filter in query_filters:
        if not filter_s == '':
            filter_s = filter_s + ','
        if not type(query_filter['val']) == str:
            query_filter['val'] = str(query_filter['val'])
        filter_s = filter_s + query_filter['name'] + '[' + query_filter['op'] + ']' + '=' + query_filter['val']

    if query_sort_parameters == [] or query_filters == []:
        sort_filter = ''
    else:
        sort_filter = '&'

    sort_str = ''
    for sort_parameter in query_sort_parameters:
        if not sort_str == '':
            sort_str = sort_str + ','
        sort_str = sort_str + sort_parameter['op'] + '(' + sort_parameter['name'] + ')'

    if not filter_s == '':
        filter_by = 'filter_by='
    else:
        filter_by = ''

    if not sort_str == '':
        sort_by = 'sort_by='
    else:
        sort_by = ''

    return filter_by + urllib.parse.quote(filter_s) + sort_filter + sort_by + urllib.parse.quote(sort_str)
