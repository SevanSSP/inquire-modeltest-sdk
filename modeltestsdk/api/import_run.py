from importlib.metadata import PackageNotFoundError, version

from modeltestsdk.resources import ImportRun
from modeltestsdk.utils import to_jsonable
from .base import BaseAPI


def installed_sdk_version() -> str:
    try:
        return version("modeltestsdk")
    except PackageNotFoundError:  # pragma: no cover - running from a source tree
        return "unknown"


class ImportRunAPI(BaseAPI):
    """Import runs: one execution of the import pipeline for a campaign, the provenance of its data files."""

    def start(self, campaign_id: str, pipeline_version: str = None, workbook_name: str = None,
              workbook_sha256: str = None, sdk_version: str = None) -> ImportRun:
        """
        Start an import run for a campaign. Data files are uploaded within a running import run.

        Parameters
        ----------
        campaign_id : str
            Campaign identifier
        pipeline_version : str, optional
            Version of the pipeline
        workbook_name : str, optional
            File name of the pipeline input workbook
        workbook_sha256 : str, optional
            Hex sha256 of the workbook, see modeltestsdk.datafile.sha256_file()
        sdk_version : str, optional
            Version of this SDK; the installed version by default

        Returns
        -------
        ImportRun
            The import run, status 'running'
        """
        body = dict(campaign_id=campaign_id, pipeline_version=pipeline_version,
                    sdk_version=sdk_version or installed_sdk_version(), workbook_name=workbook_name,
                    workbook_sha256=workbook_sha256)
        data = self.client.post("importrun", body={k: v for k, v in body.items() if v is not None})
        return ImportRun(**data)

    def finish(self, run_id: str, status: str, summary: dict = None, failures: list = None,
               raw_file_manifest: list = None) -> ImportRun:
        """
        Finish a running import run with its outcome.

        Parameters
        ----------
        run_id : str
            Import run identifier
        status : {'succeeded', 'failed', 'partial'}
            Outcome of the run
        summary : dict, optional
            Counts, e.g. tests_total, tests_uploaded, tests_unchanged, tests_failed
        failures : list of dict, optional
            Failed tests, e.g. [{"test_number": "3010", "error": "..."}]
        raw_file_manifest : list of dict, optional
            Raw files read, see modeltestsdk.datafile.describe_source_file()

        Returns
        -------
        ImportRun
            The finished import run
        """
        body = dict(status=status, summary=summary, failures=failures, raw_file_manifest=raw_file_manifest)
        data = self.client.patch("importrun", str(run_id),
                                 body=to_jsonable({k: v for k, v in body.items() if v is not None}))
        return ImportRun(**data)

    def get_by_id(self, run_id: str) -> ImportRun:
        """
        Get an import run by id.

        Parameters
        ----------
        run_id : str
            Import run identifier

        Returns
        -------
        ImportRun
            The import run
        """
        return ImportRun(**self.client.get("importrun", str(run_id)))
