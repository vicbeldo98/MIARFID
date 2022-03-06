(define (problem puerto1_temp)
    
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
        ;;  total fuel used 
        (= (total-fuel-used) 0)

        ;;  slow speed definition
        (= (conveyor-slow-speed CT1) 1)
        (= (conveyor-slow-speed CT2) 1)

        ;; fast speed definition
        (= (conveyor-fast-speed CT1) 5)
        (= (conveyor-fast-speed CT2) 5)

        ;;  slow-burn definition
        (= (conveyor-slow-burn CT1) 1)
        (= (conveyor-slow-burn CT2) 1)

        ;;  fast-burn definition
        (= (conveyor-fast-burn CT1) 2)
        (= (conveyor-fast-burn CT2) 2)

        ;; fuel de la cinta
        (= (fuel CT1) 50)
        (= (fuel CT2) 50)
    

        (= (weight C1) 20)
        (= (weight C2) 20)
        (= (weight C3) 20)
        (= (weight C4) 20)
        (= (weight C5) 20)
        (= (weight C6) 20)
        (= (weight C7) 20)
        (= (weight C8) 20)

        (= (time-height n0) 1)
        (= (time-height n1) 0.75)
        (= (time-height n2) 0.5)
        (= (time-height n3) 0.25)
        (= (time-height n4) 0.15)

        (= (conveyor-length CT1) 15)
        (= (conveyor-length CT2) 25)

        (belong G1 M1)
        (belong G2 M2)

        (belong CT1 M1)
        (belong CT2 M2)

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

        (green C1)
        (green C5)
        (green C8)
        (no-green C7)
        (no-green C6)
        (no-green C4)
        (no-green C2)
        (no-green C3)

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

    (:metric minimize (total-time))
)