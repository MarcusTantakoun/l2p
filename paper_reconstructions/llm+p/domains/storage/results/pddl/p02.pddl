(define
   (problem storage_problem)
   (:domain storage)

   (:objects 
      depot48-1-1 depot48-1-2 - storearea
      container-0-0 - storearea
      hoist0 hoist1 - hoist
      crate0 - crate
      container0 - container
      depot48 - depot
      loadarea - transitarea
   )

   (:init
      (connected depot48-1-1 depot48-1-2)
      (in depot48-1-1 depot48)
      (in depot48-1-2 depot48)
      (on crate0 container-0-0)
      (in crate0 container0)
      (in container-0-0 container0)
      (connected loadarea container-0-0)
      (connected container-0-0 loadarea)
      (connected depot48-1-1 loadarea)
      (at hoist0 depot48-1-1)
      (available hoist0)
      (at hoist1 depot48-1-2)
      (available hoist1)
      (clear depot48-1-1)
      (clear depot48-1-2)
   )

   (:goal
      (and 
         (in crate0 depot48) 
      )
   )

)