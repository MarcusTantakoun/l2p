(define (problem blocksworld_problem)
    (:domain blocksworld)
    (:objects block1 block2 block3 block4 block5 - block table1 - location)
    (:init (clear_block block3) (clear_block block5) (hand_empty) (on_block block2 block1) (on_block block3 block2) (on_block block5 block4) (on_location block1 table1) (on_location block4 table1))
    (:goal (and (on_location block1 table1) (on_block block5 block1) (on_block block2 block5) (on_block block4 block2) (on_block block3 block4) (hand_empty)))
)