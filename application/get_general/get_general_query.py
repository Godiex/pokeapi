from typing import Optional


class GetGeneralQuery:
    data_to_search: str

    def __init__(self, data_to_search: Optional[str] = None):
        if data_to_search:
            self.data_to_search = data_to_search.lower()
        else:
            self.data_to_search = None
