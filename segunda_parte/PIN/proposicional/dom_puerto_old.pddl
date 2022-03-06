;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; PUERTO
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain puerto)
	(:requirements :strips :typing :equality)
	(:types dock pile container crane conveyor height)
	(:predicates
		(belong ?x - (either crane conveyor) ?y - dock)
		(attached ?x - pile ?y - dock)
		(on ?x - container ?y - (either container pile))
		(top ?x - container ?y - pile)
		(available ?x - container ?m - dock)
		(empty ?x - (either conveyor crane pile))
		(holding ?x - container ?y - crane)
		(pick ?ct - conveyor ?m - dock)
		(transports ?x - container ?ct - conveyor)
		(green ?x - container)
		(no-green ?x - container)
		(next ?m - dock ?x - height ?y - height)
		(current-height ?p - pile ?x - height)
	)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; ACCIONES availableS ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	(:action take-from-non-empty-pile
		:parameters (?c1 - container ?p - pile ?c2 - container ?m - dock ?g - crane ?alt - height ?new_alt - height)
		:precondition
				(and
					(top ?c1 ?p)
					(on ?c1 ?c2)
					(attached ?p ?m)
					(belong ?g ?m)
					(empty ?g)
					(available ?c1 ?m)
					(current-height ?p ?alt)
					(next ?m ?new_alt ?alt)
				)
		:effect
				(and
					(not (top ?c1 ?p))
					(not (on ?c1 ?c2))
					(not (available ?c1 ?m)) ; container isnt available
					(not (empty ?g))
					(holding ?c1 ?g)
					(top ?c2 ?p)
					(available ?c2 ?m)
					(not (current-height ?p ?alt)) ; update current pile height
					(current-height ?p ?new_alt)
				)
	)

	(:action take-from-one-container-pile
		:parameters (?c1 - container ?p - pile ?m - dock ?g - crane ?alt - height ?new_alt - height)
		:precondition
				(and
					(top ?c1 ?p)
					(on ?c1 ?p)
					(attached ?p ?m)
					(belong ?g ?m)
					(empty ?g)
					(available ?c1 ?m)
					(current-height ?p ?alt)
					(next ?m ?new_alt ?alt)
				)
		:effect
				(and
					(not (top ?c1 ?p))
					(empty ?p)
					(not (on ?c1 ?p))
					(not (available ?c1 ?m))
					(not (empty ?g))
					(holding ?c1 ?g)
					(not (current-height ?p ?alt))
					(current-height ?p ?new_alt)
				)
	)

	(:action leave-in-empty-pile
		:parameters (?c1 - container ?p - pile ?m - dock ?g - crane ?alt - height ?new_alt - height)
		:precondition
				(and
					(empty ?p)
					(attached ?p ?m)
					(belong ?g ?m)
					(holding ?c1 ?g)
					(current-height ?p ?alt)
					(next ?m ?alt ?new_alt)
				)
		:effect
				(and
					(top ?c1 ?p)
					(not (empty ?p))
					(on ?c1 ?p)
					(available ?c1 ?m)
					(empty ?g)
					(not (holding ?c1 ?g))
					(not (current-height ?p ?alt))
					(current-height ?p ?new_alt)
				)
	)

	(:action leave-green-container
		:parameters (?c1 - container ?p - pile ?c2 - container ?m - dock ?g - crane ?alt - height ?new_alt - height)
		:precondition
				(and
					(top ?c2 ?p)
					(attached ?p ?m)
					(belong ?g ?m)
					(holding ?c1 ?g)
					(green ?c1)
					(current-height ?p ?alt)
					(next ?m ?alt ?new_alt)
				)
		:effect
				(and
					(top ?c1 ?p)
					(not (top ?c2 ?p))
					(on ?c1 ?c2)
					(available ?c1 ?m)
					(empty ?g)
					(not (holding ?c1 ?g))
					(not (current-height ?p ?alt))
					(current-height ?p ?new_alt)
				)
	)

	(:action leave-ordinary-container
		:parameters (?c1 - container ?p - pile ?c2 - container ?m - dock ?g - crane ?alt - height ?new_alt - height)
		:precondition
				(and
					(top ?c2 ?p)
					(attached ?p ?m)
					(belong ?g ?m)
					(holding ?c1 ?g)
					(no-green ?c1)
					(current-height ?p ?alt)
					(next ?m ?alt ?new_alt)
				)
		:effect
				(and
					(top ?c1 ?p)
					(not (top ?c2 ?p))
					(on ?c1 ?c2)
					(available ?c1 ?m)
					(not (available ?c2 ?m))
					(empty ?g)
					(not (holding ?c1 ?g))
					(not (current-height ?p ?alt))
					(current-height ?p ?new_alt)
				)
	)

	(:action leave-in-conveyor
		:parameters (?c1 - container ?ct - conveyor ?m - dock ?g - crane)
		:precondition
					(and
						(holding ?c1 ?g)
						(belong ?g ?m)
						(belong ?ct ?m)
						(empty ?ct)
					)
		:effect
				(and
					(transports ?c1 ?ct)
					(not (empty ?ct))
					(empty ?g)
					(not (holding ?c1 ?g))
				)
	)

	(:action take-from-conveyor
		:parameters (?c1 - container ?ct - conveyor ?m - dock ?g - crane)
		:precondition
					(and
						(empty ?g)
        					(pick ?ct ?m)
						(belong ?g ?m)
						(transports ?c1 ?ct)
					)
		:effect
				(and
					(empty ?ct)
					(not (transports ?c1 ?ct))
					(not (empty ?g))
					(holding ?c1 ?g)
				)
	)
)
