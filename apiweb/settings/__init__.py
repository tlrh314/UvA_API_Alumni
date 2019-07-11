from .base import *
# Attempt to add local settings
try:
    from .local import *
except ImportError:
    raise

# Add any base settings that should come after local, but
try:
    from .extra import *
except ImportError:
    pass
