module funciones

use mcf_tipos

public :: fun1

CONTAINS

function fun1(x) result(y1)

  real(kind=dp), intent(in) :: x
  real                      :: y1

  y1 = x**2.0*exp(-x)

end function fun1

end module funciones
