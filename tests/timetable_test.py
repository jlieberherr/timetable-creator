#!/usr/bin/python
# -*- coding: utf-8 -*-
from scripts.classes import Lesson, Class, Subject, Event, Teacher, Room, EventGroup, AllowedPartition
from scripts.timetable import Timetable


def test_timetable_class():
    lessons_per_day_ind = {(i, j): Lesson(i, j) for i in range(1, 4) for j in range(1, 6)}
    class_per_id = {"C1": Class("C1"), "C2": Class("C2"), "C3": Class("C3")}
    teacher_per_id = {
        "MW": Teacher("WM"),
        "JL": Teacher("JL"),
        "BG": Teacher("BG"),
        "GR": Teacher("GR"),
        "HM": Teacher("HM"),
        "PW": Teacher("PW"),
        "SG": Teacher("SG"),
        "RS": Teacher("RS"),
    }
    subject_per_id = {
        "B": Subject("B"),
        "M": Subject("M"),
        "C": Subject("C"),
        "D": Subject("D"),
        "P": Subject("P"),
        "KL": Subject("KL"),
    }
    room_per_id = {
        "R_B": Room("R_B"),
        "R_C": Room("R_C"),
        "R_P": Room("R_P"),
        "R_n_1": Room("R_n_1"),
        "R_n_2": Room("R_n_2"),
        "R_n_3": Room("R_n_3"),
    }

    partition_1_1 = AllowedPartition({1: 1})
    partition_2_1 = AllowedPartition({2: 1})
    partition_2_2 = AllowedPartition({2: 2})
    partition_1_2_2_1 = AllowedPartition({1: 2, 2: 1})
    partition_3_1 = AllowedPartition({3: 1})

    timetable = Timetable(lessons_per_day_ind, class_per_id, teacher_per_id, subject_per_id, room_per_id, set())

    assert timetable.get_nb_lessons_total() == 15

    # B and C
    event_c1_b = Event(1, subject_per_id["B"], {teacher_per_id["MW"]}, {class_per_id["C1"]}, {room_per_id["R_B"]})
    event_c1_c = Event(2, subject_per_id["C"], {teacher_per_id["BG"]}, {class_per_id["C1"]}, {room_per_id["R_C"]})
    timetable.add_event_group(EventGroup(1, {event_c1_b, event_c1_c}, {partition_2_1}))

    event_c2_b = Event(3, subject_per_id["B"], {teacher_per_id["MW"]}, {class_per_id["C2"]}, {room_per_id["R_B"]})
    event_c2_c = Event(4, subject_per_id["C"], {teacher_per_id["PW"]}, {class_per_id["C2"]}, )
    timetable.add_event_group(EventGroup(2, {event_c2_b, event_c2_c}, {partition_2_1}))

    event_c3_b = Event(5, subject_per_id["B"], {teacher_per_id["MW"]}, {class_per_id["C3"]}, {room_per_id["R_B"]})
    event_c3_c = Event(6, subject_per_id["C"], {teacher_per_id["PW"]}, {class_per_id["C3"]}, {room_per_id["R_C"]})
    timetable.add_event_group(EventGroup(3, {event_c3_b, event_c3_c}, {partition_2_1}))

    # M
    event_c1c2_m = Event(7, subject_per_id["M"], {teacher_per_id["JL"]}, {class_per_id["C1"], class_per_id["C3"]},
                         {room_per_id["R_n_1"], room_per_id["R_n_2"], room_per_id["R_n_3"]})
    timetable.add_event_group(EventGroup(4, {event_c1c2_m}, {partition_2_2, partition_1_2_2_1}))

    event_c2_m = Event(8, subject_per_id["M"], {teacher_per_id["HM"]}, {class_per_id["C2"]},
                       {room_per_id["R_n_1"], room_per_id["R_n_2"], room_per_id["R_n_3"]})
    timetable.add_event_group(EventGroup(5, {event_c2_m}, {partition_2_2}))

    # D
    event_c1c2_d = Event(10, subject_per_id["D"], {teacher_per_id["GR"]}, {class_per_id["C1"], class_per_id["C2"]},
                         {room_per_id["R_n_1"], room_per_id["R_n_2"], room_per_id["R_n_3"]})
    timetable.add_event_group(EventGroup(6, {event_c1c2_d}, {partition_3_1}))

    event_c3_d = Event(11, subject_per_id["D"], {teacher_per_id["SG"]}, {class_per_id["C3"]},
                       {room_per_id["R_n_1"], room_per_id["R_n_2"], room_per_id["R_n_3"]})
    timetable.add_event_group(EventGroup(7, {event_c3_d}, {partition_3_1}))

    # P
    event_c1_p = Event(12, subject_per_id["P"], {teacher_per_id["RS"]}, {class_per_id["C1"]}, {room_per_id["R_P"]})
    timetable.add_event_group(EventGroup(8, {event_c1_p}, {partition_2_1}))

    event_c2_p = Event(13, subject_per_id["P"], {teacher_per_id["RS"]}, {class_per_id["C2"]}, {room_per_id["R_P"]})
    timetable.add_event_group(EventGroup(9, {event_c2_p}, {partition_2_1}))

    event_c3_p = Event(14, subject_per_id["P"], {teacher_per_id["RS"]}, {class_per_id["C3"]}, {room_per_id["R_P"]})
    timetable.add_event_group(EventGroup(10, {event_c3_p}, {partition_2_1}))

    # KL
    event_c1_kl = Event(15, subject_per_id["KL"], {teacher_per_id["GR"]}, {class_per_id["C1"]},
                        {room_per_id["R_n_1"], room_per_id["R_n_2"], room_per_id["R_n_3"]})
    timetable.add_event_group(EventGroup(11, {event_c1_kl}, {partition_1_1}))

    event_c2_kl = Event(16, subject_per_id["KL"], {teacher_per_id["MW"]}, {class_per_id["C2"]},
                        {room_per_id["R_n_1"], room_per_id["R_n_2"], room_per_id["R_n_3"]})
    timetable.add_event_group(EventGroup(12, {event_c2_kl}, {partition_1_1}))

    event_c3_kl = Event(17, subject_per_id["KL"], {teacher_per_id["SG"]}, {class_per_id["C3"]},
                        {room_per_id["R_n_1"], room_per_id["R_n_2"], room_per_id["R_n_3"]})
    timetable.add_event_group(EventGroup(13, {event_c3_kl}, {partition_1_1}))

    assert len(timetable.event_groups) == 13

    assert len(timetable.get_not_scheduled_event_groups()) == 13

    assert len(timetable.get_not_scheduled_lessons(timetable.teacher_per_id["JL"])) == 15

    t_jl = timetable.teacher_per_id["JL"]
    t_jl.blocked_lessons.add(timetable.lessons_per_day_ind[(2, 3)])
    t_jl.blocked_lessons.add(timetable.lessons_per_day_ind[(2, 4)])
    assert len(timetable.get_not_scheduled_lessons(timetable.teacher_per_id["JL"])) == 13
