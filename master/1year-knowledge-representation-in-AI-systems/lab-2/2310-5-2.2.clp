(defrule find-fifth-year-hard-students
  (student (name ?name) (age ?age) (year 5) (spec "hard"))
  (test (> ?age 19))
  =>
  (printout t "Студент " ?name " учится на 5-м курсе, возраст " ?age crlf)
)
