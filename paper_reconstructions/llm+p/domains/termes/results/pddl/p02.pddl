(define
   (problem termes_problem)
   (:domain termes)

   (:objects 
      n0 - numb
      n1 - numb
      n2 - numb
      n3 - numb
      pos-0-0 - position
      pos-0-1 - position
      pos-0-2 - position
      pos-1-0 - position
      pos-1-1 - position
      pos-1-2 - position
      pos-2-0 - position
      pos-2-1 - position
      pos-2-2 - position
      pos-3-0 - position
      pos-3-1 - position
      pos-3-2 - position
   )

   (:init
      (height pos-0-0 n0)
      (height pos-0-1 n0)
      (height pos-0-2 n0)
      (height pos-1-0 n0)
      (height pos-1-1 n0)
      (height pos-1-2 n0)
      (height pos-2-0 n0)
      (height pos-2-1 n0)
      (height pos-2-2 n0)
      (height pos-3-0 n0)
      (height pos-3-1 n0)
      (height pos-3-2 n0)
      (at pos-2-0)
      (IS-DEPOT pos-2-0)
      (SUCC n1 n0)
      (SUCC n2 n1)
      (SUCC n3 n2)
      (NEIGHBor pos-0-0 pos-1-0)
      (NEIGHBor pos-0-0 pos-0-1)
      (NEIGHBor pos-0-1 pos-0-0)
      (NEIGHBor pos-0-1 pos-0-2)
      (NEIGHBor pos-0-1 pos-1-1)
      (NEIGHBor pos-0-2 pos-0-1)
      (NEIGHBor pos-0-2 pos-1-2)
      (NEIGHBor pos-1-0 pos-0-0)
      (NEIGHBor pos-1-0 pos-2-0)
      (NEIGHBor pos-1-0 pos-1-1)
      (NEIGHBor pos-1-1 pos-0-1)
      (NEIGHBor pos-1-1 pos-1-0)
      (NEIGHBor pos-1-1 pos-1-2)
      (NEIGHBor pos-1-1 pos-2-1)
      (NEIGHBor pos-1-2 pos-0-2)
      (NEIGHBor pos-1-2 pos-1-1)
      (NEIGHBor pos-1-2 pos-2-2)
      (NEIGHBor pos-2-0 pos-1-0)
      (NEIGHBor pos-2-0 pos-3-0)
      (NEIGHBor pos-2-0 pos-2-1)
      (NEIGHBor pos-2-1 pos-1-1)
      (NEIGHBor pos-2-1 pos-2-0)
      (NEIGHBor pos-2-1 pos-2-2)
      (NEIGHBor pos-2-1 pos-3-1)
      (NEIGHBor pos-2-2 pos-1-2)
      (NEIGHBor pos-2-2 pos-2-1)
      (NEIGHBor pos-2-2 pos-3-2)
      (NEIGHBor pos-3-0 pos-2-0)
      (NEIGHBor pos-3-0 pos-3-1)
      (NEIGHBor pos-3-1 pos-2-1)
      (NEIGHBor pos-3-1 pos-3-0)
      (NEIGHBor pos-3-1 pos-3-2)
      (NEIGHBor pos-3-2 pos-2-2)
      (NEIGHBor pos-3-2 pos-3-1)
   )

   (:goal
      (and 
         (height pos-2-1 n3)
         (height pos-3-0 n3)
         (not (has-block ))
      )
   )
)