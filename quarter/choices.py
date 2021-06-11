
from django.db import models

NEW = 1
WAITING_FOR_PRICING = 2
PRICE_REVIEW = 3
UNDER_NEGOTIAITON = 4
WAITING_FOR_FIRST_TRANSFER = 5
TRANSFER_REVIEW = 6
WAITING_FOR_DESIGNS = 7
DESIGN_REVIEW = 8
FIRST_EXCUTION = 9
SECOND_TRANSFER = 10
SECOND_TRANSFER_REVIEW = 11
SECOND_EXCUTION = 12
DONE = 13

STATUS_CHOICES = (
    (1, "جديد"),
    (2, "قيد التسعير"),
    (3, "مراجعة التسعير"),
    (4, "التفاوض"),
    (5, "انتظار التحويل المالي الأول"),
    (6, "مراجعة التحويل المالي"),
    (7, "التصميم"),
    (8, "مراجعة التصاميم "),
    (9, " التنفيذ الأول"),
    (10, "التحويل الثاني "),
    (11, "مراجعة التحويل الثاني "),
    (12, "التنفيذ الثاني "),
    (13, "انتهاء التنفيذ"),
    (15, "تمت "),
    (14, "المشتريات")
)
