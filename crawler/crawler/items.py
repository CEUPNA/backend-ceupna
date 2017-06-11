# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TeacherItem(scrapy.Item):
    upna_id = scrapy.Field()
    name = scrapy.Field()
    email = scrapy.Field()
    telephone = scrapy.Field()
    timetable = scrapy.Field()


class SubjectItem(scrapy.Item):
    # Detalles generales de la asignatura
    subject_id = scrapy.Field()
    degree_id = scrapy.Field()
    language = scrapy.Field()
    name = scrapy.Field()
    credits = scrapy.Field()
    year = scrapy.Field()
    semester = scrapy.Field()
    type = scrapy.Field()
    department = scrapy.Field()
    teachers = scrapy.Field()
    # Campos de la ficha
    evaluation = scrapy.Field()
    contents = scrapy.Field()
    curriculum = scrapy.Field()
