__all__ = ["Set", "Map"]
from typing import Any, NamedTuple

class MapSlot(NamedTuple):
    key: Any
    value: Any

class MapBucket:
    def __init__(self, slot_count=10):
        self.count = 0
        self.slot_count = slot_count
        self.slots: list[MapSlot] = [MapSlot(None, None)] * slot_count

    def __repr__(self):
        return "{" + ", ".join(f"{repr(slot.key)}: {slot.value}" for slot in self) + "}"

    def __iter__(self):
        for i in range(self.count):
            yield self[i]

    def __getitem__(self, i):
        return self.slots[i]

    def __setitem__(self, i, value):
        self.slots[i] = value

    def index(self, key) -> int:
        for i in range(self.count):
            if self[i].key == key:
                return i
        return -1

    def has(self, key) -> bool:
        return self.index(key) != -1

    def set(self, key, value) -> bool:
        i = self.index(key)
        if i != -1:
            self[i] = MapSlot(key, value)
            return True
        if self.count >= self.slot_count: return False
        self[self.count] = MapSlot(key, value)
        self.count += 1
        return True

    def remove(self, key):
        i = self.index(key)
        if i == -1: return
        self[i] = self[self.count - 1]
        self[self.count - 1] = MapSlot(None, None)
        self.count -= 1

class BaseMap:
    def __init__(self, bucket_count=10, slots_per_bucket=4):
        self.bucket_count = bucket_count
        self.slots_per_bucket = slots_per_bucket
        self.buckets: list[MapBucket] = [MapBucket(slot_count=slots_per_bucket) for i in range(bucket_count)]

    def _slow_set(self, key, value):
        new_bucket_count = self.bucket_count * 2
        while True:
            new_bucket_count += 1
            new_map = Map(bucket_count=new_bucket_count, slots_per_bucket=self.slots_per_bucket)
            if not new_map._fast_set(key, value):
                continue
            for k, v in self:
                if not new_map._fast_set(k, v):
                    break
            else:
                break
            continue
        self.bucket_count = new_bucket_count
        self.buckets = new_map.buckets

    def _fast_set(self, key, value) -> bool:
        # https://en.wikipedia.org/wiki/List_of_hash_functions#Non-cryptographic_hash_functions
        return self.buckets[hash(key) % self.bucket_count].set(key, value)

    def remove(self, key):
        self.buckets[hash(key) % self.bucket_count].remove(key)

    def has(self, key) -> bool:
        return self.buckets[hash(key) % self.bucket_count].index(key) != -1

    def __iter__(self):
        for bucket in self.buckets:
            for slot in bucket:
                yield slot.key, slot.value

class Map(BaseMap):
    def __getitem__(self, key):
        bucket = self.buckets[hash(key) % self.bucket_count]
        i = bucket.index(key)
        return bucket[i].value

    def __setitem__(self, key, value):
        if not self._fast_set(key, value):
            self._slow_set(key, value)

    def __repr__(self):
        return "{" + ", ".join(f"{repr(key)}: {value}" for key, value in self) + "}"

class Set(BaseMap):
    def __getitem__(self, key):
        return self.has(key)

    def add(self, key):
        if not self._fast_set(key, None):
            self._slow_set(key, None)

    def __repr__(self):
        return "{" + ", ".join(repr(key) for key, value in self) + "}"
