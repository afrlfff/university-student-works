(defrule find-fifth-year-hard-students
  (student
    (name ?name)
    (age ?age&:(integerp ?age))
    (year ?year&5&:(integerp ?year))
    (spec ?spec&"hard"&:(stringp ?spec)))
  (test (> ?age 19))
  =>
  (printout t "Студент " ?name " учится на 5-м курсе, возраст " ?age crlf)
)
