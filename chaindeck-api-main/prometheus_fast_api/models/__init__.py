from prometheus_fast_api.models import ResetPassword, User,Node
from prometheus_fast_api.models.common import get_db,SessionLocal,Base,engine
Base.metadata.create_all(engine)