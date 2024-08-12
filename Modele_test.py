from pycsp3 import *

x=Var(dom=range(0,5))
y=Var(dom=range(0,4))
z=Var(dom=range(0,3))
res=Var(dom=range(0,20))

timeout_sol_inter=0
variable_heuristique="WdegOnDom"
inverse_heuristique=False
Value_ordering_heuristique=None
variante_var_heuristique="CACD"

option_ACE=f"-t={int(timeout_sol_inter)}s" if timeout_sol_inter>0 else ""
option_ACE+=f" {f"-varh={variable_heuristique}" if variable_heuristique is not None else ""}"
option_ACE+=f" {"-anti_varh" if inverse_heuristique else ""}"
option_ACE+=f" {f"-valh={Value_ordering_heuristique}" if Value_ordering_heuristique else ""}"
option_ACE+=f" {f"-wt={variante_var_heuristique}" if variante_var_heuristique else ""}"

satisfy((x+y+z)==res)
maximize(res)

solver_verbose=-1

nombre_solution=ALL

resultat_recherche=solve(verbose=solver_verbose,options=option_ACE,sols=nombre_solution)

print(resultat_recherche)
if resultat_recherche is SAT or resultat_recherche is OPTIMUM is not UNSAT:
        print(f"Nombre de solutions: {n_solutions()} pour le petit modele" )
        boundmax=bound()
        for numero_solution in range(n_solutions()):
            x_var=values(x, sol=numero_solution)
            y_var=values(y, sol=numero_solution)
            z_var=values(z, sol=numero_solution)
            res_var=values(res, sol=numero_solution)
            print(x_var," | ",y_var," | ",z_var," | ",res_var)
