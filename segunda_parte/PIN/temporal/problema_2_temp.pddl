(define (problem puerto1)
    
    (:domain puerto)
    
    (:objects 
        M1 M2 - dock
        P1 P2 P3 P4 P5 P6 - pile
        C1 C2 C3 C4 C5 C6 C7 - container
        G1 G2 - crane
        CT1 CT2 - conveyor
        n0 n1 n2 - height
    )

    (:init

        (= (weight C1) 20)
        (= (weight C2) 20)
        (= (weight C3) 20)
        (= (weight C4) 20)
        (= (weight C5) 20)
        (= (weight C6) 20)
        (= (weight C7) 20)

        (= (time-height n0) 1)
        (= (time-height n1) 0.75)
        (= (time-height n2) 0.5)

        (= (conveyor-length CT1) 15)
        (= (conveyor-length CT2) 25)

        (= (conveyor-speed CT1) 5)
        (= (conveyor-speed CT2) 5)

        (belong G1 M1)
        (belong G2 M2)

        (belong CT1 M1)
        (belong CT2 M2)

        ;; Cambiado por refactorización, antes era attached
        (belong P1 M1)
        (belong P2 M1)
        (belong P3 M1)
        (belong P4 M2)
        (belong P5 M2)
        (belong P6 M2)

        (pick CT2 M1)
        (pick CT1 M2)

        (on C1 P1)
        (on C2 P2)
        (on C3 P3)
        (on C4 P4)
        (on C7 C4)
        (on C5 P5)
        (on C6 P6)

        (top C1 P1)
        (top C2 P2)
        (top C3 P3)
        (top C7 P4)
        (top C5 P5)
        (top C6 P6)

        (available C1 M1)
        (available C2 M1)
        (available C3 M1)
        (available C4 M2)
        (available C5 M2)
        (available C6 M2)
        (available C7 M2)
        ;; Se necesita por consistencia?
        ;; No debería hacer nada estando o no ya que nunca hay una precondición de que esté available el
        ;; c2 (sea container o pila) mientras sea top, pero creo que mejor dejarlo puesto
        (available P4 M2)
        (available P5 M2)
        (available P6 M2)

        (green C4)
        (green C5)
        (green C6)
        (green C7)
        (no-green C1)
        (no-green C2)
        (no-green C3)

        (empty CT1)
        (empty CT2)

        (empty G1)
        (empty G2)

        ; height succession definition

        (next M1 n0 n1)
        (next M1 n1 n2)

        (next M2 n0 n1)
        (next M2 n1 n2)

        ; starting pile height

        (current-height P1 n1)
        (current-height P2 n1)
        (current-height P3 n1)
        (current-height P4 n2)
        (current-height P5 n1)
        (current-height P6 n1)

    )

    (:goal
        (and
            (available C4 M1)
            (available C5 M1)
            (available C6 M1)
            (available C7 M1)
        )
    )
)