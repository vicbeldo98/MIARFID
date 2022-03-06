(define (problem puerto1)
    
    (:domain puerto)
    
    (:objects 
        M1 M2 - dock
        P1 P2 P3 P4 P5 P6 - pile
        C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 - container
        G1 G2 - crane
        CT1 CT2 - conveyor
        n0 n1 n2 n3 n4 n5 n6 n7 n8 - height
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
        (on C10 C7)
        (on C2 P2)
        (on C5 C2)
        (on C8 C5)
        (on C11 C8)
        (on C13 C11)
        (on C3 P3)
        (on C6 C3)
        (on C9 C6)
        (on C12 C9)
        (on C14 P4)
        (on C17 C14)
        (on C20 C17)
        (on C23 C20)
        (on C15 P5)
        (on C18 C15)
        (on C21 C18)
        (on C16 P6)
        (on C19 C16)
        (on C22 C19)
        (on C24 C22)

        (top C10 P1)
        (top C13 P2)
        (top C12 P3)
        (top C23 P4)
        (top C21 P5)
        (top C24 P6)

        (available C10 M1)
        (available C13 M1)
        (available C12 M1)
        (available C23 M2)
        (available C21 M2)
        (available C18 M2)
        (available C24 M2)

        (green C1)
        (green C4)
        (green C8)
        (green C9)
        (green C15)
        (green C17)
        (green C21)
        (green C22)
        (no-green C2)
        (no-green C3)
        (no-green C5)
        (no-green C6)
        (no-green C7)
        (no-green C10)
        (no-green C11)
        (no-green C12)
        (no-green C13)
        (no-green C14)
        (no-green C16)
        (no-green C18)
        (no-green C19)
        (no-green C20)
        (no-green C23)
        (no-green C24)

        (empty CT1)
        (empty CT2)

        (empty G1)
        (empty G2)

        ; height succession definition

        
        (next M1 n0 n1)
        (next M1 n1 n2)
        (next M1 n2 n3)
        (next M1 n3 n4)
        (next M1 n4 n5)
        (next M1 n5 n6)
        (next M1 n6 n7)
        (next M1 n7 n8)

        (next M2 n0 n1)
        (next M2 n1 n2)
        (next M2 n2 n3)
        (next M2 n3 n4)
        (next M2 n4 n5)
        (next M2 n5 n6)
        (next M2 n6 n7)
        (next M2 n7 n8)

        ; starting pile height

        (current-height P1 n4)
        (current-height P2 n5)
        (current-height P3 n4)
        (current-height P4 n4)
        (current-height P5 n3)
        (current-height P6 n4)

    )

    (:goal
        (and
            (available C1 M1)
            (available C4 M1)
            (available C8 M1)
            (available C9 M1)
            (available C15 M1)
            (available C17 M1)
            (available C21 M1)
            (available C22 M1)
        )
    )
)