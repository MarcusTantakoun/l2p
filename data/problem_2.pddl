(define (problem test_domain_problem)
    (:domain test_domain)
    (:objects arm1 - arm blue green red yellow - block table1 - table)
    (:init (arm_empty arm1) (clear arm1) (clear blue) (clear green) (on blue red) (on green yellow) (on_table red) (on_table yellow))
    (:goal (and (on green red) (on blue green) (on yellow blue) (clear yellow)))
)