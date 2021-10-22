for type in 1 2 3
do
    for k in 0.05 0.1 0.8 0.99
        do
            for rep in 1 2 3
            do
                python3 chinese_postman_enfr_sim.py --k $k --max_iterations 800 --t_inicial 5000 --temp_type $type  >> res-$type-$k.txt
            done
        done
done