(defrule find-fifth-year-hard-students
  (student
    (name ?name)
    (year ?year&5&:(integerp ?year))
    (age ?age&:(integerp ?age)&=(- 22 (- 5 ?year)))
    (spec ?spec&"hard"&:(stringp ?spec)))
  (test (> ?age 19))
  =>
  (printout t "Студент " ?name " учится на 5-м курсе, возраст " ?age crlf)
)
