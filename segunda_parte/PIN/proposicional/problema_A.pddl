(define (problem puerto1)

    (:domain puerto)

    (:objects
        M1 - dock
        P1 P2 P3 P4 P5 P6 - pile
        C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 - container
        G1 G2 - crane
        CT1 CT2 - conveyor
        n0 n1 n2 n3 n4 - height
    )

    (:init
        (belong G1 M1)

        (belong CT1 M1)

        (pick CT2 M1)

        (attached P1 M1)
        (attached P2 M1)
        (attached P3 M1)

        (on C1 P1)
        (on C2 C1)
        (on C3 C2)
        (on C4 P2)

        (top C3 P1)
        (top C4 P2)

        (available C3 M1)
        (available C2 M1)
        (available C4 M1)

        (green C1)
        (green C3)

        (no-green C2)
        (no-green C4)

        (empty CT1)
        (empty CT2)

        (empty G1)
        (empty G2)

        (next M1 n0 n1)
        (next M1 n1 n2)
        (next M1 n2 n3)
        (next M1 n3 n4)

        (current-height P1 n2)
        (current-height P2 n2)
        (current-height P3 n1)
        (current-height P4 n2)
        (current-height P5 n3)
        (current-height P6 n1)

    )

    (:goal
        (and
            (available C1 M1)
            (available C3 M1)
        )
    )
)