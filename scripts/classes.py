#!/usr/bin/python
# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Set, Dict


@dataclass(eq=True, frozen=True)
class Lesson:
    day: int
    index: int


@dataclass(eq=True, frozen=True)
class Resource:
    id: str
    blocked_lessons: Set[Lesson] = field(default_factory=set, compare=False, hash=False, repr=False)
    scheduled_event_group_per_lesson: Dict = field(default_factory=dict, compare=False,
                                                   hash=False, repr=False)

    def get_not_schedulable_lessons(self) -> Set[Lesson]:
        return self.blocked_lessons.union(self.scheduled_event_group_per_lesson.keys())


class Teacher(Resource):
    pass


@dataclass(eq=True, frozen=True)
class Class(Resource):
    pass


@dataclass(eq=True, frozen=True)
class Room(Resource):
    pass


@dataclass(eq=True, frozen=True)
class Subject:
    id: str


@dataclass
class AllowedPartition:
    nb_per_block: Dict[int, int]

    def __eq__(self, other):
        return self.nb_per_block == other.nb_per_block

    def __hash__(self):
        return hash(tuple(sorted(self.nb_per_block.items())))

    def get_nb_lessons(self) -> int:
        return sum([k * v for k, v in self.nb_per_block.items()])


def check_allowed_partitions(allowed_partitions: Set[AllowedPartition]) -> bool:
    return len({allowed_partition.get_nb_lessons() for allowed_partition in allowed_partitions}) == 1


@dataclass(eq=True, frozen=True)
class Event:
    id: int
    subject: Subject = field(compare=False, hash=False)
    involved_teachers: Set[Teacher] = field(default_factory=set, compare=False, hash=False)
    involved_classes: Set[Class] = field(default_factory=set, compare=False, hash=False)
    allowed_rooms: Set[Room] = field(default_factory=set, compare=False, hash=False)

    def get_not_schedulable_lessons(self) -> Set[Lesson]:
        res = set.union(
            *[t.blocked_lessons for t in self.involved_teachers] + [c.blocked_lessons for c in self.involved_classes])
        lessons_with_no_free_room = set.intersection(*[r.get_not_schedulable_lessons() for r in self.allowed_rooms])
        return res.union(lessons_with_no_free_room)


@dataclass(eq=True, frozen=True)
class EventGroup:
    id: int
    events: Set[Event] = field(default_factory=set, compare=False, hash=False, repr=False)
    allowed_partitions: Set[AllowedPartition] = field(default_factory=set, compare=False, hash=False, repr=False)
    scheduled_lessons: Set[Lesson] = field(default_factory=set, compare=False, hash=False, repr=False)
    fixed: bool = field(default=False, compare=False, hash=False)

    def __post_init__(self):
        if not check_allowed_partitions(self.allowed_partitions):
            raise ValueError(
                "Allowed partitions must have the same number of lessons: {}".format(self.allowed_partitions))

    def get_involved_teachers(self) -> Set[Teacher]:
        return {teacher for event in self.events for teacher in event.involved_teachers}

    def get_involved_classes(self) -> Set[Class]:
        return {class_ for event in self.events for class_ in event.involved_classes}

    def get_nb_lessons(self) -> int:
        #
        return next(iter(self.allowed_partitions)).get_nb_lessons()

    def is_scheduled(self) -> bool:
        return len(self.scheduled_lessons) == self.get_nb_lessons()

    def get_not_schedulable_lessons(self) -> Set[Lesson]:
        return set.union(*[event.get_not_schedulable_lessons() for event in self.events])
