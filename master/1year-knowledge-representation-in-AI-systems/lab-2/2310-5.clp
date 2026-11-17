(deftemplate student
  (slot name
    (type SYMBOL))
  (slot age
    (type INTEGER)
    (range 17 22))
  (slot year
    (type INTEGER)
    (range 2 5))
  (slot spec
    (type STRING)
    (allowed-values "hard" "soft" "ai"))
  (slot aver_mark
    (type FLOAT)
    (range 3.0 5.0)))


(deffacts students
  (student (name Ivan)    (age 22) (year 5) (spec "hard") (aver_mark 4.5))
  (student (name Anna)    (age 21) (year 5) (spec "hard") (aver_mark 4.8))
  (student (name Petr)    (age 19) (year 5) (spec "hard") (aver_mark 3.5))
  (student (name Maria)   (age 20) (year 5) (spec "hard") (aver_mark 4.0))
  (student (name Oleg)    (age 22) (year 5) (spec "soft") (aver_mark 4.2))
  (student (name Elena)   (age 21) (year 4) (spec "hard") (aver_mark 4.7))
  (student (name Dmitry)  (age 20) (year 3) (spec "ai")   (aver_mark 5.0))
  (student (name Olga)    (age 18) (year 2) (spec "soft") (aver_mark 3.0))
  (student (name Sergey)  (age 17) (year 2) (spec "ai")   (aver_mark 3.8))
  (student (name Natalia) (age 21) (year 4) (spec "soft") (aver_mark 4.5))
)
