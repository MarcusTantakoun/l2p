(define (problem test_domain_1_problem)
    (:domain test_domain)
    (:objects robotic_arm - arm blue green red yellow - block main_table - table)
    (:init (arm_empty robotic_arm) (clear blue) (clear green) (on blue red) (on red yellow) (on_table green main_table) (on_table yellow main_table))
    (:goal (on red green))
)