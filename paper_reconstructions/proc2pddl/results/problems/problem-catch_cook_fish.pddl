(define (problem catch_cook_fish)
    (:domain survive_deserted_island)
    (:objects down east in north out south up west - direction fire - fire fish - fish beach jungle ocean river - location person - player rock - rock spear - spear survivor - survivor tinder - tinder vines - vines water - water wood - wood)
    (:init (at person beach) (at rock ocean) (at survivor river) (at tinder beach) (at vines jungle) (at_ocean beach) (can_light_fire beach) (connected beach east jungle) (connected beach west ocean) (connected jungle east river) (connected jungle north cave) (connected jungle west beach) (connected ocean east beach) (connected river west jungle) (has_fish river) (has_water_source river) (has_wood jungle))
    (:goal (cooked fish))
)