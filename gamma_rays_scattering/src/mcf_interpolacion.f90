module m_interpoli_sp
!
! Polynomial interpolation
!
use mcf_tipos

public :: polint
interface polint
	module procedure polint_sp
end interface
private :: polint_sp

INTEGER, parameter, private  ::  NMAX = 30

CONTAINS  !==========================================================

SUBROUTINE POLINT_sp(XA,YA,N,X,Y,DY)
!
! Given arrays xa and ya, of length n, this routine computes
! the value at x of the interpolating polynomial of degree n-1
! which passes through the (x(i),y(i)) points.
! This value is returned in y, and dy contains an error estimate.
!
integer, intent(in)                       :: n
real(kind=sp), intent(in), dimension(:)   :: xa, ya
real(kind=sp), intent(in)                 :: X
real(kind=sp), intent(out)                :: y, dy

real(kind=sp)    ::  DEN,DIF,DIFT,HO,HP,W
integer :: I,M,NS

real(kind=sp), dimension(nmax)   ::  C, D     ! Could be automatic arrays

if (n>nmax) then
   print *, "Please increase nmax in polint"
   stop
endif

!
! Find the index of the closest table entry
!
NS = 1
DIF = ABS(X-XA(1))
DO I = 1,N
    DIFT = ABS(X-XA(I))
    IF (DIFT < DIF) THEN
        NS = I
        DIF = DIFT
    END IF

    C(I) = YA(I)
    D(I) = YA(I)
enddo
Y = YA(NS)
NS = NS - 1
DO M = 1, N-1
   DO I = 1, N-M
        HO = XA(I) - X
        HP = XA(I+M) - X
        W = C(I+1) - D(I)
        DEN = HO - HP
        IF (DEN == 0.0_sp) THEN
            print *,  "POLINT - DEN=0.0_sp"
            RETURN
        END IF

        DEN = W/DEN
        D(I) = HP*DEN
        C(I) = HO*DEN
   enddo
   IF ( 2*NS < (N-M) ) THEN
      DY = C(NS+1)
   ELSE
      DY = D(NS)
      NS = NS - 1
   END IF

   Y = Y + DY
enddo

END subroutine polint_sp

 
end module m_interpoli_sp

module m_interpoli_dp
!
! Polynomial interpolation
!
use mcf_tipos

public :: polint
interface polint
	module procedure polint_dp
end interface
private :: polint_dp

INTEGER, parameter, private  ::  NMAX = 30

CONTAINS  !==========================================================

SUBROUTINE POLINT_dp(XA,YA,N,X,Y,DY)
!
! Given arrays xa and ya, of length n, this routine computes
! the value at x of the interpolating polynomial of degree n-1
! which passes through the (x(i),y(i)) points.
! This value is returned in y, and dy contains an error estimate.
!
integer, intent(in)                       :: n
real(kind=dp), intent(in), dimension(:)   :: xa, ya
real(kind=dp), intent(in)                 :: X
real(kind=dp), intent(out)                :: y, dy

real(kind=dp)    ::  DEN,DIF,DIFT,HO,HP,W
integer :: I,M,NS

real(kind=dp), dimension(nmax)   ::  C, D     ! Could be automatic arrays

if (n>nmax) then
   print *, "Please increase nmax in polint"
   stop
endif

!
! Find the index of the closest table entry
!
NS = 1
DIF = ABS(X-XA(1))
DO I = 1,N
    DIFT = ABS(X-XA(I))
    IF (DIFT < DIF) THEN
        NS = I
        DIF = DIFT
    END IF

    C(I) = YA(I)
    D(I) = YA(I)
enddo
Y = YA(NS)
NS = NS - 1
DO M = 1, N-1
   DO I = 1, N-M
        HO = XA(I) - X
        HP = XA(I+M) - X
        W = C(I+1) - D(I)
        DEN = HO - HP
        IF (DEN == 0.0_dp) THEN
            print *,  "POLINT - DEN=0.0_dp"
            RETURN
        END IF

        DEN = W/DEN
        D(I) = HP*DEN
        C(I) = HO*DEN
   enddo
   IF ( 2*NS < (N-M) ) THEN
      DY = C(NS+1)
   ELSE
      DY = D(NS)
      NS = NS - 1
   END IF

   Y = Y + DY
enddo

END subroutine polint_dp

 
end module m_interpoli_dp

module m_spline_sp
!
! Spline interpolation
!
use mcf_tipos

public :: spline, splint   
interface spline
	module procedure spline_sp
end interface
interface splint
	module procedure splint_sp
end interface
private :: spline_sp, splint_sp

CONTAINS !==========================================================

SUBROUTINE SPLINE_sp(X,Y,N,Y2,YP1,YPN)
!
! Given arrays x and y of size n, this routine computes
! an array y2 holding information about the second derivative
! of the interpolating spline. YP1 and YPN, if present, are the
! requested values of the first derivative of the spline at the
! end points. If not given, a "natural" spline with zero second
! derivative at the extremes is constructed.
! The array y2 is needed to evaluate the spline, but it only needs
! to be computed once.
!
integer, intent(in)                          :: n
real(kind=sp), dimension(:), intent(in)  :: x, y
real(kind=sp), dimension(:), intent(out) :: y2
real(kind=sp), intent(in), optional      :: yp1, ypn

real(kind=sp)  ::  P,QN,SIG,UN
INTEGER            ::  I,K

real(kind=sp), parameter  :: zero = 0.0_sp, &
                                 half = 0.5_sp, &
                                 one  = 1.0_sp, &
                                 two  = 2.0_sp, &
                                 three= 3.0_sp, &
                                 six  = 6.0_sp

real(kind=sp), dimension(n)  ::   U    ! Automatic array

!--------------------------------------------------------
do i = 1, N-1
   if (x(i+1) - x(i) <= 0.0_sp) then 
           STOP " X ha de estar en orden creciente en spline"
   end if
enddo

IF (present(YP1)) THEN
    Y2(1) = -half
    U(1) = (three/ (X(2)-X(1)))* ((Y(2)-Y(1))/ (X(2)-X(1))-YP1)
ELSE
    Y2(1) = zero
    U(1) = zero
END IF

DO I = 2,N - 1
    SIG = (X(I)-X(I-1))/ (X(I+1)-X(I-1))
    P = SIG*Y2(I-1) + two
    Y2(I) = (SIG-one)/P
    U(I) = ( six * ((Y(I+1)-Y(I))/ (X(I+1)-X(I))- (Y(I)-Y(I-1))/ &
            (X(I)-X(I-1)))/ (X(I+1)-X(I-1))-SIG*U(I-1))/P
enddo
IF (present(YPN)) THEN
    QN = half
    UN = (three/(X(N)-X(N-1)))* (YPN - (Y(N)-Y(N-1))/ (X(N)-X(N-1)))
ELSE
    QN = zero
    UN = zero
END IF

Y2(N) = (UN-QN*U(N-1))/ (QN*Y2(N-1) + one)
DO K = N-1 , 1 , -1
    Y2(K) = Y2(K)*Y2(K+1) + U(K)
enddo

END subroutine spline_sp

SUBROUTINE SPLINT_sp(XA,YA,Y2A,N,X,Y)
!
! Given arrays xa and ya of size n, and an array y2a computed
! previously by routine spline, this routine computes the value
! at x of the interpolating spline. The value is returned in y.
!
integer, intent(in)                          :: n
real(kind=sp), dimension(:), intent(in)  :: xa, ya, y2a
real(kind=sp), intent(in)                :: x
real(kind=sp), intent(out)               :: y


real(kind=sp)                 ::  A,B,H
integer              ::  K,KHI,KLO

KLO = 1
KHI = N
do
   IF (KHI-KLO <= 1) then
      exit
   end if
   K = (KHI+KLO)/2
   IF (XA(K) > X) THEN
      KHI = K
   ELSE
      KLO = K
   END IF
enddo

H = XA(KHI) - XA(KLO)
IF (H == 0.0_sp) THEN
    print *, "Bad XA input."
    RETURN
END IF

A = (XA(KHI)-X)/H
B = (X-XA(KLO))/H
Y = A*YA(KLO) + B*YA(KHI) + ((A**3.0_sp-A)*Y2A(KLO)+  &
   (B**3.0_sp-B)*Y2A(KHI))* (H**2.0_sp)/6.0_sp

END subroutine splint_sp

end module m_spline_sp

module m_spline_dp
!
! Spline interpolation
!
use mcf_tipos

public :: spline, splint   
interface spline
	module procedure spline_dp
end interface
interface splint
	module procedure splint_dp
end interface
private :: spline_dp, splint_dp

CONTAINS !==========================================================

SUBROUTINE SPLINE_dp(X,Y,N,Y2,YP1,YPN)
!
! Given arrays x and y of size n, this routine computes
! an array y2 holding information about the second derivative
! of the interpolating spline. YP1 and YPN, if present, are the
! requested values of the first derivative of the spline at the
! end points. If not given, a "natural" spline with zero second
! derivative at the extremes is constructed.
! The array y2 is needed to evaluate the spline, but it only needs
! to be computed once.
!
integer, intent(in)                          :: n
real(kind=dp), dimension(:), intent(in)  :: x, y
real(kind=dp), dimension(:), intent(out) :: y2
real(kind=dp), intent(in), optional      :: yp1, ypn

real(kind=dp)  ::  P,QN,SIG,UN
INTEGER            ::  I,K

real(kind=dp), parameter  :: zero = 0.0_dp, &
                                 half = 0.5_dp, &
                                 one  = 1.0_dp, &
                                 two  = 2.0_dp, &
                                 three= 3.0_dp, &
                                 six  = 6.0_dp

real(kind=dp), dimension(n)  ::   U    ! Automatic array

!--------------------------------------------------------
do i = 1, N-1
   if (x(i+1) - x(i) <= 0.0_dp)  then
           STOP " X ha de estar en orden creciente en spline"
   end if
enddo

IF (present(YP1)) THEN
    Y2(1) = -half
    U(1) = (three/ (X(2)-X(1)))* ((Y(2)-Y(1))/ (X(2)-X(1))-YP1)
ELSE
    Y2(1) = zero
    U(1) = zero
END IF

DO I = 2,N - 1
    SIG = (X(I)-X(I-1))/ (X(I+1)-X(I-1))
    P = SIG*Y2(I-1) + two
    Y2(I) = (SIG-one)/P
    U(I) = ( six * ((Y(I+1)-Y(I))/ (X(I+1)-X(I))- (Y(I)-Y(I-1))/ &
            (X(I)-X(I-1)))/ (X(I+1)-X(I-1))-SIG*U(I-1))/P
enddo
IF (present(YPN)) THEN
    QN = half
    UN = (three/(X(N)-X(N-1)))* (YPN - (Y(N)-Y(N-1))/ (X(N)-X(N-1)))
ELSE
    QN = zero
    UN = zero
END IF

Y2(N) = (UN-QN*U(N-1))/ (QN*Y2(N-1) + one)
DO K = N-1 , 1 , -1
    Y2(K) = Y2(K)*Y2(K+1) + U(K)
enddo

END subroutine spline_dp

SUBROUTINE SPLINT_dp(XA,YA,Y2A,N,X,Y)
!
! Given arrays xa and ya of size n, and an array y2a computed
! previously by routine spline, this routine computes the value
! at x of the interpolating spline. The value is returned in y.
!
integer, intent(in)                          :: n
real(kind=dp), dimension(:), intent(in)  :: xa, ya, y2a
real(kind=dp), intent(in)                :: x
real(kind=dp), intent(out)               :: y


real(kind=dp)                 ::  A,B,H
integer              ::  K,KHI,KLO

KLO = 1
KHI = N
do
   IF (KHI-KLO <= 1) then
      exit
   end if
   K = (KHI+KLO)/2
   IF (XA(K) > X) THEN
      KHI = K
   ELSE
      KLO = K
   END IF
enddo

H = XA(KHI) - XA(KLO)
IF (H == 0.0_dp) THEN
    print *, "Bad XA input."
    RETURN
END IF

A = (XA(KHI)-X)/H
B = (X-XA(KLO))/H
Y = A*YA(KLO) + B*YA(KHI) + ((A**3.0_dp-A)*Y2A(KLO)+  &
   (B**3.0_dp-B)*Y2A(KHI))* (H**2.0_dp)/6.0_dp

END subroutine splint_dp

end module m_spline_dp

module mcf_interpoli
!
! Interpolacion polinomica
!
use m_interpoli_sp
use m_interpoli_dp

public

end module mcf_interpoli
module mcf_spline
!
! Spline interpolation
!

use m_spline_sp
use m_spline_dp

public

end module mcf_spline
