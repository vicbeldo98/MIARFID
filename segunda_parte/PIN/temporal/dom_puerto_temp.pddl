;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; PUERTO
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain puerto)

	(:requirements :strips :typing :fluents :durative-actions)

	(:types dock pile container crane conveyor height)

	(:predicates
		(belong ?x - (either crane conveyor pile) ?y - dock)
		(on ?x - container ?y - (either container pile conveyor))
		(top ?x - (either container pile) ?y - pile)
		(available ?x - (either container pile) ?m - dock)
		(empty ?x - (either conveyor crane))
		(holding ?x - container ?y - crane)
		(pick ?ct - conveyor ?m - dock)
		(green ?x - container)
		(no-green ?x - container)
		(next ?m - dock ?x - height ?y - height)
		(current-height ?p - pile ?x - height)
        (needs-transport ?c - container)
		(transported ?c - container)
	)

    (:functions
        (weight ?c1 - container)
        (time-height ?x - height)
        (conveyor-length ?ct -conveyor)
        (conveyor-speed ?ct -conveyor)
    )

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; ACCIONES availableS ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	(:durative-action take
		:parameters (?c1 - container ?p - pile ?c2 - (either container pile) ?m - dock ?g - crane ?alt - height ?new_alt - height)
		:duration (= ?duration (* (weight ?c1) (time-height ?alt)))
		:condition 
				(and
					(at start (top ?c1 ?p))
					(at start (on ?c1 ?c2))
					(over all (belong ?p ?m))
					(over all (belong ?g ?m))
					(at start (empty ?g))
					(at start (available ?c1 ?m))
					(at start (current-height ?p ?alt))
					(over all (next ?m ?new_alt ?alt))
				)
		:effect
				(and
					(at start (not (top ?c1 ?p)))
					(at start (not (on ?c1 ?c2)))
					(at start (not (available ?c1 ?m))) ; container isnt available when the crane is holding it
					(at start (not (empty ?g)))
					(at end (holding ?c1 ?g))
					(at end (top ?c2 ?p))
					(at end (available ?c2 ?m))
					(at start (not (current-height ?p ?alt))) ; update current pile height
					(at end (current-height ?p ?new_alt))
				)
	)

	(:durative-action leave-green-container
		:parameters (?c1 - container ?p - pile ?c2 - (either container pile) ?m - dock ?g - crane ?alt - height ?new_alt - height)
		:duration (= ?duration (* (weight ?c1) (time-height ?alt)))
		:condition 
				(and
					(at start (top ?c2 ?p))
					(over all (belong ?p ?m))
					(over all (belong ?g ?m))
					(at start (holding ?c1 ?g))
					(over all (green ?c1))
					(at start (current-height ?p ?alt))
					(over all (next ?m ?alt ?new_alt))
				)
		:effect
				(and
					(at end (top ?c1 ?p))
					(at start (not (top ?c2 ?p)))
					(at end (on ?c1 ?c2))
					(at end (available ?c1 ?m))
					(at end (empty ?g))
					(at start (not (holding ?c1 ?g)))
					(at start (not (current-height ?p ?alt)))
					(at end (current-height ?p ?new_alt))
				)
	)

	(:durative-action leave-ordinary-container
		:parameters (?c1 - container ?p - pile ?c2 - (either container pile) ?m - dock ?g - crane ?alt - height ?new_alt - height)
		:duration (= ?duration (* (weight ?c1) (time-height ?alt)))
		:condition 
				(and
					(at start (top ?c2 ?p))
					(over all (belong ?p ?m))
					(over all (belong ?g ?m))
					(at start (holding ?c1 ?g))
					(over all (no-green ?c1))
					(at start (current-height ?p ?alt))
					(over all (next ?m ?alt ?new_alt))
				)
		:effect
				(and
					(at end (top ?c1 ?p))
					(at start (not (top ?c2 ?p)))
					(at end (on ?c1 ?c2))
					(at end (available ?c1 ?m))
					(at start (not (available ?c2 ?m)))
					(at end (empty ?g))
					(at start (not (holding ?c1 ?g)))
					(at start (not (current-height ?p ?alt)))
					(at end (current-height ?p ?new_alt))
				)
	)

	(:durative-action leave-in-conveyor
		:parameters (?c1 - container ?ct - conveyor ?m - dock ?g - crane)
		:duration (= ?duration (weight ?c1))
		:condition 
				(and
					(at start (holding ?c1 ?g))
					(over all (belong ?g ?m))
					(over all (belong ?ct ?m))
					(at start (empty ?ct))
				)
		:effect
				(and
					(at end (on ?c1 ?ct))
					(at start (not (empty ?ct)))
					(at end (empty ?g))
					(at start (not (holding ?c1 ?g)))
                    (at end (needs-transport ?c1))
				)
	)

    (:durative-action transport-conveyor
		:parameters (?c1 - container ?ct - conveyor)
		:duration (= ?duration (/ (conveyor-length ?ct) (conveyor-speed ?ct)))
		:condition 
				(and
					(at start (needs-transport ?c1))
					(over all (on ?c1 ?ct))
				)
		:effect
				(and
					(at start (not (needs-transport ?c1)))
					(at end (transported ?c1))
				)
	)

	(:durative-action take-from-conveyor
		:parameters (?c1 - container ?ct - conveyor ?m - dock ?g - crane)
		:duration (= ?duration (weight ?c1))
		:condition 
				(and
					(at start (empty ?g))
					(over all (pick ?ct ?m))
					(over all (belong ?g ?m))
					(at start (on ?c1 ?ct))
					(at start (transported ?c1))
				)
		:effect
				(and
					(at start (empty ?ct))
					(at start (not (on ?c1 ?ct)))
					(at start (not (empty ?g)))
					(at end (holding ?c1 ?g))
					(at start (not (transported ?c1)))
				)
	)
)
