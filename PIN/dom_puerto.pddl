;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; PUERTO
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain puerto)
	(:requirements :strips :typing :equality)
	(:types muelle pila contenedor grua cinta_transporte)
	(:predicates  
		(belong ?x - (either grua cinta_transporte) ?y - muelle)
		(attached ?x - pila ?y - muelle)
		(on ?x - contenedor ?y - (either contenedor pila))
		(top ?x - contenedor ?y - pila)
		(disponible ?x - contenedor ?m - muelle)
		(empty ?x - (either cinta_transporte grua pila))
		(holding ?x - contenedor ?y - grua)
		(pick ?ct - cinta_transporte ?m - muelle)
		(transports ?x - contenedor ?ct - cinta_transporte)
		(green ?x - contenedor)
		(no-green ?x - contenedor)
	)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; ACCIONES DISPONIBLES ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	(:action take-from-non-empty-pile
		:parameters (?c1 - contenedor ?p - pila ?c2 - contenedor ?m - muelle ?g - grua)
		:precondition 
				(and	
					(top ?c1 ?p) ; el contenedor objetivo está encima de la pila
					(on ?c1 ?c2) ; el contenedor objetivo está encima de otro contenedor
					(attached ?p ?m) ; la pila está en el muelle m
					(belong ?g ?m) ; la grua está en el muelle m
					(empty ?g) ; la grua está vacía
					(disponible ?c1 ?m) ; el contenedor está disponible
				)
		:effect
				(and
					(not (top ?c1 ?p)) ; el contenedor objetivo no está ya encima de la pila
					(top ?c2 ?p) ; la nueva cima es el otro contenedor
					(not (on ?c1 ?c2)) ; el contenedor objetivo ya no está encima del otro contenedor
					(not (disponible ?c1 ?m)) ; el contenedor objetivo ya no está disponible
					(disponible ?c2 ?m) ; ahora el otro contenedor está disponible
					(not (empty ?g)) ; la grua ya no está vacía
					(holding ?c1 ?g) ; la grua está sujetando el contenedor objetivo
				)
	)

	(:action take-from-one-contenedor-pile
		:parameters (?c1 - contenedor ?p - pila ?m - muelle ?g - grua)
		:precondition 
				(and	
					(top ?c1 ?p) ; el contenedor objetivo está encima de la pila
					(on ?c1 ?p) ; el contenedor objetivo está encima de la pila
					(attached ?p ?m) ; la pila está en el muelle m
					(belong ?g ?m) ; la grua está en el muelle m
					(empty ?g) ; la grua está vacía
					(disponible ?c1 ?m) ; el contenedor está disponible
				)
		:effect
				(and
					(not (top ?c1 ?p)) ; el contenedor objetivo no está ya encima de la pila
					(empty ?p) ; la pila está vacía
					(not (on ?c1 ?p)) ; el contenedor objetivo ya no está encima de la pila
					(not (disponible ?c1 ?m)) ; el contenedor objetivo ya no está disponible
					(not (empty ?g)) ; la grua ya no está vacía
					(holding ?c1 ?g) ; la grua está sujetando el contenedor objetivo
				)
	)

	(:action leave-in-empty-pile
		:parameters (?c1 - contenedor ?p - pila ?m - muelle ?g - grua)
		:precondition 
				(and
					(empty ?p) ; la pila esta vacia
					(attached ?p ?m) ; la pila está en el muelle m
					(belong ?g ?m) ; la grua está en el muelle m
					(holding ?c1 ?g) ; la grua está sujetando c1
				)
		:effect
				(and
					(top ?c1 ?p) ; el contenedor objetivo está encima de la pila
					(not (empty ?p)) ; la pila ya no está vacía
					(on ?c1 ?p) ; el contenedor objetivo está encima de la pila
					(disponible ?c1 ?m) ; el contenedor objetivo está disponible
					(empty ?g) ; la grua está vacía
					(not (holding ?c1 ?g)) ; la grua ya no está sujetando el contenedor objetivo
				)
	)

	(:action leave-green-contenedor
		:parameters (?c1 - contenedor ?p - pila ?c2 - contenedor ?m - muelle ?g - grua)
		:precondition 
				(and
					(top ?c2 ?p) ; la pila tiene como tope c2
					(attached ?p ?m) ; la pila está en el muelle m
					(belong ?g ?m) ; la grua está en el muelle m
					(holding ?c1 ?g) ; la grua está sujetando c1
					(green ?c1)
				)
		:effect
				(and
					(top ?c1 ?p) ; el contenedor objetivo está encima de la pila
					(not (top ?c2 ?p)) ; el contenedor anterior ya no está en la cima
					(on ?c1 ?c2) ; el contenedor tiene abajo al anterior
					(disponible ?c1 ?m) ; el contenedor objetivo está disponible
					(empty ?g) ; la grua está vacía
					(not (holding ?c1 ?g)) ; la grua ya no está sujetando el contenedor objetivo
				)
	)

	(:action leave-ordinary-contenedor
		:parameters (?c1 - contenedor ?p - pila ?c2 - contenedor ?m - muelle ?g - grua)
		:precondition 
				(and
					(top ?c2 ?p) ; la pila tiene como tope c2
					(attached ?p ?m) ; la pila está en el muelle m
					(belong ?g ?m) ; la grua está en el muelle m
					(holding ?c1 ?g) ; la grua está sujetando c1
					(no-green ?c1)
				)
		:effect
				(and
					(top ?c1 ?p) ; el contenedor objetivo está encima de la pila
					(not (top ?c2 ?p)) ; el contenedor anterior ya no está en la cima
					(on ?c1 ?c2) ; el contenedor tiene abajo al anterior
					(disponible ?c1 ?m) ; el contenedor objetivo está disponible
					(not (disponible ?c2 ?m)) ; el contenedor de abajo ya no está disponible
					(empty ?g) ; la grua está vacía
					(not (holding ?c1 ?g)) ; la grua ya no está sujetando el contenedor objetivo
				)
	)

	(:action leave-in-cinta_transporte
		:parameters (?c1 - contenedor ?ct - cinta_transporte ?m - muelle ?g - grua)
		:precondition 
					(and
						(holding ?c1 ?g) ; la grua tiene c1
						(belong ?g ?m) ; la grua está en el muelle m
						(belong ?ct ?m) ; la cinta transportadora está en m
						(empty ?ct) ; la cinta transportadora está vacía
					)
		:effect
				(and
					(transports ?c1 ?ct)
					(not (empty ?ct))
					(empty ?g) ; la grua está vacía
					(not (holding ?c1 ?g)) ; la grua ya no está sujetando el contenedor objetivo
				)
	)

	(:action take-from-cinta_transporte
		:parameters (?c1 - contenedor ?ct - cinta_transporte ?m - muelle ?g - grua)
		:precondition 
					(and
						(empty ?g) ; la grua no tiene nada
        				(pick ?ct ?m) ; en esta cinta transportadora se recogen contenedores
						(belong ?g ?m) ; la grua está en el muelle m
						(transports ?c1 ?ct) ; la cinta transportadora tiene c1
					)
		:effect
				(and
					(empty ?ct) ; la cinta transportadora está vacía
					(not (transports ?c1 ?ct)) ; la cinta transportadora está vacía
					(not (empty ?g)) ; la grua ya no está vacía
					(holding ?c1 ?g) ; la grua está sujetando el contenedor objetivo
				)
	)
)