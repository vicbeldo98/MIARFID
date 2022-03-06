(define (problem puerto1)
    
    (:domain puerto)
    
    (:objects 
        M1 M2 - dock
        P1 P2 P3 P4 P5 P6 - pile
        C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 - container
        G1 G2 - crane
        CT1 CT2 - conveyor
        n0 n1 n2 n3 - height
    )

    (:init

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
        (on C4 C1)
        (on C7 C4)
        (on C2 P2)
        (on C5 C2)
        (on C8 C5)
        (on C3 P3)
        (on C6 C3)
        (on C9 P4)
        (on C12 C9)
        (on C10 P5)
        (on C13 C10)
        (on C11 P6)
        (on C14 C11)

        (top C7 P1)
        (top C8 P2)
        (top C6 P3)
        (top C12 P4)
        (top C13 P5)
        (top C14 P6)

        (available C7 M1)
        (available C8 M1)
        (available C5 M1)
        (available C6 M1)
        (available C12 M2)
        (available C9 M2)
        (available C13 M2)
        (available C14 M2)

        (green C1)
        (green C8)
        (green C12)
        (no-green C2)
        (no-green C3)
        (no-green C4)
        (no-green C5)
        (no-green C6)
        (no-green C7)
        (no-green C9)
        (no-green C10)
        (no-green C11)
        (no-green C13)
        (no-green C14)

        (empty CT1)
        (empty CT2)

        (empty G1)
        (empty G2)

        ; height succession definition

        (next M1 n0 n1)
        (next M1 n1 n2)
        (next M1 n2 n3)

        (next M2 n0 n1)
        (next M2 n1 n2)

        ; starting pile height

        (current-height P1 n3)
        (current-height P2 n3)
        (current-height P3 n2)
        (current-height P4 n2)
        (current-height P5 n2)
        (current-height P6 n2)

    )

    (:goal
        (and
            (available C1 M1)
            (available C8 M1)
            (available C12 M1)
        )
    )
)