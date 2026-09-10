class Node:
    # 생성자
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def get_next(self):
        return self.next

    def get_prev(self):
        return self.prev