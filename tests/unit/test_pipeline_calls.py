import hashlib
from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import numpy as np
import pytest
import requests

from modeltestsdk import Client
from modeltestsdk.config import Config
from modeltestsdk.resources import Campaign, FloaterTest, Sensor, WaveCalibration
from modeltestsdk.utils import to_jsonable

HOST = "https://modeltest.example"
CAMPAIGN_ID, TEST_ID, RUN_ID = str(uuid4()), str(uuid4()), str(uuid4())


def response(json_body, status=200, headers=None):
    r = MagicMock()
    r.status_code = status
    r.headers = headers or {}
    r.json.return_value = json_body
    if status >= 400:
        r.raise_for_status.side_effect = requests.exceptions.HTTPError(str(status))
    else:
        r.raise_for_status.return_value = None
    return r


@pytest.fixture
def client():
    c = Client(Config(api_host=HOST, requests_max_retries=2, requests_backoff_factor=0.5), token="abc")
    c.session.request = MagicMock()
    return c


def sent(client):
    args, kwargs = client.session.request.call_args
    return args[0], args[1], kwargs["json"]


def campaign_data(**kwargs):
    return dict(id=CAMPAIGN_ID, name="Mariner", description="d", location="Marintek", date="2011-05-01T00:00:00",
                scale_factor=65, water_depth=120, read_only=True, data_format="MARINTEK_POST_2019", **kwargs)


def test_campaign_upsert(client):
    client.session.request.return_value = response(campaign_data(status="created"))
    campaign = client.campaign.upsert(dict(name="Mariner", date=datetime(2011, 5, 1), scale_factor=np.float64(65)))
    assert sent(client) == ("PUT", f"{HOST}/api/v1/campaign",
                            {"name": "Mariner", "date": "2011-05-01T00:00:00", "scale_factor": 65.0})
    assert isinstance(campaign, Campaign) and campaign.id == CAMPAIGN_ID and campaign.upsert_status == "created"
    assert campaign.client is client


def test_resources_send_only_fields_that_are_set(client):
    client.session.request.return_value = response([])
    sensor = Sensor(id=str(uuid4()), campaign_id=CAMPAIGN_ID, name="HEAVE", description="", unit="m", kind="length",
                    source="direct measurement", x=0, y=0, position_reference="local",
                    position_heading_lock=False, position_draft_lock=False, positive_direction_definition="up")
    client.sensor.upsert_many(CAMPAIGN_ID, [sensor])
    body = sent(client)[2][0]
    assert body["name"] == "HEAVE" and "z" not in body and "area" not in body
    assert "id" not in body and "client" not in body


@pytest.mark.parametrize("api, method, path", [
    ("floater_config", "floaterconfigs", f"campaign/{CAMPAIGN_ID}/floaterconfigs"),
    ("sensor", "sensors", f"campaign/{CAMPAIGN_ID}/sensors"),
    ("tag", "tags", f"campaign/{CAMPAIGN_ID}/tags"),
])
def test_campaign_batch_upserts(client, api, method, path):
    items = {
        "floater_config": dict(name="GM8", description="", characteristic_length=70.0, draft=15.0),
        "sensor": dict(name="HEAVE", description="", unit="m", kind="length", source="direct measurement", x=0, y=0,
                       z=None, position_reference="local", position_heading_lock=False,
                       position_draft_lock=False, positive_direction_definition="up"),
        "tag": dict(name="failed", comment=None, test_id=TEST_ID),
    }[api]
    stored = [dict(items, id=str(uuid4()), campaign_id=CAMPAIGN_ID, status="unchanged")]
    client.session.request.return_value = response(stored)
    result = getattr(client, api).upsert_many(CAMPAIGN_ID, [items])
    assert sent(client) == ("PUT", f"{HOST}/api/v1/{path}", [items])
    assert len(result) == 1 and result[0].id == stored[0]["id"] and result[0].upsert_status == "unchanged"


def test_test_upserts_by_type(client):
    wave = WaveCalibration(number="8110", description="100 yr", test_date=datetime(2011, 5, 1),
                           campaign_id=CAMPAIGN_ID, type="Wave Calibration", wave_spectrum="jonswap",
                           wave_height=13.8, wave_period=17.0, gamma=1.5, wave_direction=0.0, current_velocity=0.0,
                           current_direction=None)
    floater = FloaterTest(number="6", description="decay", test_date=datetime(2011, 5, 1), campaign_id=CAMPAIGN_ID,
                          category="decay", orientation=0.0)  # type left at its default
    stored = [dict(wave.model_dump(exclude={"client"}, mode="json"), id=str(uuid4()), status="created"),
              dict(floater.model_dump(exclude={"client"}, mode="json"), id=str(uuid4()), status="updated")]
    client.session.request.return_value = response(stored)

    tests = client.floater_test.upsert_many(CAMPAIGN_ID, [wave, dict(type="Floater Test", number="6")])
    method, url, body = sent(client)
    assert url == f"{HOST}/api/v1/campaign/{CAMPAIGN_ID}/tests"  # not floatertest/...
    assert body[0]["type"] == "Wave Calibration" and body[0]["current_direction"] is None
    assert isinstance(tests[0], WaveCalibration) and isinstance(tests[1], FloaterTest)
    assert [t.upsert_status for t in tests] == ["created", "updated"]

    client.test.upsert_many(CAMPAIGN_ID, [floater])
    assert sent(client)[2][0]["type"] == "Floater Test"


def test_timeseries_upsert(client):
    item = dict(sensor_id=str(uuid4()), fs=np.float32(12.5), intermittent=False, default_start_time=np.nan,
                default_end_time=12306.0)
    client.session.request.return_value = response([dict(item, fs=12.5, default_start_time=None, id=str(uuid4()),
                                                         test_id=TEST_ID, status="created")])
    ts = client.timeseries.upsert_many(TEST_ID, [item])
    method, url, body = sent(client)
    assert url == f"{HOST}/api/v1/test/{TEST_ID}/timeseries"
    assert body[0]["fs"] == 12.5 and body[0]["default_start_time"] is None
    assert ts[0].test_id == TEST_ID and ts[0].upsert_status == "created"


def test_import_runs(client):
    run = dict(id=RUN_ID, campaign_id=CAMPAIGN_ID, status="running", started_at="2026-10-12T10:00:00",
               pipeline_version="2.0.0")
    client.session.request.return_value = response(run)
    started = client.import_runs.start(CAMPAIGN_ID, pipeline_version="2.0.0", workbook_name="Pipeline_Input.xls")
    method, url, body = sent(client)
    assert (method, url) == ("POST", f"{HOST}/api/v1/importrun")
    assert body["campaign_id"] == CAMPAIGN_ID and body["sdk_version"] and "workbook_sha256" not in body
    assert started.status == "running" and started.id == RUN_ID

    client.session.request.return_value = response(dict(run, status="partial", summary={"tests_failed": 1}))
    finished = client.import_runs.finish(RUN_ID, "partial", summary={"tests_failed": np.int64(1)},
                                         failures=[{"test_number": "3010", "error": "no file"}])
    method, url, body = sent(client)
    assert (method, url) == ("PATCH", f"{HOST}/api/v1/importrun/{RUN_ID}")
    assert body == {"status": "partial", "summary": {"tests_failed": 1},
                    "failures": [{"test_number": "3010", "error": "no file"}]}
    assert finished.summary == {"tests_failed": 1}

    client.session.request.return_value = response(run)
    assert client.import_runs.get_by_id(RUN_ID).pipeline_version == "2.0.0"


def datafile(**kwargs):
    values = dict(id=str(uuid4()), test_id=TEST_ID, group=0, sha256="a" * 64, size_bytes=10, n_rows=3,
                  blob_path="x.parquet", format_version=1, import_run_id=RUN_ID, created_at="2026-10-12T10:00:00")
    values.update(kwargs)
    return values


def test_active_datafiles(client):
    client.session.request.return_value = response([datafile(status="active", timeseries_ids=[str(uuid4())])])
    files = client.test.active_datafiles(TEST_ID)
    args, kwargs = client.session.request.call_args
    assert args == ("GET", f"{HOST}/api/v1/test/{TEST_ID}/datafiles") and kwargs["params"] == {"status": "active"}
    assert files[0].sha256 == "a" * 64 and len(files[0].timeseries_ids) == 1

    client.wave_calibration.datafiles(TEST_ID)
    args, kwargs = client.session.request.call_args
    assert args[1] == f"{HOST}/api/v1/test/{TEST_ID}/datafiles" and kwargs["params"] == {}


@pytest.fixture
def upload(client, tmp_path, monkeypatch):
    path = tmp_path / "file.parquet"
    path.write_bytes(b"parquet bytes")
    sleeps = []
    monkeypatch.setattr("modeltestsdk.client.time.sleep", sleeps.append)
    bodies = []

    def put(url, data, headers, timeout):
        bodies.append(data.read())
        return next(responses)

    client._upload_session.put = MagicMock(side_effect=put)
    responses = iter([])

    def run(*results):
        nonlocal responses
        responses = iter(results)
        return client.test.upload_datafile(TEST_ID, 0, path, RUN_ID)

    run.path, run.sleeps, run.bodies = path, sleeps, bodies
    return run


def uploaded(status="created"):
    return response(datafile(status=status, superseded_id=None, timeseries=[
        {"timeseries_id": str(uuid4()), "n_points": 3, "t_first": 0.0, "t_last": 0.2,
         "statistics": {"min": 1.0, "max": 3.0, "std": None, "n_points": 3, "stored": True}}]),
        status=201 if status == "created" else 200)


def test_upload_datafile(client, upload):
    result = upload(uploaded())
    url = client._upload_session.put.call_args.args[0]
    headers = client._upload_session.put.call_args.kwargs["headers"]
    assert url == f"{HOST}/api/v1/test/{TEST_ID}/datafiles/0"
    assert headers["X-Content-SHA256"] == hashlib.sha256(b"parquet bytes").hexdigest()
    assert headers["X-Import-Run-Id"] == RUN_ID and headers["Content-Type"] == "application/vnd.apache.parquet"
    assert headers["Authorization"] == "Bearer abc"
    assert client._upload_session.put.call_args.kwargs["timeout"] == (60.0, 900.0)
    assert result.status == "created" and result.timeseries[0].statistics.std is None
    assert upload.bodies == [b"parquet bytes"]


def test_upload_retries_busy_and_server_errors(client, upload):
    result = upload(response({}, 429, {"Retry-After": "10"}), response({}, 503), uploaded("unchanged"))
    assert result.status == "unchanged"
    assert upload.sleeps == [10.0, 1.0]  # Retry-After, then backoff 0.5 * 2 ** 1
    assert upload.bodies == [b"parquet bytes"] * 3  # the file is sent again in full


def test_upload_retries_connection_errors_then_gives_up(client, upload):
    client._upload_session.put = MagicMock(side_effect=requests.exceptions.ConnectionError("reset"))
    with pytest.raises(requests.exceptions.ConnectionError):
        upload()
    assert client._upload_session.put.call_count == 3 and upload.sleeps == [0.5, 1.0]


def test_upload_errors_are_not_retried(client, upload):
    with pytest.raises(requests.exceptions.HTTPError):
        upload(response({"detail": {"code": "invalid_parquet"}}, 422))
    assert client._upload_session.put.call_count == 1


def test_upload_gives_up_when_busy(client, upload):
    with pytest.raises(requests.exceptions.HTTPError):
        upload(*[response({}, 429, {"Retry-After": "soon"})] * 3)
    assert upload.sleeps == [0.5, 1.0]


def test_upload_with_known_sha256(client, upload):
    client._upload_session.put = MagicMock(return_value=uploaded())
    client.test.upload_datafile(TEST_ID, 1, upload.path, RUN_ID, sha256="b" * 64)
    assert client._upload_session.put.call_args.kwargs["headers"]["X-Content-SHA256"] == "b" * 64
    assert client._upload_session.put.call_args.args[0].endswith("/datafiles/1")


def test_to_jsonable():
    some_id = uuid4()
    body = {"a": (np.int32(1), np.nan, some_id), "b": np.array([1.5, np.nan]), "c": datetime(2020, 1, 1)}
    assert to_jsonable(body) == {"a": [1, None, str(some_id)], "b": [1.5, None], "c": "2020-01-01T00:00:00"}
    assert to_jsonable(np.inf) == np.inf
