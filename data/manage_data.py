class Data():
    def __init__(self):
        self.boards: dict[int, object] = {}
        self.users: dict[str, object] = {}
        self.board_lists: dict[int, list[object]] = {}
        self.items: dict[int, list[object]] = {}

    def get_board_items(self):
        return [
            "Item 1",
            "Item 2",
            "Item 3",
            "Item 4",
            "Item 5",
            "Item 6",
            "Item 7",
            "Item 8",
        ]