(
    define (problem puerto1)
    
    (:domain puerto)
    
    (:objects 
        M1 M2 - muelle
        P1 P2 P3 P4 P5 P6 - pila
        C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 - contenedor
        G1 G2 - grua
        CT1 CT2 - cinta_transporte
    )

    (:init
        (belong G1 M1)
        (belong G2 M2)

        (belong CT1 M1)
        (belong CT2 M2)

        (pick CT2 M1)
        (pick CT1 M2)

        (attached P1 M1)
        (attached P2 M1)
        (attached P3 M1)
        (attached P4 M2)
        (attached P5 M2)
        (attached P6 M2)

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

        (disponible C7 M1)
        (disponible C1 M1)
        (disponible C10 M1)
        (disponible C11 M1)
        (disponible C8 M2)
        (disponible C2 M2)
        (disponible C6 M2)

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
    )

    (:goal
        (and
            (disponible C3 M1)
            (disponible C4 M1)
            (disponible C7 M1)
        )
    )
)