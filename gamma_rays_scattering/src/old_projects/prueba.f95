program prue

real :: x, y
integer :: i

do i = 1, 20
  call random_number(x)
  call random_number(y)
  print *, x, y
end do

end program prue
