module mcf_tipos
!
! Define tipos estandar basados en la extension (para enteros)
! y en la precision (numero de cifras significativas) para reales.
!
! En un programa de calculo cientifico, lo que interesa es disponer
! de la precision o la extension requerida. El uso de las funciones
! intrinsecas "selected_int_kind" y "selected_real_kind" garantiza
! que podemos seleccionar el tipo adecuado sin conocer los detalles
! de la arquitectura del ordenador.
!
! Un programa tipico:
!---------------------------------
! program tipico
! use mcf_tipos
!
! real(kind=doble)    :: x
! integer(kind=byte)  :: n
!   ...
! end program tipico
!----------------------------------
! Algunos ordenadores no tienen cierto tipo (por ejemplo, el byte, o
! el long). En ese caso el compilador nos avisaria cuando declararamos
! una variable de ese tipo.
!
!=======================================================================
! Tipos enteros (se especifica la extension en potencias de 10)
!
integer, parameter, public :: int2   = selected_int_kind(2)    
integer, parameter, public :: int4   = selected_int_kind(4)  
integer, parameter, public :: int8   = selected_int_kind(8)  
integer, parameter, public :: int10  = selected_int_kind(10)   

integer, parameter, public :: byte  = int2
integer, parameter, public :: short = int4
integer, parameter, public :: int   = int8
integer, parameter, public :: long  = int10

!
! Tipos reales
!
integer, parameter, public :: single = selected_real_kind(6) 
integer, parameter, public :: double = selected_real_kind(14)
!
! Otros nombres utiles para los tipos
!
integer, parameter, public :: sencillo = single
integer, parameter, public :: doble = double
!
integer, parameter, public :: sp = single
integer, parameter, public :: dp = double

end module mcf_tipos
