(defrule start_system
 (initial-fact)
 =>
 (printout t crlf "Culinary Dish Advisor" crlf)
 (printout t "Questions depend on your previous answers." crlf)
 (assert (need hunger))
)

(defrule ask_hunger
 ?n <- (need hunger)
 =>
 (retract ?n)
 (printout t crlf "Are you hungry? (yes / no): ")
 (bind ?v (read t))
 (while (and (neq ?v yes) (neq ?v no)) do
  (printout t "Invalid. Enter yes or no." crlf)
  (printout t "Are you hungry? (yes / no): ")
  (bind ?v (read t)))
 (assert (hunger ?v))
)

(defrule stop_not_hungry
 (hunger no)
 =>
 (printout t crlf "You are not hungry. No cooking needed now." crlf)
 (assert (done))
)

(defrule ask_meal_type
 (hunger yes)
 (not (meal_type ?x))
 (not (done))
 =>
 (printout t crlf "Sweet or savory dish? (sweet / savory): ")
 (bind ?v (read t))
 (while (and (neq ?v sweet) (neq ?v savory)) do
  (printout t "Invalid. Enter sweet or savory." crlf)
  (printout t "Sweet or savory dish? (sweet / savory): ")
  (bind ?v (read t)))
 (assert (meal_type ?v))
)

(defrule ask_cuisine
 (hunger yes)
 (meal_type ?mt)
 (not (cuisine ?x))
 (not (done))
 =>
 (printout t crlf "Preferred cuisine?" crlf)
 (printout t "(russian / italian / japanese / georgian / any): ")
 (bind ?v (read t))
 (while (and (neq ?v russian) (neq ?v italian) (neq ?v japanese)
             (neq ?v georgian) (neq ?v any)) do
  (printout t "Invalid cuisine." crlf)
  (printout t "(russian / italian / japanese / georgian / any): ")
  (bind ?v (read t)))
 (assert (cuisine ?v))
)

(defrule ask_meal_size_italian
 (hunger yes)
 (cuisine italian)
 (not (meal_size ?x))
 (not (done))
 =>
 (printout t crlf "How filling? (light / hearty): ")
 (bind ?v (read t))
 (while (and (neq ?v light) (neq ?v hearty)) do
  (printout t "Invalid. Enter light or hearty." crlf)
  (printout t "How filling? (light / hearty): ")
  (bind ?v (read t)))
 (assert (meal_size ?v))
)

(defrule ask_meal_size_georgian
 (hunger yes)
 (cuisine georgian)
 (not (meal_size ?x))
 (not (done))
 =>
 (printout t crlf "How filling? (light / hearty): ")
 (bind ?v (read t))
 (while (and (neq ?v light) (neq ?v hearty)) do
  (printout t "Invalid. Enter light or hearty." crlf)
  (printout t "How filling? (light / hearty): ")
  (bind ?v (read t)))
 (assert (meal_size ?v))
)

(defrule ask_meal_size_any
 (hunger yes)
 (cuisine any)
 (not (meal_size ?x))
 (not (done))
 =>
 (printout t crlf "How filling? (light / hearty): ")
 (bind ?v (read t))
 (while (and (neq ?v light) (neq ?v hearty)) do
  (printout t "Invalid. Enter light or hearty." crlf)
  (printout t "How filling? (light / hearty): ")
  (bind ?v (read t)))
 (assert (meal_size ?v))
)

(defrule ask_meal_size_russian_savory
 (hunger yes)
 (cuisine russian)
 (meal_type savory)
 (not (meal_size ?x))
 (not (done))
 =>
 (printout t crlf "How filling? (light / hearty): ")
 (bind ?v (read t))
 (while (and (neq ?v light) (neq ?v hearty)) do
  (printout t "Invalid. Enter light or hearty." crlf)
  (printout t "How filling? (light / hearty): ")
  (bind ?v (read t)))
 (assert (meal_size ?v))
)

(defrule ask_meal_size_japanese_savory
 (hunger yes)
 (cuisine japanese)
 (meal_type savory)
 (not (meal_size ?x))
 (not (done))
 =>
 (printout t crlf "How filling? (light / hearty): ")
 (bind ?v (read t))
 (while (and (neq ?v light) (neq ?v hearty)) do
  (printout t "Invalid. Enter light or hearty." crlf)
  (printout t "How filling? (light / hearty): ")
  (bind ?v (read t)))
 (assert (meal_size ?v))
)

(defrule ask_available_time_italian
 (hunger yes)
 (cuisine italian)
 (meal_size ?ms)
 (not (available_time ?x))
 (not (done))
 =>
 (printout t crlf "Available time? (short / medium / long): ")
 (bind ?v (read t))
 (while (and (neq ?v short) (neq ?v medium) (neq ?v long)) do
  (printout t "Invalid. Enter short, medium or long." crlf)
  (printout t "Available time? (short / medium / long): ")
  (bind ?v (read t)))
 (assert (available_time ?v))
)

(defrule ask_available_time_russian_sweet
 (hunger yes)
 (cuisine russian)
 (meal_type sweet)
 (not (available_time ?x))
 (not (done))
 =>
 (printout t crlf "Available time? (short / medium / long): ")
 (bind ?v (read t))
 (while (and (neq ?v short) (neq ?v medium) (neq ?v long)) do
  (printout t "Invalid. Enter short, medium or long." crlf)
  (printout t "Available time? (short / medium / long): ")
  (bind ?v (read t)))
 (assert (available_time ?v))
)

(defrule ask_available_time_japanese_sweet
 (hunger yes)
 (cuisine japanese)
 (meal_type sweet)
 (not (available_time ?x))
 (not (done))
 =>
 (printout t crlf "Available time? (short / medium / long): ")
 (bind ?v (read t))
 (while (and (neq ?v short) (neq ?v medium) (neq ?v long)) do
  (printout t "Invalid. Enter short, medium or long." crlf)
  (printout t "Available time? (short / medium / long): ")
  (bind ?v (read t)))
 (assert (available_time ?v))
)

(defrule ask_available_time_japanese_hearty
 (hunger yes)
 (cuisine japanese)
 (meal_type savory)
 (meal_size hearty)
 (not (available_time ?x))
 (not (done))
 =>
 (printout t crlf "Available time? (short / medium / long): ")
 (bind ?v (read t))
 (while (and (neq ?v short) (neq ?v medium) (neq ?v long)) do
  (printout t "Invalid. Enter short, medium or long." crlf)
  (printout t "Available time? (short / medium / long): ")
  (bind ?v (read t)))
 (assert (available_time ?v))
)

(defrule ask_cooking_skill_italian
 (hunger yes)
 (cuisine italian)
 (available_time ?tm)
 (not (cooking_skill ?x))
 (not (done))
 =>
 (printout t crlf "Cooking skill? (beginner / intermediate / advanced): ")
 (bind ?v (read t))
 (while (and (neq ?v beginner) (neq ?v intermediate) (neq ?v advanced)) do
  (printout t "Invalid. Enter beginner, intermediate or advanced." crlf)
  (printout t "Cooking skill? (beginner / intermediate / advanced): ")
  (bind ?v (read t)))
 (assert (cooking_skill ?v))
)

(defrule complexity_beginner_short
 (cuisine italian)
 (cooking_skill beginner) (available_time short) (not (cooking_complexity ?x))
 =>
 (assert (cooking_complexity simple))
 (printout t crlf "Derived cooking_complexity: simple" crlf))

(defrule complexity_beginner_medium
 (cuisine italian)
 (cooking_skill beginner) (available_time medium) (not (cooking_complexity ?x))
 =>
 (assert (cooking_complexity simple))
 (printout t crlf "Derived cooking_complexity: simple" crlf))

(defrule complexity_beginner_long
 (cuisine italian)
 (cooking_skill beginner) (available_time long) (not (cooking_complexity ?x))
 =>
 (assert (cooking_complexity moderate))
 (printout t crlf "Derived cooking_complexity: moderate" crlf))

(defrule complexity_intermediate_short
 (cuisine italian)
 (cooking_skill intermediate) (available_time short) (not (cooking_complexity ?x))
 =>
 (assert (cooking_complexity simple))
 (printout t crlf "Derived cooking_complexity: simple" crlf))

(defrule complexity_intermediate_medium
 (cuisine italian)
 (cooking_skill intermediate) (available_time medium) (not (cooking_complexity ?x))
 =>
 (assert (cooking_complexity moderate))
 (printout t crlf "Derived cooking_complexity: moderate" crlf))

(defrule complexity_intermediate_long
 (cuisine italian)
 (cooking_skill intermediate) (available_time long) (not (cooking_complexity ?x))
 =>
 (assert (cooking_complexity complex))
 (printout t crlf "Derived cooking_complexity: complex" crlf))

(defrule complexity_advanced_short
 (cuisine italian)
 (cooking_skill advanced) (available_time short) (not (cooking_complexity ?x))
 =>
 (assert (cooking_complexity moderate))
 (printout t crlf "Derived cooking_complexity: moderate" crlf))

(defrule complexity_advanced_medium
 (cuisine italian)
 (cooking_skill advanced) (available_time medium) (not (cooking_complexity ?x))
 =>
 (assert (cooking_complexity complex))
 (printout t crlf "Derived cooking_complexity: complex" crlf))

(defrule complexity_advanced_long
 (cuisine italian)
 (cooking_skill advanced) (available_time long) (not (cooking_complexity ?x))
 =>
 (assert (cooking_complexity complex))
 (printout t crlf "Derived cooking_complexity: complex" crlf))

(defrule rec_it_sweet_simple
 (cuisine italian) (meal_type sweet) (cooking_complexity simple) (not (done))
 =>
 (printout t crlf "Recommend: tiramisu cups" crlf)
 (printout t "Why: quick Italian sweet for simple cooking." crlf)
 (assert (done)))

(defrule rec_it_sweet_moderate
 (cuisine italian) (meal_type sweet) (cooking_complexity moderate) (not (done))
 =>
 (printout t crlf "Recommend: panna cotta" crlf)
 (printout t "Why: classic Italian dessert, moderate effort." crlf)
 (assert (done)))

(defrule rec_it_sweet_complex
 (cuisine italian) (meal_type sweet) (cooking_complexity complex) (not (done))
 =>
 (printout t crlf "Recommend: homemade tiramisu" crlf)
 (printout t "Why: full Italian dessert for skilled cooks." crlf)
 (assert (done)))

(defrule rec_it_savory_light
 (cuisine italian) (meal_type savory) (meal_size light) (cooking_complexity ?c) (not (done))
 =>
 (printout t crlf "Recommend: minestrone" crlf)
 (printout t "Why: light Italian soup for any skill level." crlf)
 (assert (done)))

(defrule rec_it_savory_hearty_simple
 (cuisine italian) (meal_type savory) (meal_size hearty) (cooking_complexity simple) (not (done))
 =>
 (printout t crlf "Recommend: tomato pasta" crlf)
 (printout t "Why: hearty simple Italian pasta." crlf)
 (assert (done)))

(defrule rec_it_savory_hearty_moderate
 (cuisine italian) (meal_type savory) (meal_size hearty) (cooking_complexity moderate) (not (done))
 =>
 (printout t crlf "Recommend: carbonara" crlf)
 (printout t "Why: hearty Italian pasta, moderate skill." crlf)
 (assert (done)))

(defrule rec_it_savory_hearty_complex
 (cuisine italian) (meal_type savory) (meal_size hearty) (cooking_complexity complex) (not (done))
 =>
 (printout t crlf "Recommend: lasagna" crlf)
 (printout t "Why: complex hearty Italian main course." crlf)
 (assert (done)))

(defrule rec_ge_sweet_light
 (cuisine georgian) (meal_type sweet) (meal_size light) (not (done))
 =>
 (printout t crlf "Recommend: churchkhela" crlf)
 (printout t "Why: light Georgian sweet, no skill question needed." crlf)
 (assert (done)))

(defrule rec_ge_sweet_hearty
 (cuisine georgian) (meal_type sweet) (meal_size hearty) (not (done))
 =>
 (printout t crlf "Recommend: gozinaki" crlf)
 (printout t "Why: richer Georgian sweet candy." crlf)
 (assert (done)))

(defrule rec_ge_savory_light
 (cuisine georgian) (meal_type savory) (meal_size light) (not (done))
 =>
 (printout t crlf "Recommend: chikhirtma" crlf)
 (printout t "Why: light Georgian soup." crlf)
 (assert (done)))

(defrule rec_ge_savory_hearty
 (cuisine georgian) (meal_type savory) (meal_size hearty) (not (done))
 =>
 (printout t crlf "Recommend: khachapuri" crlf)
 (printout t "Why: hearty Georgian cheese bread." crlf)
 (assert (done)))

(defrule rec_ru_sweet_short
 (cuisine russian) (meal_type sweet) (available_time short) (not (done))
 =>
 (printout t crlf "Recommend: syrniki" crlf)
 (printout t "Why: fast Russian sweet when time is short." crlf)
 (assert (done)))

(defrule rec_ru_sweet_medium
 (cuisine russian) (meal_type sweet) (available_time medium) (not (done))
 =>
 (printout t crlf "Recommend: blini" crlf)
 (printout t "Why: Russian pancakes with medium time." crlf)
 (assert (done)))

(defrule rec_ru_sweet_long
 (cuisine russian) (meal_type sweet) (available_time long) (not (done))
 =>
 (printout t crlf "Recommend: blini with fillings" crlf)
 (printout t "Why: richer Russian sweet when you have time." crlf)
 (assert (done)))

(defrule rec_ru_savory_light
 (cuisine russian) (meal_type savory) (meal_size light) (not (done))
 =>
 (printout t crlf "Recommend: chicken soup" crlf)
 (printout t "Why: light Russian option; skill not asked." crlf)
 (assert (done)))

(defrule rec_ru_savory_hearty
 (cuisine russian) (meal_type savory) (meal_size hearty) (not (done))
 =>
 (printout t crlf "Recommend: pelmeni" crlf)
 (printout t "Why: hearty Russian dumplings." crlf)
 (assert (done)))

(defrule rec_jp_sweet_short
 (cuisine japanese) (meal_type sweet) (available_time short) (not (done))
 =>
 (printout t crlf "Recommend: mochi" crlf)
 (printout t "Why: quick Japanese sweet." crlf)
 (assert (done)))

(defrule rec_jp_sweet_medium
 (cuisine japanese) (meal_type sweet) (available_time medium) (not (done))
 =>
 (printout t crlf "Recommend: dorayaki" crlf)
 (printout t "Why: Japanese sweet pancakes, medium time." crlf)
 (assert (done)))

(defrule rec_jp_sweet_long
 (cuisine japanese) (meal_type sweet) (available_time long) (not (done))
 =>
 (printout t crlf "Recommend: homemade dorayaki" crlf)
 (printout t "Why: fuller Japanese dessert with more time." crlf)
 (assert (done)))

(defrule rec_jp_savory_light
 (cuisine japanese) (meal_type savory) (meal_size light) (not (done))
 =>
 (printout t crlf "Recommend: onigiri" crlf)
 (printout t "Why: light Japanese snack; time not asked." crlf)
 (assert (done)))

(defrule rec_jp_savory_hearty_short
 (cuisine japanese) (meal_type savory) (meal_size hearty) (available_time short) (not (done))
 =>
 (printout t crlf "Recommend: oyakodon" crlf)
 (printout t "Why: fast hearty Japanese bowl." crlf)
 (assert (done)))

(defrule rec_jp_savory_hearty_medium
 (cuisine japanese) (meal_type savory) (meal_size hearty) (available_time medium) (not (done))
 =>
 (printout t crlf "Recommend: teriyaki chicken" crlf)
 (printout t "Why: hearty Japanese main with medium time." crlf)
 (assert (done)))

(defrule rec_jp_savory_hearty_long
 (cuisine japanese) (meal_type savory) (meal_size hearty) (available_time long) (not (done))
 =>
 (printout t crlf "Recommend: ramen" crlf)
 (printout t "Why: long-cook hearty Japanese soup." crlf)
 (assert (done)))

(defrule rec_any_sweet_light
 (cuisine any) (meal_type sweet) (meal_size light) (not (done))
 =>
 (printout t crlf "Recommend: pancakes" crlf)
 (printout t "Why: light sweet default when cuisine=any." crlf)
 (assert (done)))

(defrule rec_any_sweet_hearty
 (cuisine any) (meal_type sweet) (meal_size hearty) (not (done))
 =>
 (printout t crlf "Recommend: blini" crlf)
 (printout t "Why: heartier sweet default when cuisine=any." crlf)
 (assert (done)))

(defrule rec_any_savory_light
 (cuisine any) (meal_type savory) (meal_size light) (not (done))
 =>
 (printout t crlf "Recommend: onigiri" crlf)
 (printout t "Why: light savory default when cuisine=any." crlf)
 (assert (done)))

(defrule rec_any_savory_hearty
 (cuisine any) (meal_type savory) (meal_size hearty) (not (done))
 =>
 (printout t crlf "Recommend: carbonara" crlf)
 (printout t "Why: hearty savory default when cuisine=any." crlf)
 (assert (done)))
