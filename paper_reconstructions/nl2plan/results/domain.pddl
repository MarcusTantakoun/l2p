(define (domain test_domain)
    (:requirements :conditional-effects :disjunctive-preconditions :equality :negative-preconditions :strips :typing :universal-preconditions)
    (:types arm block table - object)
    (:predicates (clear ?b - block)  (empty ?a - arm)  (holding ?a - arm ?b - block)  (on ?b1 - block ?b2 - block)  (on-table ?b - block ?t - table))
    (:action pickup
        :parameters (?b - block ?a - arm ?t - table)
        :precondition (and (clear ?t) (empty ?a) (on-table ?b ?t))
        :effect (and (holding ?a ?b) (not (on-table ?b ?t)) (not (clear ?t)))
    )
     (:action putdown
        :parameters (?a - arm ?b - block ?t - table)
        :precondition (holding ?a ?b)
        :effect (and (not (holding ?a ?b)) (on-table ?b ?t))
    )
     (:action stack
        :parameters (?a - arm ?b_top - block ?b_bottom - block)
        :precondition (and (holding ?a ?b_top) (clear ?b_bottom))
        :effect (and (not (holding ?a ?b_top)) (on ?b_top ?b_bottom) (not (clear ?b_bottom)))
    )
     (:action unstack
        :parameters (?a - arm ?b1 - block ?b2 - block ?t - table)
        :precondition (and (empty ?a) (clear ?b1) (on ?b1 ?b2))
        :effect (and (holding ?a ?b1) (not (on ?b1 ?b2)) (clear ?b2))
    )
)