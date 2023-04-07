#!/usr/bin/python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Dict, List, Set

from scripts.classes import Class, Teacher, Room, Subject, Lesson, EventGroup, Resource


@dataclass
class Timetable:
    lessons_per_day_ind: Dict[tuple, Lesson]
    class_per_id: Dict[str, Class]
    teacher_per_id: Dict[str, Teacher]
    subject_per_id: Dict[str, Subject]
    room_per_id: Dict[str, Room]
    event_groups: Set[EventGroup]

    def get_not_scheduled_event_groups(self) -> List[EventGroup]:
        return [event_group for event_group in self.event_groups if not event_group.is_scheduled()]

    def add_event_group(self, event_group: EventGroup):
        self.event_groups.add(event_group)

    def get_nb_lessons_total(self) -> int:
        return len(self.lessons_per_day_ind)

    def get_not_scheduled_lessons(self, resource: Resource) -> List[Lesson]:
        return [lesson for lesson in self.lessons_per_day_ind.values() if
                lesson not in resource.blocked_lessons and lesson not in resource.scheduled_event_group_per_lesson]
