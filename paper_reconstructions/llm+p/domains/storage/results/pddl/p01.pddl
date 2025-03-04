(define
   (problem storage_problem)
   (:domain storage)

   (:objects 
      depot48-1-1 - storearea
      container-0-0 - storearea
      hoist0 - hoist
      crate0 - crate
      container0 - container
      depot48 - depot
      loadarea - transitarea
   )

   (:init
      (connected depot48-1-1 depot48-1-1)
      (on crate0 container-0-0)
      (in crate0 container0)
      (in container-0-0 container0)
      (connected loadarea container-0-0)
      (connected container-0-0 loadarea)
      (connected depot48-1-1 loadarea)
      (connected loadarea depot48-1-1)
      (at hoist0 depot48-1-1)
      (available hoist0)
      (in depot48-1-1 depot48)
   )

   (:goal
      (and 
         (in crate0 depot48) 
      )
   )

)