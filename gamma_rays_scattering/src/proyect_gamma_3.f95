MODULE CONSTANTES

  use mcf_tipos

  real(kind=dp), parameter, public :: m_e = 9.1093829140E-31            ! [Kg]
  real(kind=dp), parameter, public :: e_V = 1.6021765653E-19            ! [J]
  real(kind=dp), parameter, public :: c = 299729458.0                   ! [m/s]
  real(kind=dp), parameter, public :: r_e = 2.8179E-15                  ! [m]
  real(kind=dp), parameter, public :: pi = acos(-1.0)
  real(kind=dp), parameter, public :: N_A = 6.02214E23                  ! [mol**-1]
  
END MODULE CONSTANTES

!=================================================================

MODULE KLEIN_NISHINA

  use mcf_tipos
  use constantes

  public :: prob_distrib_theta, seccion_eficaz

  CONTAINS

  function prob_distrib_theta(gamma,theta) result(P_theta)
     real(kind=dp), intent(in) :: gamma, theta
     real(kind=dp)             :: P_theta_1, P_theta_2, P_theta_3
     real(kind=dp)             :: P_theta
        P_theta_1 = r_e**2.0_dp / 2.0_dp / (1.0_dp + gamma*(1.0_dp-cos(theta)))**2.0_dp
        P_theta_2 = (1.0_dp + cos(theta)**2.0_dp)
        P_theta_3 = ( gamma**2.0_dp*(1.0_dp-cos(theta))**2.0_dp  ) / ( 1.0_dp+gamma*(1.0_dp-cos(theta)) )
        P_theta = ( P_theta_1*(P_theta_2+P_theta_3)  )*2.0_dp*pi*sin(theta)
  end function prob_distrib_theta


  subroutine seccion_eficaz(gamma,Z,sigma)
     real(kind=dp), intent(in)    :: gamma
     integer(kind=dp), intent(in) :: Z
     real(kind=dp), intent(out)   :: sigma
     real(kind=dp)                :: sigma_1, sigma_2, sigma_3, sigma_4, sigma_KN
        sigma_1 = (2.0_dp*(1.0_dp+gamma))/(1.0_dp+2.0_dp*gamma) - (log(1.0_dp+2.0_dp*gamma))/(gamma)
        sigma_2 = (1.0_dp+gamma)/(gamma*2.0_dp)*sigma_1
        sigma_3 = log(1.0_dp+2.0_dp*gamma)/(2.0_dp*gamma)
        sigma_4 = (1.0_dp+3.0_dp*gamma)/((1.0_dp+2.0_dp*gamma )**2.0_dp)
        sigma_KN = 2.0_dp*pi*r_e**2.0_dp*(sigma_2 + sigma_3 - sigma_4)
        sigma = real(Z,kind=dp)*sigma_KN
  end subroutine seccion_eficaz
  
END MODULE KLEIN_NISHINA

! =================================================================

MODULE ANGULOS_RANDOM

  use mcf_tipos
  use constantes
  use klein_nishina
  
  public :: angulos                  ! PHI Y THETA SON LOS ANGULOS DISPERSADOS

  CONTAINS

  subroutine angulos(gamma, phi, theta)
     real(kind=dp), intent(in)  :: gamma
     real(kind=dp), intent(out) :: phi, theta 
     real(kind=dp)              :: p_de_theta
        call random_number(phi)
        phi = 2.0_dp*pi*phi                  
        DO
           call random_number(theta)
           theta = theta*pi
           call random_number(p_de_theta)
           p_de_theta = p_de_theta*1E-28_dp
           IF ( p_de_theta <= prob_distrib_theta(gamma,theta) ) then
              exit
           END IF
        END DO
  end subroutine angulos

END MODULE ANGULOS_RANDOM

!=================================================================

MODULE ENERGIA_UMBRAL

  use mcf_tipos
  use constantes

  public :: umbral
  
  CONTAINS

  subroutine umbral(Z,E_umbral)
     integer(kind=dp), intent(in) :: Z
     real(kind=dp), intent(out)   :: E_umbral
     IF (Z>0 .and. Z<=20) then
        E_umbral = (0.06E+6_dp)*e_V
     ELSE IF (Z>20 .and. Z<=30) then
        E_umbral = (0.15E+6_dp)*e_V
     ELSE IF (Z>30 .and. Z<=40) then
        E_umbral = (0.2E+6_dp)*e_V
     ELSE IF (Z>40 .and. Z<=50) then
        E_umbral = (0.25E+6_dp)*e_V
     ELSE IF (Z>50 .and. Z<=60) then
        E_umbral = (0.3E+6_dp)*e_V
     ELSE IF (Z>60 .and. Z<=70) then
        E_umbral = (0.5E+6_dp)*e_V
     ELSE IF (Z>70 .and. Z<=80) then
        E_umbral = (0.6E+6_dp)*e_V
     ELSE IF (Z>80 .and. Z<=90) then
        E_umbral = (0.7E+6_dp)*e_V
     ELSE 
        print *, "Este programa no trabaja con Z mayores de 90"
        stop
     END IF
  end subroutine umbral

END MODULE ENERGIA_UMBRAL

!=================================================================

PROGRAM GAMMA_SCATT

  use angulos_random
  use constantes
  use energia_umbral
  use graph
  use klein_nishina
  use mcf_tipos
 

  real(kind=dp)                    :: theta, theta_vieja, theta_nueva, theta_inicial
  real(kind=dp)                    :: phi, phi_vieja, phi_nueva, phi_inicial
  real(kind=dp)                    :: s, r, grosor_muestra, sigma
  real(kind=dp)                    :: E_inicial, E_umbral, E_vieja, E_nueva, gamma
  integer(kind=dp)                 :: Z, i, numero_fotones, puntos, incidencia
  real(kind=dp)                    :: rho, Ma, n
  real(kind=dp)                    :: x_nueva, x_vieja, y_vieja, y_nueva, z_vieja, z_nueva
  integer(kind=dp)                 :: gamma_traspasado, gamma_devuelto, gamma_absorbido
  character(len=130), dimension(1) :: dibujo
  integer, dimension(1)            :: type

  print *, "Introduzca: Z, masa atomica(gr*mol**-1), y densidad(gr*cm**-3)"
  read *, Z, Ma, rho

  print *, "Anchura de la muestra(m)"
  read *, grosor_muestra

  print *, "Pulse ""1"" si desea una incidencia normal al material. ", &
           "Pulse ""2"" si desea ajustar el angulo de incidencia"
  read *, incidencia
  IF (incidencia==1) then
     phi_inicial = 0.0_dp
     theta_inicial = pi/2.0_dp
  ELSE IF (incidencia==2) then
     print *, "Introduca los angulos phi y theta con los que incide el rayo al material (en grados)"
     read *, phi_inicial, theta_inicial
     phi_inicial = phi_inicial*pi/180.0
     theta_inicial = theta_inicial*pi/180.0
  END IF

  print *, "Introduzca el numero de fotones que se van a lanzar"
  read *,  numero_fotones

  print *, "Pulse ""1"" si desea ver los puntos en los que choca cada foton. ", &
           "Pulse cualquier otro numero si no lo desea"
  read *, puntos

  E_inicial = (1.1E+6_dp)*e_V 
  call umbral(Z,E_umbral)

  gamma_traspasado = 0
  gamma_devuelto = 0
  gamma_absorbido = 0

  n = (rho*N_A*real(Z,kind=dp)/Ma)*1.0E+6_dp           ! DENSIDAD DE ELECTRONES EN m**-3
!  print *, "DENSIDAD DE ELECTRONES", n

 
! ================================== !
! ==== ALGORITMO DEL TRANSPORTE ==== !
! ================================== !

   DO i = 1, numero_fotones

!     print *, "!==================================================================================!"
!     print *, "!=========================== NUEVO FOTON DISPARADO ================================!"
!     print *, "!==================================================================================!"

     E_vieja = E_inicial                         ! ENERGIA INCIDENTE EN JULIOS
     phi_vieja = phi_inicial
     theta_vieja = theta_inicial
     
     IF (puntos==1) then
       OPEN(unit=1,file="POSICION",status="replace",action="readwrite")
     END IF

     gamma = E_vieja/(m_e*c**2.0_dp)

!     print *, "ENERGIA VIEJA, GAMMA:", E_vieja, gamma

     call seccion_eficaz(gamma,Z,sigma)           ! ==== CROSS SECTION ==== !
!     print *, "SIGMA", sigma

     call random_number(r)
     s = -log(r)/(n*sigma)                        ! ==== LONGITUD DEL MOVIMIENTO RANDOM ==== !
!     PRINT *, "S", s

     x_vieja = s*sin(theta_vieja)*cos(phi_vieja)
     y_vieja = s*sin(theta_vieja)*sin(phi_vieja)
     z_vieja = s*cos(theta_vieja)
!     print *, "POSCION X, Y, Z", x_vieja, y_vieja, z_vieja
   
     IF (puntos==1) then
        WRITE(unit=1,fmt=*) x_vieja, y_vieja, z_vieja
     END IF

     IF (x_vieja >= grosor_muestra) then
        gamma_traspasado = gamma_traspasado + 1
!        print *, "GAMMA TRASPASADO"
     ELSE IF (x_vieja <= 0.0) then
        print *, "Las particulas no estan entrando en el material. Introduce otros angulos de incidencia"
        stop
     ELSE                              
        DO                                                      !==== COMPTON====!
           call angulos(gamma, phi, theta)
           E_nueva = E_vieja / (1.0_dp + gamma*(1.0_dp-cos(theta)))
!           print *, "ENERGIA NUEVA, PHI, THETA:", E_nueva, phi, theta
      
           IF (E_nueva < E_umbral) then
              gamma_absorbido = gamma_absorbido + 1           
!              print *, "==== GAMMA ABSORBIDO ===="
              exit
           ELSE
              gamma = E_nueva / (m_e*c**2.0)
              call seccion_eficaz(gamma,Z,sigma)                ! CROSS SECTION
!              print *, "SIGMA", sigma
 
              call random_number(r)
              s = -log(r)/(n*sigma)     
!              PRINT *, "S2", s

              theta_nueva = (cos(theta_vieja)*cos(theta)) + (sin(theta_vieja)*sin(theta)*sin(phi))
!              print *, "DENTRO DEL PARENTESIS THETA", theta_nueva
              THETA_NUEVA = acos(theta_nueva)

              DO
                 phi_nueva = sin(theta)*sin(phi)/sin(theta_nueva)
!                 print *, "DENTRO DEL PARENTESIS PHI", phi_nueva
                 IF (phi_nueva<1.0_dp .and. phi_nueva>-1.0_dp) then
                    exit
                 ELSE
                    call random_number(r)
                    phi = 2.0_dp*pi*r
                 END IF
              END DO
             
!              print *, "DENTRO DEL PARENTESIS PHI", phi_nueva
              PHI_NUEVA = asin(phi_nueva) + phi_vieja

!              print *, "TETA NUEVA, PHI NUEVA", theta_nueva, phi_nueva
!              print *, "s,sin(theta),cos(theta):", s, sin(theta_nueva), cos(theta_nueva)
!              print *, "sin(phi),cos(phi):",  sin(phi_nueva), cos(phi_nueva)

              x_nueva = (s*sin(theta_nueva)*cos(phi_nueva)) + x_vieja
              y_nueva = (s*sin(theta_nueva)*sin(phi_nueva)) + y_vieja
              z_nueva = (s*cos(theta_nueva)) + z_vieja
!              print *, "POSCION X, Y, Z", x_nueva, y_nueva, z_nueva

             IF (puntos==1) then
                WRITE(unit=1, fmt=*) x_nueva, y_nueva, z_nueva
             END IF
 
              IF (x_nueva >= grosor_muestra) then
                 gamma_traspasado = gamma_traspasado + 1
!                 print *, "GAMMA TRASPASADO"
                 exit
              ELSE IF (x_nueva < 0.0) then
                 gamma_devuelto = gamma_devuelto + 1
!                 print *, "GAMMA DEVUELTO"
                 exit
              ELSE 
                 x_vieja = x_nueva
                 y_vieja = y_nueva
                 z_vieja = z_nueva
                 E_vieja = E_nueva
                 theta_vieja = theta_nueva
                 phi_vieja = phi_nueva
              END IF
           END IF
        END DO     
     END IF
     IF (puntos==1) then
        CLOSE(unit=1)
        dibujo(1) = "POSICION"
        type(1) = 5
        CALL PLOT(dibujo, type=type)
     END IF
 
  END DO

  print *, "======================= FIN DEL PROGRAMA ======================="
  print *, "Grosor de la muestra:", grosor_muestra, "metros"
  print *, "Z, Ma(gr*mol**-1), rho(gr*cm**-3) del material de estudio:", Z, ",", Ma, ",", rho
  print *, "Fotones absorbidos, traspasados y devueltos:", gamma_absorbido, ",", gamma_traspasado, ",", gamma_devuelto
  print *, "Coeficiente de absorción:", real(gamma_absorbido,kind=dp)/real(numero_fotones,kind=dp)
  print *, "Coeficiente de transmision:", real(gamma_traspasado,kind=dp)/real(numero_fotones,kind=dp)
  print *, "Coeficiente de retrodispersion:", real(gamma_devuelto,kind=dp)/real(numero_fotones,kind=dp)


END PROGRAM GAMMA_SCATT
