(define (problem test_domain_problem)
    (:domain test_domain)
    (:objects arm1 - arm blue green red yellow - block table1 - table)
    (:init (arm_empty arm1) (clear blue) (clear green) (on blue red) (on red yellow) (on_table green) (on_table yellow))
    (:goal (and (on red green) (clear red) (arm_empty arm1)))
)