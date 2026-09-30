from core import *
from apps.hellobike.config import *
from apps.hellobike.tasks.subtask_flashback import flashback

d = connect_device()
flashback(d, ".*同程.*")
flashback(d, ".*飞猪.*")