;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; PUERTO
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain puerto)
	(:requirements :strips :typing :equality)
	(:types dock pile container crane conveyor)
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
	)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; ACCIONES availableS ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	(:action take
		:parameters (?c1 - container ?p - pile ?c2 - (either container pile) ?m - dock ?g - crane ?alt - height ?new_alt - height)
		:precondition 
				(and	
					(top ?c1 ?p)
					(on ?c1 ?c2)
					(belong ?p ?m)
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
					(not (available ?c1 ?m)) ; container isnt available when the crane is holding it
					(not (empty ?g))
					(holding ?c1 ?g)
					(top ?c2 ?p)
					(available ?c2 ?m)
					(not (current-height ?p ?alt)) ; update current pile height
					(current-height ?p ?new_alt)
				)
	)

	(:action leave-green-container
		:parameters (?c1 - container ?p - pile ?c2 - (either container pile) ?m - dock ?g - crane ?alt - height ?new_alt - height)
		:precondition 
				(and
					(top ?c2 ?p)
					(belong ?p ?m)
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
		:parameters (?c1 - container ?p - pile ?c2 - (either container pile) ?m - dock ?g - crane ?alt - height ?new_alt - height)
		:precondition 
				(and
					(top ?c2 ?p)
					(belong ?p ?m)
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
					(on ?c1 ?ct)
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
						(on ?c1 ?ct)
					)
		:effect
				(and
					(empty ?ct)
					(not (on ?c1 ?ct))
					(not (empty ?g))
					(holding ?c1 ?g)
				)
	)
)
