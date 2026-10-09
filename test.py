from core import *
from apps.hellobike.config import *
from apps.hellobike.tasks.subtask_flashback import flashback

d = connect_device()
back_to_app(d, PACKAGE_NAME)

