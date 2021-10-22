for pmut in 0.5
do
    for it in 300
    do
        for rep in 1 2 3 4 5
        do
            python3 chinese_postman_simpl.py --p_mutation $pmut --max_iterations $it >> results_$pmut-$it.txt
        done
    done
done