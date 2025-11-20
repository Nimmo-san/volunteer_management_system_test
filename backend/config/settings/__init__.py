# from .base import *  # noqa: F403
import os


MODULE = os.environ.get("DJANGO_SETTINGS_MODULE", "").split(".")[2]
if  MODULE == "prod":
    from .prod import *  # noqa: F403
else:
    from .dev import *  # noqa: F403
