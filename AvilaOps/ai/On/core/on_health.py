from datetime import datetime

from _bootstrap import ensure_on_namespace

ensure_on_namespace()

from on.core.on_storage import update_heartbeat

def heartbeat(agent_name: str):
    update_heartbeat(agent_name, datetime.utcnow().isoformat())
