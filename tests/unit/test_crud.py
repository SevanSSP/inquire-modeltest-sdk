"""
The resource APIs and resources against an in-memory stand-in for the v2 API: create, read, filter, update and delete
of campaigns, floater configurations, sensors, tests, timeseries and tags, and reading data, statistics, coordinates
and documents.
"""
import json
import re
from datetime import datetime
from unittest.mock import MagicMock
from urllib.parse import unquote
from uuid import uuid4

import matplotlib
import pytest
from qats import TimeSeries as QatsTimeseries, TsDB

from modeltestsdk import Client
from modeltestsdk.config import Config
from modeltestsdk.resources import (Campaign, CampaignDocument, FloaterConfig, FloaterTest, Sensor, Statistics, Tag,
                                    Timeseries, WaveCalibration, WindCalibration)
from modeltestsdk.utils import to_jsonable

matplotlib.use("Agg")

HOST = "https://modeltest.example"
TEST_TYPES = {"floatertest": "Floater Test", "wavecalibration": "Wave Calibration", "windcalibration": "Wind Calibration"}
TABLES = {"campaign": "campaign", "floaterconfig": "floaterconfig", "sensor": "sensor", "test": "test",
          "timeseries": "timeseries", "tags": "tags", **{k: "test" for k in TEST_TYPES}}
TIME = [0.0, 0.5, 1.0, 1.5, 2.0]
VALUE = [1.0, 2.0, 3.0, 2.0, 1.0]
DOCUMENTS = [dict(path="Main report/report.pdf", name="report.pdf", document_class="Main report", size_bytes=3,
                  modified="2026-11-02T10:00:00")]


def response(body, status=200):
    r = MagicMock()
    r.status_code = status
    r.json.return_value = body
    r.raise_for_status.return_value = None
    return r


class FakeAPI:
    """The v2 API's resource endpoints, in memory: POST creates, GET reads (filter_by eq only), PATCH, DELETE."""

    def __init__(self):
        self.rows = {table: {} for table in set(TABLES.values())}
        self.calls = []

    def __call__(self, method, url, params=None, json=None, headers=None, timeout=None):
        assert headers["Authorization"] == "Bearer abc"
        path = unquote(url[len(f"{HOST}/api/v1/"):])
        self.calls.append((method, path, params, json))
        resource, _, rest = path.partition("/")
        if rest.endswith("/data"):
            return response({"data": {"time": TIME, "value": VALUE}})
        if rest.endswith("/statistics"):
            return response(dict(timeseries_id=rest.split("/")[0], min=1.0, max=3.0, mean=1.8, n_points=5,
                                 window_start=params.get("start_time", 0.0), stored="start_time" not in params))
        if rest.endswith("/coordinates"):
            return response({"floaterconfig_id": rest.split("/")[0], "sensors": [], "problems": []})
        if rest.endswith("/documents"):
            return response(DOCUMENTS)
        rows = self.rows[TABLES[resource]]
        if method == "POST":
            row = dict(json, id=str(uuid4()))
            if resource in TEST_TYPES:
                row["type"] = TEST_TYPES[resource]
            rows[row["id"]] = row
            return response(row)
        if method == "GET" and not rest:
            found = [r for r in rows.values() if resource not in TEST_TYPES or r["type"] == TEST_TYPES[resource]]
            for expression in (params or {}).get("filter_by", "").split(","):
                if expression:
                    field, value = re.fullmatch(r"(\w+)\[eq\]=(.*)", expression).groups()
                    found = [r for r in found if str(r.get(field)) == value]
            return response(found[params.get("skip") or 0:][:params.get("limit") or None])
        if method == "GET":
            return response(rows[rest])
        if method == "PATCH":
            rows[rest].update(json)
            return response(rows[rest])
        if method == "DELETE":
            del rows[rest]
            return response(None)
        raise AssertionError(f"unexpected {method} {url}")  # pragma: no cover


@pytest.fixture
def api():
    return FakeAPI()


@pytest.fixture
def client(api):
    c = Client(Config(api_host=HOST), token="abc")
    c.session.request = api
    c._cached_session = MagicMock(request=api)  # get_data_points caches responses
    return c


@pytest.fixture
def campaign(client):
    c = Campaign(client=client, name="Bream FPSO", description="Sevan 650 FPSO", location="MARINTEK",
                 date=datetime(2014, 10, 1), scale_factor=65, water_depth=112.1, main_characteristic_length=82.0,
                 lab_axis_x="+x", lab_axis_y="+y", lab_axis_z="+z", z_origin="keel")
    c.create()
    return c


@pytest.fixture
def scene(client, campaign):
    """A floater config, a sensor, a wave and wind calibration, a floater test and a timeseries with a tag."""
    config = FloaterConfig(client=client, name="Loaded, in-line", description="", campaign_id=campaign.id,
                           characteristic_length=82.0, draft=24.79, heading=300.0, vcg=21.58,
                           geometry={"type": "circular", "diameter": 82.0, "height": 43.5})
    config.create()
    sensor = Sensor(client=client, campaign_id=campaign.id, name="ZPOS_WL", description="Heave", unit="m",
                    kind="length", source="direct measurement", x=0.0, y=0.0, z=0.0, position_reference="global",
                    position_heading_lock=False, position_draft_lock=False, position_z_reference="waterline",
                    positive_direction_definition="up", measures_frame="lab_local", measures_axis="z",
                    measures_sign=1, dof="heave")
    sensor.create()
    wave = WaveCalibration(client=client, number="8110", description="Hs 13.8", test_date=datetime(2014, 10, 1),
                           campaign_id=campaign.id, wave_spectrum="jonswap", wave_height=13.8, wave_period=17.0)
    wind = WindCalibration(client=client, number="9010", description="Wind", test_date=datetime(2014, 10, 1),
                           campaign_id=campaign.id, wind_spectrum="NPD", wind_velocity=30.0, zref=10.0,
                           wind_direction=0.0)
    for test in (wave, wind):
        test.create()
    floater = FloaterTest(client=client, number="3010", description="Irregular", test_date=datetime(2014, 10, 1),
                          campaign_id=campaign.id, category="irregular wave", orientation=300.0,
                          floaterconfig_id=config.id, wave_id=wave.id, wind_id=wind.id)
    floater.create(read_only=True)
    ts = Timeseries(client=client, sensor_id=sensor.id, test_id=floater.id, fs=10.0, default_start_time=0.5,
                    default_end_time=2.0)
    ts.create()
    tag = Tag(client=client, name="quality: questionable", comment="spike", timeseries_id=ts.id)
    tag.create()
    return dict(config=config, sensor=sensor, wave=wave, wind=wind, floater=floater, ts=ts, tag=tag)


def test_create_sends_the_v2_fields(api, campaign, scene):
    method, path, _, body = api.calls[0]
    assert (method, path) == ("POST", "campaign")
    assert body["main_characteristic_length"] == 82.0 and body["lab_axis_x"] == "+x" and body["z_origin"] == "keel"
    assert "client" not in body and "id" not in body and body["read_only"] is False
    config_body = next(b for m, p, _, b in api.calls if (m, p) == ("POST", "floaterconfig"))
    assert config_body["heading"] == 300.0 and config_body["geometry"]["type"] == "circular" and "turn" not in config_body
    sensor_body = next(b for m, p, _, b in api.calls if (m, p) == ("POST", "sensor"))
    assert sensor_body["measures_axis"] == "z" and sensor_body["dof"] == "heave"
    floater_body = next(b for m, p, _, b in api.calls if (m, p) == ("POST", "floatertest"))
    assert floater_body["type"] == "Floater Test" and floater_body["read_only"] is True
    assert scene["floater"].read_only is True and scene["ts"].id and scene["tag"].id
    json.dumps([b for *_, b in api.calls if b])  # every body is plain JSON


def test_create_needs_a_client():
    with pytest.raises(AttributeError, match="No client"):
        Campaign(name="x", description="", location="", date=datetime(2020, 1, 1), scale_factor=1,
                 water_depth=1).create()


def test_create_twice_keeps_the_id(api, campaign, capsys):
    first = campaign.id
    campaign.create()
    assert campaign.id == first and "already exists" in capsys.readouterr().out


def test_read_and_filter(client, campaign, scene):
    assert client.campaign.get_by_id(campaign.id).name == "Bream FPSO"
    assert client.campaign.get_by_name("Bream FPSO").scalar().id == campaign.id
    assert client.campaign.get().scalar().main_characteristic_length == 82.0
    assert campaign.floater_configurations().scalar().vcg == 21.58
    assert campaign.sensors().scalar().measures_frame == "lab_local"
    assert {t.type for t in campaign.tests()} == {"Floater Test", "Wave Calibration", "Wind Calibration"}
    assert client.sensor.get_by_name("ZPOS_WL").scalar().id == scene["sensor"].id
    assert client.sensor.get().scalar().position_z_reference == "waterline"
    assert client.floater_config.get().scalar().heading == 300.0
    assert client.test.get_by_number("3010").scalar().id == scene["floater"].id
    assert isinstance(client.test.get_by_id(scene["wave"].id), WaveCalibration)
    assert client.floater_test.get().scalar().id == scene["floater"].id
    assert client.wave_calibration.get().scalar().wave_height == 13.8
    assert client.wind_calibration.get_by_id(scene["wind"].id).wind_velocity == 30.0
    assert client.timeseries.get().scalar().fs == 10.0
    ts = client.timeseries.get_by_sensor_id_and_test_id(scene["sensor"].id, scene["floater"].id)
    assert ts.id == scene["ts"].id
    assert client.timeseries.get_by_sensor_id_and_test_id(scene["sensor"].id, scene["wave"].id) is None
    assert client.timeseries.get_by_test_id(scene["floater"].id).scalar().id == ts.id
    assert client.tag.get().scalar().name == "quality: questionable"
    assert client.tag.get_by_name("quality: questionable").scalar().id == scene["tag"].id
    assert client.tag.get_by_test_id(scene["floater"].id).scalar() is None
    assert client.tag.get_by_id(scene["tag"].id).comment == "spike"


def test_relations(client, scene):
    floater, ts, tag, sensor = scene["floater"], scene["ts"], scene["tag"], scene["sensor"]
    assert floater.wave_calibration.id == scene["wave"].id and floater.wind_calibration.id == scene["wind"].id
    assert floater.floater_config.id == scene["config"].id
    assert scene["wave"].floater_tests().scalar().id == floater.id
    assert scene["wind"].floater_tests().scalar().id == floater.id
    assert floater.timeseries().scalar().id == ts.id and floater.timeseries(sensor_id=sensor.id).id == ts.id
    assert floater.tags().scalar() is None
    assert sensor.timeseries().scalar().id == ts.id and sensor.tags().scalar() is None
    assert ts.sensor.id == sensor.id and ts.test.id == floater.id and ts.tags().scalar().id == tag.id
    assert tag.timeseries.id == ts.id and tag.sensor is None and tag.test is None
    sensor_tag = Tag(client=client, name="comment", sensor_id=sensor.id)
    test_tag = Tag(client=client, name="comment", test_id=floater.id)
    assert sensor_tag.sensor.id == sensor.id and test_tag.test.id == floater.id
    assert Tag(client=client, name="comment", test_id=scene["wave"].id).test.id == scene["wave"].id
    assert Tag(client=client, name="comment", test_id=scene["wind"].id).test.id == scene["wind"].id


def test_update_and_delete(api, client, campaign, scene):
    scene["config"].vcg = 21.73
    scene["config"].update()
    method, path, _, body = api.calls[-1]
    assert (method, path) == ("PATCH", f"floaterconfig/{scene['config'].id}")
    assert body["vcg"] == 21.73 and "id" not in body and "read_only" not in body
    assert client.floater_config.get_by_id(scene["config"].id).vcg == 21.73
    client.timeseries.update(scene["ts"].id, {"default_start_time": 1.0})
    assert client.timeseries.get_by_id(scene["ts"].id).default_start_time == 1.0

    scene["tag"].delete()
    scene["floater"].delete()
    assert api.calls[-1][:2] == ("DELETE", f"test/{scene['floater'].id}")
    campaign.delete()
    assert api.calls[-1][:2] == ("DELETE", f"campaign/{campaign.id}")
    assert not api.rows["campaign"] and not api.rows["tags"]


def test_data_and_statistics(api, client, scene, capsys):
    ts = scene["ts"]
    dps = ts.get_data(start=0.5, end=2.0)
    assert dps.time == TIME and dps.value == VALUE and dps.timeseries_id == ts.id and len(dps) == 5
    assert "WARNING" in capsys.readouterr().out  # the quality tag
    params = next(p for m, p_, p, _ in api.calls if p_.endswith("/data"))
    assert params == {"start_time": 0.5, "end_time": 2.0, "all_data": False}  # None isn't sent
    assert list(dps.to_pandas().iloc[:, 0]) == VALUE
    assert isinstance(ts.get_qats_ts(), QatsTimeseries) and isinstance(dps.to_qats_ts(), QatsTimeseries)
    ts.plot(show=False)
    lst = client.timeseries.get()
    assert isinstance(lst.get_qats_tsdb(), TsDB) and len(lst.get_data()) == 1
    lst.plot(show=False)

    stored = ts.get_statistics()
    assert isinstance(stored, Statistics) and stored.stored is True and stored.max == 3.0
    window = ts.get_statistics(start=1.0, end=2.0)
    assert window.stored is False and window.window_start == 1.0
    assert api.calls[-1][2] == {"start_time": 1.0, "end_time": 2.0}


def test_coordinates(client, scene):
    assert scene["config"].coordinates() == {"floaterconfig_id": scene["config"].id, "sensors": [], "problems": []}


def test_documents(client, campaign, tmp_path):
    docs = campaign.documents()
    assert docs == [CampaignDocument(**DOCUMENTS[0])]

    r = MagicMock()
    r.__enter__.return_value = r
    r.iter_content.return_value = [b"PD", b"F"]
    client.session.get = MagicMock(return_value=r)
    target = campaign.download_document(docs[0].path, tmp_path)
    assert target == tmp_path / "report.pdf" and target.read_bytes() == b"PDF"
    url = client.session.get.call_args.args[0]
    assert url == f"{HOST}/api/v1/campaign/{campaign.id}/documents/Main%20report/report.pdf"
    assert client.session.get.call_args.kwargs["params"] == {"download": True}
    assert client.session.get.call_args.kwargs["stream"] is True
    named = client.campaign.download_document(campaign.id, docs[0].path, tmp_path / "copy.pdf")
    assert named.read_bytes() == b"PDF"


def test_to_pandas(campaign, scene):
    assert campaign.to_pandas().loc["name", "value"] == "Bream FPSO"
    df = campaign.floater_configurations().to_pandas()
    assert df.loc[0, "geometry"]["type"] == "circular"
    assert to_jsonable(df.loc[0, "heading"]) == 300.0
