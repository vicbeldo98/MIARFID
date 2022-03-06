(define (problem puerto1)
    
    (:domain puerto)
    
    (:objects 
        M1 M2 - dock
        P1 P2 P3 P4 - pile
        C1 C2 C3 C4 C5 C6 C7 C8 - container
        G1 G2 - crane
        CT1 CT2 - conveyor
        n0 n1 n2 n3 n4 - height
    )

    (:init

        (belong G1 M1)
        (belong G2 M2)

        (belong CT1 M1)
        (belong CT2 M2)

        ;; Cambiado por refactorización, antes era attached
        (belong P1 M1)
        (belong P2 M1)
        (belong P3 M2)
        (belong P4 M2)

        (pick CT2 M1)
        (pick CT1 M2)

        (on C1 P1)
        (on C3 C1)
        (on C2 P2)
        (on C4 C2)
        (on C5 P3)
        (on C7 C5)
        (on C6 P4)
        (on C8 C6)

        (top C3 P1)
        (top C4 P2)
        (top C7 P3)
        (top C8 P4)

        (available C3 M1)
        (available C4 M1)
        (available C7 M2)
        (available C8 M2)
        (available C6 M2)

        (green C1)
        (green C5)
        (green C8)
        (no-green C2)
        (no-green C3)
        (no-green C4)
        (no-green C6)
        (no-green C7)

        (empty CT1)
        (empty CT2)

        (empty G1)
        (empty G2)

        ; height succession definition

        (next M1 n0 n1)
        (next M1 n1 n2)
        (next M1 n2 n3)
        (next M1 n3 n4)

        (next M2 n0 n1)
        (next M2 n1 n2)
        (next M2 n2 n3)
        (next M2 n3 n4)

        ; starting pile height

        (current-height P1 n2)
        (current-height P2 n2)
        (current-height P3 n2)
        (current-height P4 n2)

    )

    (:goal
        (and
            (available C1 M1)
            (available C5 M1)
            (available C8 M1)
        )
    )
)