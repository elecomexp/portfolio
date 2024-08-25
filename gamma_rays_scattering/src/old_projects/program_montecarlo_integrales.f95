program integrales_montecarlo

use mcf_tipos
use funciones

real(kind=dp)       :: x_random, y_random
real(kind=dp)       :: solucion 
integer             :: i, dentro, iteraciones

iteraciones = 90000000
dentro = 0

lander: do i = 1, iteraciones
  
  call random_number(x_random)
  call random_number(y_random)

  x_random = x_random*2.0 - 1.0    ! ASI RECORREMOS VALORES PARA x_random DESDE -1 HASTA 1
  y_random = y_random*8.0          ! QUE ES EL INTERVALO EN EL QUE QUEREMOS INTEGRAR, Y PARA
                                   ! y_random NOS ASEGURAMOS QUE SEA MAYOR QUE EL MAXIMO DE 
                                   ! LA FUNCION EN ESE INTERVALO


  if ( y_random <= fun1(x_random) ) then
    dentro = dentro + 1
  end if

end do lander

solucion =  16*real(dentro, kind=dp) / real(iteraciones, kind=dp)    ! POR 5 PORQUE ES EL AREA DEL CUADRANTE EN EL QUE TRABAJAMOS
print *, "Solucion", solucion

end program integrales_montecarlo
