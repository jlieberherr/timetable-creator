#!/usr/bin/python
# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Set, Dict


@dataclass(eq=True, frozen=True)
class Lesson:
    day: int
    index: int


@dataclass(eq=True, frozen=True)
class Teacher:
    id: str
    blocked_lessons: Set[Lesson] = field(default_factory=set, compare=False, hash=False, repr=False)


@dataclass(eq=True, frozen=True)
class Class:
    id: str
    blocked_lessons: Set[Lesson] = field(default_factory=set, compare=False, hash=False, repr=False)


@dataclass(eq=True, frozen=True)
class Room:
    id: str
    blocked_lessons: Set[Lesson] = field(default_factory=set, compare=False, hash=False, repr=False)


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
    allowed_partitions: Set[AllowedPartition] = field(compare=False, hash=False, repr=False)
    involved_teachers: Set[Teacher] = field(default_factory=set, compare=False, hash=False)
    involved_classes: Set[Class] = field(default_factory=set, compare=False, hash=False)
    allowed_rooms: Set[Room] = field(default_factory=set, compare=False, hash=False)
    blocked_lessons: Set[Lesson] = field(default_factory=set, compare=False, hash=False, repr=False)
    fixed: bool = field(default=False, compare=False, hash=False)

    def __post_init__(self):
        if not check_allowed_partitions(self.allowed_partitions):
            raise ValueError(
                "Allowed partitions must have the same number of lessons: {}".format(self.allowed_partitions))
