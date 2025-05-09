(define (domain blocksworld_domain)
    (:requirements :conditional-effects :disjunctive-preconditions :equality :negative-preconditions :strips :typing :universal-preconditions)
    (:types arm block table - object)
    (:predicates (clear ?b - block)  (empty ?a - arm)  (holding ?a - arm ?b - block)  (on_top ?b1 - block ?b2 - block))
    (:action stack
        :parameters (?arm - arm ?top - block ?bottom - block)
        :precondition (and (holding ?arm ?top) (clear ?bottom) (not (on_top ?top ?bottom)) (not (empty ?arm)))
        :effect (and (empty ?arm) (on_top ?top ?bottom) (not (clear ?bottom)) (not (holding ?arm ?top)))
    )
)