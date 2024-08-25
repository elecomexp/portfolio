MODULE CONSTANTES

  use mcf_tipos

  real(kind=dp), parameter, public :: m_e = 9.1093829140e-31
  real(kind=dp), parameter, public :: e_V = 1.6021765653e-19

END MODULE CONSTANTES

!==============================================================

MODULE ACELERADOR

  use mcf_tipos
  use constantes

  public :: acelerate

  CONTAINS

  subroutine acelerate(electron_volts,vel_electron)
     real(kind=dp), intent(in)  :: electron_volts
     real(kind=dp), intent(out) :: vel_electron
     real(kind=dp)              :: E
        E = electron_volts*e_V
        vel_electron = sqrt(2.0*E/m_e)
  end subroutine acelerate

END MODULE ACELERADOR

!==============================================================

PROGRAM CONDUCTIVIDAD

  use mcf_tipos
  use graph
  use constantes
  use acelerador

  real(kind=dp)                            :: recorrido_libre_medio, energy, vel_electron, anchura_muestra
  real(kind=dp)                            :: posicion_x, posicion_y, theta, x, tiempo
  integer(kind=dp)                         :: N, e_pasan, e_devueltos, i
  real(kind=dp), parameter                 :: pi = acos(-1.0)
  character(len=130), dimension(1)         :: dibujo
  integer, dimension(1)                    :: type

!  print *, "Introduzca la energia aplicada en electronvoltios"
!  read *, energy
!  call acelerate(energy,vel_electron)
!  print *, "Velocidad del electron:", vel_electron
!
!  print *, "Recorrido libre medio:"      
!  read *, recorrido_libre_medio
!
! PARA EL HELIO ES E-7 cm
!
!  print *, "Introduzca el numero de electrones que se lanzan"
!  read *, N
!
!  print *, "Anchura de la muestra de estudio"
!  read *, anchura_muestra

  energy = 3E+5!  
  call acelerate(energy,vel_electron)
  recorrido_libre_medio = 1E-5
  N = 100000
  anchura_muestra = 0.8

  posicion_x = 0.0
  posicion_y = 0.0
  e_pasan = 0
  e_devueltos = 0

  OPEN(unit=1, file="POSICION", status="replace", action="readwrite")
  WRITE(unit=1, fmt=*) posicion_x, tiempo
  DO i = 1, N
     DO
        call random_number(x)
        call random_number(theta)
        x = - recorrido_libre_medio*log(x)
        theta = 2.0*pi*theta
        posicion_x = posicion_x + x*cos(theta)
        posicion_y = posicion_y + x*sin(theta)
           print *, x, posicion_x, posicion_Y
        tiempo = tiempo + x/vel_electron
        if ( i==1 ) then
           WRITE(unit=1,fmt=*) posicion_x, tiempo
        end if
        if ( posicion_x>anchura_muestra ) then
           e_pasan = e_pasan + 1
           exit
        else if (posicion_x <= 0.0 ) then
           e_devueltos = e_devueltos + 1
           exit 
        end if
     END DO
  END DO
  CLOSE(unit=1)

  dibujo(1) = "POSICION"
  type(1) = 2
  CALL PLOT(dibujo,type=type)

  print *, "N, e_pasan, e_devueltos",  N, e_pasan, e_devueltos
  
END PROGRAM CONDUCTIVIDAD
