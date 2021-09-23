# Dado un vector de pesos w y unos datos a clasificar x,
# devuelve la clase correspondiente

# Variable de entrada
#     w = matriz(D+1,C)
function cstar=linmach(w,x)
  C=columns(w); cstar=1; max=-inf;
  for c=1:C
    g=w(:,c)'*x;
    if (g>max) max=g; cstar=c; endif; end
endfunction
