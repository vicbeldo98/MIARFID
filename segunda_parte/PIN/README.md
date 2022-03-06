# PIN

EJECUCIÓN DE LOS DIFERENTES PLANIFICADORES


FF

./PLANIFICADORES/FF/metric_ff -o dom_puerto.pddl -f prob_puerto.pddl


LPG

./PLANIFICADORES/LPG/lpg-td-1.0 -o dom_puerto.pddl -f prob_puerto.pddl -n 50 -out sol


OPTIC

./PLANIFICADORES/optic-clp dom_puerto.pddl prob_puerto.pddl 
