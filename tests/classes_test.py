#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from scripts.classes import Lesson, Teacher, AllowedPartition, check_allowed_partitions, Event, Subject, Class, \
    EventGroup, Resource, Room

DEFAULT_ALLOWED_PARTITION = AllowedPartition({2: 1})
DEFAULT_ALLOWED_PARTITION_SET = {DEFAULT_ALLOWED_PARTITION}

DEFAULT_EVENT = Event(1, Subject("S"))
DEFAULT_EVENT_GROUP = EventGroup(1, {DEFAULT_EVENT}, DEFAULT_ALLOWED_PARTITION_SET)


def test_resources_class():
    resource = Resource("r")
    resource.blocked_lessons.update({Lesson(1, 2), Lesson(1, 3)})
    assert resource.get_not_schedulable_lessons() == {Lesson(1, 2), Lesson(1, 3)}
    resource.scheduled_event_group_per_lesson.update({Lesson(1, 1): DEFAULT_EVENT_GROUP})
    resource.scheduled_event_group_per_lesson.update({Lesson(1, 2): DEFAULT_EVENT_GROUP})
    assert resource.get_not_schedulable_lessons() == {Lesson(1, 2), Lesson(1, 3), Lesson(1, 1)}


def test_lesson_class():
    lesson_1 = Lesson(3, 5)
    assert lesson_1.day == 3
    assert lesson_1.index == 5
    lesson_2 = Lesson(3, 5)
    assert lesson_1 == lesson_2
    lesson_3 = Lesson(3, 6)
    assert lesson_1 != lesson_3


def test_teacher_class():
    lesson_1 = Lesson(3, 5)
    lesson_2 = Lesson(3, 6)
    lesson_3 = Lesson(4, 1)
    teacher_1 = Teacher("t1", {lesson_1, lesson_2, lesson_3})
    assert teacher_1.id == "t1"
    assert teacher_1.blocked_lessons == {lesson_1, lesson_2, lesson_3}
    assert teacher_1.blocked_lessons != {lesson_1, lesson_2}
    teacher_2 = Teacher("t1", {lesson_1, lesson_2})
    assert teacher_1 == teacher_2
    teacher_3 = Teacher("t3", {lesson_1, lesson_2})
    assert teacher_2 != teacher_3
    teacher_1.blocked_lessons.add(lesson_3)
    assert teacher_1.blocked_lessons == {lesson_1, lesson_2, lesson_3}
    lesson_4 = Lesson(5, 2)
    teacher_1.blocked_lessons.add(lesson_4)
    assert teacher_1.blocked_lessons == {lesson_1, lesson_2, lesson_3, lesson_4}

    teacher_5 = Teacher("t5")
    assert teacher_5.blocked_lessons == set()


def test_allowed_partition_class():
    allowed_partition_1 = AllowedPartition({1: 2, 2: 1})
    assert allowed_partition_1.nb_per_block == {1: 2, 2: 1}
    assert allowed_partition_1.get_nb_lessons() == 4
    allowed_partition_2 = AllowedPartition({3: 1})
    assert allowed_partition_2.nb_per_block == {3: 1}
    assert allowed_partition_2.get_nb_lessons() == 3
    assert not check_allowed_partitions({allowed_partition_1, allowed_partition_2})
    allowed_partition_3 = AllowedPartition({2: 2})
    assert check_allowed_partitions({allowed_partition_1, allowed_partition_3})
    allowed_partition_4 = AllowedPartition({1: 2, 2: 1})
    assert {allowed_partition_1} == {allowed_partition_1, allowed_partition_4}
    assert not {allowed_partition_1} == {allowed_partition_2, allowed_partition_4}


def test_event_class():
    event = Event(1, Subject("M"))
    assert event.id == 1
    assert event.subject == Subject("M")


def test_event_get_not_schedulable_lessons():
    t1 = Teacher("t1", blocked_lessons={Lesson(1, 2), Lesson(1, 3)})
    t2 = Teacher("t2", blocked_lessons={Lesson(1, 3), Lesson(1, 4)})
    c1 = Class("c1", blocked_lessons={Lesson(1, 4), Lesson(1, 5)})
    c2 = Class("c2", blocked_lessons={Lesson(2, 1)})
    r1 = Room("r1", blocked_lessons={Lesson(1, 2), Lesson(3, 1)})
    r2 = Room("r2", blocked_lessons={Lesson(3, 1), Lesson(3, 2)})
    event = Event(1, Subject("M"), involved_teachers={t1, t2}, involved_classes={c1, c2}, allowed_rooms={r1, r2})
    assert event.get_not_schedulable_lessons() == {Lesson(1, 2), Lesson(1, 3), Lesson(1, 4), Lesson(1, 5), Lesson(2, 1),
                                                   Lesson(3, 1)}


def test_event_group_not_schedulable_lessons():
    t1 = Teacher("t1", blocked_lessons={Lesson(1, 2), Lesson(1, 3)})
    t2 = Teacher("t2", blocked_lessons={Lesson(1, 3), Lesson(1, 4)})
    c1 = Class("c1", blocked_lessons={Lesson(1, 4), Lesson(1, 5)})
    c2 = Class("c2", blocked_lessons={Lesson(2, 1)})
    r1 = Room("r1", blocked_lessons={Lesson(1, 2), Lesson(3, 1)})
    r2 = Room("r2", blocked_lessons={Lesson(3, 1), Lesson(3, 2)})
    event_1 = Event(1, Subject("M"), involved_teachers={t1}, involved_classes={c1}, allowed_rooms={r1})
    event_2 = Event(2, Subject("F"), involved_teachers={t2}, involved_classes={c2}, allowed_rooms={r2})
    event_group = EventGroup(1, {event_1, event_2}, DEFAULT_ALLOWED_PARTITION_SET)
    assert event_group.get_not_schedulable_lessons() == {Lesson(1, 2), Lesson(1, 3), Lesson(1, 4), Lesson(1, 5),
                                                         Lesson(2, 1), Lesson(3, 1), Lesson(3, 2)}


def test_event_group_class():
    event_1 = Event(1, Subject("M"), involved_teachers={Teacher("tM")}, involved_classes={Class("c1")})
    event_2 = Event(2, Subject("F"), involved_teachers={Teacher("tF")}, involved_classes={Class("c1")})
    partition_1 = AllowedPartition({1: 2, 2: 1})
    partition_2 = AllowedPartition({3: 1})
    partition_3 = AllowedPartition({2: 2})
    allowed_partitions_1 = {partition_1, partition_2}
    allowed_partitions_2 = {partition_1, partition_3}
    with pytest.raises(ValueError):
        EventGroup(1, {event_1, event_2}, allowed_partitions_1)
    event_group_1 = EventGroup(2, {event_1, event_2}, allowed_partitions_2)
    assert event_group_1.id == 2
    assert event_group_1.allowed_partitions == allowed_partitions_2
    assert event_group_1.get_involved_teachers() == {Teacher("tM"), Teacher("tF")}
    assert event_group_1.get_involved_classes() == {Class("c1")}
    assert event_group_1.get_nb_lessons() == 4
    assert not event_group_1.is_scheduled()
    event_group_1.scheduled_lessons.add(Lesson(1, 2))
    event_group_1.scheduled_lessons.add(Lesson(1, 3))
    assert not event_group_1.is_scheduled()
    event_group_1.scheduled_lessons.add(Lesson(2, 2))
    event_group_1.scheduled_lessons.add(Lesson(2, 3))
    assert event_group_1.is_scheduled()
