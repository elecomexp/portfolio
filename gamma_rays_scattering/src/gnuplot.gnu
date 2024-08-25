set terminal x11
set zero 1e-20
set surface
set xlabel "x"
set ylabel "y"
set zlabel "z"
splot "POSICION" using   1:  2:  3 with  points     
pause -1 "Return para continuar"
set terminal png enhanced
set output "grafico5.png"
replot
