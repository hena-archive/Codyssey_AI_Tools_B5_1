class Entry:
    def __init__(self, key, value, expire_at = None, node = None):
        self.key = key
        self.value = value

        # TTL이 없으면 None
        self.expire_at = expire_at

        # LRU 리스트에서 자신의 Node
        self.recent_node = node

        self.byte_size = len(key) + len(value)
