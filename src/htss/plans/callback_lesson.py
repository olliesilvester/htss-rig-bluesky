from typing import Any, Callable, Optional
from bluesky.callbacks import CallbackBase
from event_model.documents import RunStart

"""We can create our own callbacks to inspect what has happened in our plans"""

class BasicCallback(CallbackBase):

    def __init__(self,
        *,
        emit: Callable[..., Any] | None = None,):
        super().__init__(emit=emit)

    #After the RunEngine sees 'yield from open_run(md)' , this will be triggered
    def start(self, doc: RunStart) -> Optional[RunStart]:
        print(f"A bluesky run has been started. Document looks like {doc}")
    
    def event(self, doc: RunStart) -> Optional[RunStart]:
        print(f"A bluesky run has been detected. Document looks like {doc}")

    #After the RunEngine sees 'yield from close_run(md)' , this will be triggered
    def stop(self, doc: RunStart) -> Optional[RunStart]:
        print(f"A bluesky stop has been detected. Document looks like {doc}")