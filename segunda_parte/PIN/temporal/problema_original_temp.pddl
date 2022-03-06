(define (problem puerto1)

    (:domain puerto)

    (:objects
        M1 M2 - dock
        P1 P2 P3 P4 P5 P6 - pile
        C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 - container
        G1 G2 - crane
        CT1 CT2 - conveyor
        n0 n1 n2 n3 n4 - height
    )

    (:init

        (= (weight C1) 20)
        (= (weight C2) 20)
        (= (weight C3) 20)
        (= (weight C4) 20)
        (= (weight C5) 20)
        (= (weight C6) 20)
        (= (weight C7) 20)
        (= (weight C8) 20)
        (= (weight C9) 20)
        (= (weight C10) 20)
        (= (weight C11) 20)

        (= (time-height n0) 1)
        (= (time-height n1) 0.8)
        (= (time-height n2) 0.6)
        (= (time-height n3) 0.4)
        (= (time-height n4) 0.2)

        (= (conveyor-length CT1) 15)
        (= (conveyor-length CT2) 25)

        (= (conveyor-speed CT1) 5)
        (= (conveyor-speed CT2) 5)

        (belong G1 M1)
        (belong G2 M2)

        (belong CT1 M1)
        (belong CT2 M2)

        (pick CT2 M1)
        (pick CT1 M2)

        (belong P1 M1)
        (belong P2 M1)
        (belong P3 M1)
        (belong P4 M2)
        (belong P5 M2)
        (belong P6 M2)

        (on C1 P1)
        (on C7 C1)
        (on C9 P2)
        (on C10 C9)
        (on C11 P3)
        (on C4 P4)
        (on C8 C4)
        (on C5 P5)
        (on C3 C5)
        (on C2 C3)
        (on C6 P6)

        (top C7 P1)
        (top C10 P2)
        (top C11 P3)
        (top C8 P4)
        (top C2 P5)
        (top C6 P6)

        (available C7 M1)
        (available C1 M1)
        (available C10 M1)
        (available C11 M1)
        (available C8 M2)
        (available C2 M2)
        (available C6 M2)

        (green C3)
        (green C4)
        (green C7)
        (no-green C1)
        (no-green C2)
        (no-green C5)
        (no-green C6)
        (no-green C8)
        (no-green C9)
        (no-green C10)
        (no-green C11)

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
        (current-height P3 n1)
        (current-height P4 n2)
        (current-height P5 n3)
        (current-height P6 n1)

    )

    (:goal
        (and
            (available C3 M1)
            (available C4 M1)
            (available C7 M1)
        )
    )

    (:metric minimize (total-time))
)