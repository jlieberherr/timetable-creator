#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest

from scripts.classes import Lesson, Teacher, AllowedPartition, check_allowed_partitions, Event, Subject, Class


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
    assert not check_allowed_partitions([allowed_partition_1, allowed_partition_2])
    allowed_partition_3 = AllowedPartition({2: 2})
    assert check_allowed_partitions([allowed_partition_1, allowed_partition_3])
    allowed_partition_4 = AllowedPartition({1: 2, 2: 1})
    assert {allowed_partition_1} == {allowed_partition_1, allowed_partition_4}
    assert not {allowed_partition_1} == {allowed_partition_2, allowed_partition_4}


def test_event_class():
    subject = Subject("M")
    partition_1 = AllowedPartition({1: 2, 2: 1})
    partition_2 = AllowedPartition({3: 1})
    partition_3 = AllowedPartition({2: 2})
    allowed_partitions_1 = {partition_1, partition_2}
    allowed_partitions_2 = {partition_1, partition_3}
    subject = Subject("M")
    with pytest.raises(ValueError):
        Event(1, subject, allowed_partitions_1)
    event_1 = Event(2, subject, allowed_partitions_2, involved_teachers={Teacher("t1")}, involved_classes={Class("c1")})
    assert event_1.id == 2
    assert event_1.subject == subject
    assert event_1.allowed_partitions == allowed_partitions_2
    assert event_1.involved_teachers == {Teacher("t1")}
    assert event_1.involved_classes == {Class("c1")}
    assert event_1.allowed_rooms == set()
