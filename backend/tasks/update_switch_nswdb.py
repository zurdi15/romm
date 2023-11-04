import os
from pathlib import Path

from typing import Final
from config import (
    ENABLE_SCHEDULED_UPDATE_SWITCH_TITLEDB,
    SCHEDULED_UPDATE_SWITCH_TITLEDB_CRON,
)
from .utils import RemoteFilePullTask

FIXTURE_FILE_PATH: Final = (
    Path(os.path.dirname(__file__)).parent
    / "handler"
    / "fixtures"
    / "switch_nswdb.json"
)


class UpdateSwitchNswDBTask(RemoteFilePullTask):
    def __init__(self):
        super().__init__(
            func="tasks.update_switch_nswdb.update_switch_nswdb_task.run",
            description="switch nswdb update",
            enabled=ENABLE_SCHEDULED_UPDATE_SWITCH_TITLEDB,
            cron_string=SCHEDULED_UPDATE_SWITCH_TITLEDB_CRON,
            url="https://raw.githubusercontent.com/blawar/nswdb/master/US.en.json",
            file_path=FIXTURE_FILE_PATH,
        )


update_switch_nswdb_task = UpdateSwitchNswDBTask()
