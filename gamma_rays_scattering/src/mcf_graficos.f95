!*************************************************************************************************
!Esta es una interface a GnuPlot (algunas extensiones de la version 4 estan marcadas aunque no se 
!usen en el servidos) que puede usarse desde cualquier programa.
! 
!
!Los parametros de entrada son:
!
!Un vector que contiene los nombres de los ficheros que se desean dibujar juntos.
!
!Tres vectores que contienen las columnas a dibujar. Asi x(1)=1,y(1)=2,z(1)=3 indicaria una
!grafica tridimensional en la que x, y, z son las tres primeras columnas almacenadas. Si no se
!incluye ninguna de ellas, la subrutina decide el tipo de dibujo segun la estructura del fichero:
!un fichero con solo 2 columnas sera representado asumiendo que los valores de x e y corresponden
!a las columnas de datos 1 y 2 respectivamente. Si el fichero tiene 3 o mas columnas, la 
!representacion sera tridimensional asumiendo que x, y, z son las tres primera columnas del 
!fichero.
!
!Un vector de dimension 3 conteniendo las etiquetas de los ejes. Por defecto son "x", "y" y "z".
!
!Un vector cuyos valores indican si la correspondiente grafica se realiza con puntos (1), 
!lineas (2), puntos y lineas (3)o barras de error (4). Por defecto la grafica se realiza con puntos.
!
!Una variable que indica el formato en que se guarda una copia del grafico. Los posibles valores 
!son: 1 (png) o 2 (postscript). Es valor por defector es 1 (png). El nombre del fichero que 
!contiene el grafico es grafico<n>.png o grafico<n>.ps donde <n> es un número correlativo a partir
!de 1.
!
!El selector del tipo de grafico tridimensional: superficie (1), mapa de contorno (2) , ambos (3).
!El valor por defecto es 1 (superficie).
!
!Los datos recibidos por esta subrutina son discretos y si se require un mapa de contorno o una
!superficie dibujada con lineas, debe hacerse un enrejado (interpolacion) con los puntos. El
!muestreo es controlado por ngrid. Por defecto es 20.
!
!El número de lineas en los mapas de contorno se controla con nlevels. El defecto es 10.
!
!Min_x (max_x) fija el valor minimo (maximo) para realizar graficos bidimensionales en la misma escala.
!Se reuiqren ambos valores (no hay valores por defecto).
!
!Min_value (max_value) fija el valor de y o z (minimos) maximos para realizar dibujos en la 
!misma escala. Se reuiqren ambos valores (no hay valores por defecto)
!
!Slides (0/n) inhibe la parada tras cada plot. Por defecto no está activado (0). n indica los segundos
!entre graficos (no menor de 2.0 segundos).
!
!Ratio es un parametro opcional con valores 0, 1 que hace iguales los ejes x e y. Por defecto
!su valor es 0.
!El control de errores no es en absoluto exhaustivo y por tanto pueden obtenerse resultados 
!imprevisibles.
!*************************************************************************************************
module graph
use mcf_tipos
public  :: plot
private :: test_file,wait,define_command
contains

! very dirty trick!!!. Indirect call to gnuplot allows a direct time control
subroutine define_command()
logical  :: file_exists
!character(len=*), parameter :: call_gnu="gnuplot -geometry 1260x742+0+0 -background white ""gnuplot.gnu"""
character(len=*), parameter :: call_gnu="gnuplot -geometry +0+0 -background white ""gnuplot.gnu"""

inquire(file=".gnu",exist=file_exists)

if (.not. file_exists) then
	open(unit=666,file=".gnu",status="replace",position="rewind",action="write")
	write(unit=666,fmt="(a)") call_gnu
	close(unit=666)
end if

call system("chmod a+x .gnu")

end subroutine define_command

subroutine wait(delta) 
real(kind=sp),intent(in) :: delta
real(kind=sp)            :: initial_time,time

call cpu_time(initial_time)

do
        call cpu_time(time)
        if ((time-initial_time)>=delta) then
                exit
        end if
end do

end subroutine wait

subroutine test_file (file,plot_dim) 
character(len=*),intent(in)             :: file
integer,intent(out)                     :: plot_dim
integer                                 :: i,char,flag_blank,status
character(len=*), parameter             :: blank=" "
character(len=1)                        :: test
real(kind=sp),dimension(:),allocatable  :: test_number
logical                                 :: file_exists

! test_file is very naive. it is assumed that the file contains only numbers
! and blanks between them. A simple checks is carried out about the type
! of comments allowed by GnuPlot...
! negative status means file does not exist or unexpected record type

plot_dim = 0
flag_blank = 0
char = 0

!
! Check if file exists

inquire (file=trim(file),exist=file_exists)

if (file_exists) then

        open(unit=999,file=trim(file),status="old",action="read",position="rewind")

        do
                char = char+1

                read(unit=999,iostat=status,fmt="(a)",advance="no") test

                if (status<0) then
                        exit
                else
! comments allowed by GnuPlot
                        if (char==1.and.(test=="#".or.test=="!")) then
! skip this line
                                read(unit=999,iostat=status,fmt="(/)")

                                if (status<0) then
                                        exit
                                end if
! put the file pointer at the beginning of the line
                                backspace(unit=999)
! start reading again
                                char = 0
                                cycle
                        end if

                        if (test==blank.and.flag_blank==0)  then
                                flag_blank=1
                        else if ((test/=blank.and.flag_blank==1).or.(test/=blank.and.char==1)) then
                                flag_blank=0
                                plot_dim=plot_dim+1

                        end if
                end if

        end do
end if

if (plot_dim>=2) then
! are really numbers? (we check only one line!)
        allocate (test_number(plot_dim))
        backspace(unit=999)

        read(unit=999,iostat=status,fmt=*) (test_number(i),i=1,plot_dim)

        if (status/=0) then
                plot_dim = 0
        end if
        deallocate (test_number)
end if

close(unit=999)

end subroutine test_file

subroutine plot (file,x,y,z,axeslabel,type,output,surface,ngrid,nlevels,min_x,max_x,min_value,max_value,slide,ratio)

character(len=*),intent(in),dimension(:)               :: file
integer,intent(in),optional,dimension(:)               :: x,y,z
integer,intent(in),optional,dimension(:)               :: type
character(len=*),intent(in),optional,dimension(:)      :: axeslabel
integer,intent(in),optional                            :: output,surface,ngrid,nlevels,ratio
real(kind=sp),intent(in),optional                      :: min_x,max_x,min_value,max_value,slide

integer,parameter          :: x_default=1,y_default=2,z_default=3
character(len=*),parameter :: axeslabel_x_default="x",axeslabel_y_default="y",axeslabel_z_default="z"
character(len=*),parameter,dimension(1:4) :: plot_type= (/" points     "," lines      " &
									   ," linespoints"," errorbars  "/)
!*************************************************************************************************
! GnuPlot 4: use the next instruction instead the driver png.
!
!character(len=*),parameter,dimension(1:2) :: output_type= (/"jpeg      ","postscript"/)
character(len=*),parameter,dimension(1:2) :: output_type= (/"png       ","postscript"/)
!*************************************************************************************************
! GnuPlot 4: use the next instruction instead the driver and extension png.
!
!character(len=*),parameter,dimension(1:2) :: output_extension=(/"jpg","ps "/)
character(len=*),parameter,dimension(1:2) :: output_extension=(/"png","ps "/)
integer,parameter            :: type_default=1,output_default=1,surface_default=1, &
                                grid_default=20, levels_default=10, grid_max=100, levels_max=50
real(kind=sp),parameter      :: slide_default=2.0
integer                      :: i,digits,count_digits,dim,file_count,x_column,y_column,z_column
integer                      :: plot_dim_check,plot_dim,plot_typ,output_typ,surface_typ,grid,levels
real(kind=sp)                :: slides
character(len=6)             :: format
character(len=9)             :: with
character(len=50)            :: axeslabel_x,axeslabel_y,axeslabel_z
integer,save                 :: call_count=0


! count the number of calls

call_count = call_count+1
count_digits = call_count
digits=1

do
count_digits = count_digits/10
if (count_digits>0) then
        digits=digits+1
else
        exit
end if
end do

write(unit=format,fmt="(a,i0,a)") "i",digits,",3a)"

if (.not. present(output)) then
        output_typ = output_default
else
        output_typ = output
end if

if (.not. present(surface)) then
        surface_typ = surface_default
else
        surface_typ = surface
end if

if (.not. present(ngrid)) then
        grid = grid_default
else
        grid = ngrid
        if (grid>grid_max) then
                grid = grid_max
	end if
end if

if (.not. present(nlevels)) then
        levels = levels_default
else
        levels = nlevels
        if (levels>levels_max) then
                levels = levels_max
	end if
end if

if (.not. present(slide).or.slide==0.0) then
        slides = 0.0
else
	call define_command()
        if (slide<slide_default) then
                slides = slide_default
        else
                slides = slide
        end if
end if

axeslabel_x = axeslabel_x_default
axeslabel_y = axeslabel_y_default
axeslabel_z = axeslabel_z_default

open (unit=666,file="gnuplot.gnu",status="replace",action="readwrite")

! some header
!*************************************************************************************************
! GnuPlot 4 windows: use the next instruction instead the old terminal x11
!
!write (unit=666,fmt="(a)") "set terminal windows color enhanced"
write (unit=666,fmt="(a)") "set terminal x11" 
!*************************************************************************************************

if (present(ratio).and.ratio==1)then
	write (unit=666,fmt="(a)") "set size ratio 1" 
end if  

write (unit=666,fmt="(a)") "set zero 1e-20"   

dim = size(file)
file_count = 0

main_do: do i=1,dim

! input check

        call test_file(file(i),plot_dim_check)

        if (plot_dim_check<2) then                
                print *, "El fichero ",i," no puede dibujarse"
                cycle main_do
        else
                plot_dim = 2
                if (plot_dim_check>=3) then
                        plot_dim = 3
                end if
                file_count = file_count+1
        end if

        x_column = x_default
        y_column = y_default
        z_column = z_default
        plot_typ = type_default

        if (present(x) .and. present(y)) then
                         
                if (.not. present(z)) then
!2-dimensional plot
                        plot_dim = 2

                        if (x(i)>plot_dim_check.or.y(i)>plot_dim_check) then

                                print *, "Selector de columnas inconsistente"
                                stop

                        end if

                        if (x(i)>=0) then
                                x_column=x(i)
                        end if

                        if (y(i)>=0) then
                                y_column=y(i)
                        end if
                 else
                        plot_dim = 3

                        if (plot_dim>plot_dim_check) then
                                print *,"El fichero ",trim(file(i))," solo tiene dos columnas"
                                stop
                        end if

                        if (z(i)>plot_dim_check) then

                                print *, "Selector de columnas inconsistente"
                                stop

                        end if

                        if (z(i)>=0) then
                                z_column=z(i)
                        end if

                 end if
        end if

!plot type: 1 (points), 2 (lines), 3 (linespoints), 4 (errorbars)

        if (present(type).and.type(i)<=4.and.type(i)>=1) then
                 plot_typ=type(i)
        end if

	  if (plot_typ == 4 .and. plot_dim_check < 3) then

	  	print *, "Imposible dibujar las barras de error. Solo hay dos columnas"
		stop

	  else if (plot_typ == 4 .and. plot_dim == 3) then

		print *, "No es posible dibujar barras de error en graficas tridimensionales"
		stop
	
	  end if

!we have everything

        if (plot_dim == 2) then

		     if (plot_typ == 4) then

				with = " :3 with"
		     else

				with = " with"

		     end if

                 if (file_count == 1) then

                        if (present(axeslabel)) then
                                axeslabel_x = axeslabel(1)
                                axeslabel_y = axeslabel(2)
                        end if

                        write(unit=666,fmt="(3a)") "set xlabel """,trim(axeslabel_x),""""
                        write(unit=666,fmt="(3a)") "set ylabel """,trim(axeslabel_y),""""

                        if (present(min_x).and.present(max_x).and. &
                            present(min_value).and.present(max_value)) then
                                write(unit=666,advance="no", &
                                      fmt="(a,f0.3,a,f0.3,a,f0.3,a,f0.3,3a,i3,a,i3,2a)") &
                                      "plot [",min_x,":",max_x,"] [",min_value,":",max_value,"]""", &
                                      trim(file(i)),""" using ",x_column,":", &
                                      y_column,trim(with), plot_type(plot_typ)
          		else if (present(min_value).and.present(max_value)) then
                  		write(unit=666,advance="no", &
                        	      fmt="(a,f0.3,a,f0.3,3a,i3,a,i3,2a)") &
                                      "plot [] [",min_value,":",max_value,"] """, &
                                      trim(file(i)),""" using ",x_column,":", &
                                      y_column,trim(with), plot_type(plot_typ)
                        else if (present(min_x).and.present(max_x)) then
                                write(unit=666,advance="no", &
                                      fmt="(a,f0.3,a,f0.3,3a,i3,a,i3,2a)") &
                                      "plot [",min_x,":",max_x,"] [] """, &
                                      trim(file(i)),""" using ",x_column,":", &
                                      y_column,trim(with), plot_type(plot_typ)
                        else
                                write(unit=666,advance="no", &
                                      fmt="(3a,i3,a,i3,2a)") &
                                      "plot """,trim(file(i)),""" using ",x_column, &
                                      ":",y_column,trim(with), plot_type(plot_typ)
                        end if

                 else
                        write(unit=666,advance="no",fmt="(3a,i3,a,i3,2a)") &
                              ",""",trim(file(i)),""" using ",x_column,":",y_column,trim(with), &
                              plot_type(plot_typ)
                 end if

        else
                 if (file_count == 1) then

                        if (present(axeslabel)) then
                                axeslabel_x = axeslabel(1)
                                axeslabel_y = axeslabel(2)
                                axeslabel_z = axeslabel(3)
                        end if

                        if (plot_typ/=1.or.surface_typ>=2) then
!*************************************************************************************************
                                if (grid/=0) then
! GnuPlot 4 windows: use the next instruction instead the old set grid
!
                                        write(unit=666,fmt="(a,i3,a,i3)") "set dgrid ",grid,",",grid
!                                       write(unit=666,fmt="(a,i3,a,i3)") "set dgrid3d ",grid,",",grid
                                        write(unit=666,fmt="(a)") "set hidden3d"
                                end if
                                write(unit=666,fmt="(a,i3)") "set cntrparam levels ",levels
!                               write(unit=666,fmt="(a)") "set isosamples 101,101"
!                               write(unit=666,fmt="(a)") "set samples 61,61"
                        end if
                        write(unit=666,fmt="(a)") "set surface"
                        write(unit=666,fmt="(3a)") "set xlabel """,trim(axeslabel_x),""""
                        write(unit=666,fmt="(3a)") "set ylabel """,trim(axeslabel_y),""""
                        write(unit=666,fmt="(3a)") "set zlabel """,trim(axeslabel_z),""""

                        select case (surface_typ)
                        case (2)
!*************************************************************************************************
! GnuPlot 4: use the next instruction instead the old set nosurface
!
                                write(unit=666,fmt="(a)") "unset surface"
!                               write(unit=666,fmt="(a)") "set nosurface"
                                write(unit=666,fmt="(a)") "set contour"
!*************************************************************************************************
! GnuPlot 4: use the next instruction instead the old set noclabel
!
                                write(unit=666,fmt="(a)") "unset clabel"
!                               write(unit=666,fmt="(a)") "set noclabel"
!*************************************************************************************************
! GnuPlot 4: use the next instruction instead the old set nozlabel
!
!                               write(unit=666,fmt="(a)") "unset zlabel"
!                               write(unit=666,fmt="(a)") "set nozlabel"
!*************************************************************************************************
! GnuPlot 4: use the next instruction instead the old set nozticks
!
                                write(unit=666,fmt="(a)") "unset ztics"
!                               write(unit=666,fmt="(a)") "set noztics"
!*************************************************************************************************
! GnuPlot 4: use the next instruction instead the old set view
!
                                write(unit=666,fmt="(a)") "set view map"
!                               write(unit=666,fmt="(a)") "set view 0,0"
                        case (3)
!*************************************************************************************************
! GnuPlot 4: use the next instruction instead the old set noclabel
!
                                write(unit=666,fmt="(a)") "unset clabel"
!                               write(unit=666,fmt="(a)") "set noclabel"
                                write(unit=666,fmt="(a)") "set contour base"
                        end select

                        if (present(min_value).and.present(max_value)) then
                                write(unit=666,advance="no", &
                                      fmt="(a,f0.3,a,f0.3,3a,i3,a,i3,a,i3,2a)") &
                                      "splot [][][",min_value,":",max_value,"] """, &
                                      trim(file(i)),""" using ",x_column,":",y_column, &
                                      ":",z_column," with ", plot_type(plot_typ)
						
                        else
                                write(unit=666,advance="no", &
                                      fmt="(3a,i3,a,i3,a,i3,2a)") &
                                      "splot """, trim(file(i)),""" using ",x_column, &
                                      ":",y_column, ":",z_column," with ", &
                                      plot_type(plot_typ)
                        end if
                 else
                        write(unit=666,advance="no",fmt="(3a,i3,a,i3,a,i3,2a)") &
                              ",""",trim(file(i)),""" using ",x_column,":",y_column,":",z_column," with ",&
                              plot_type(plot_typ)
                 end if
        end if


end do  main_do

if (file_count==0) then
        print *,"Nada que dibujar"
else
        if (slides == 0.0) then
!*************************************************************************************************
! GnuPlot 4: use the next instruction to use the mouse as input device
!
!               write(unit=666,fmt="(/,a)")          "pause -1 ""Click para continuar"""
                write(unit=666,fmt="(/,a)")          "pause -1 ""Return para continuar"""
!*************************************************************************************************
! GnuPlot 4: use the next instruction for setting enhanced terminal
!
                if (output_typ == 1) then
                     write(unit=666,fmt="(3a)")         "set terminal ",trim(output_type(output_typ))," enhanced"
                else
                     write(unit=666,fmt="(3a)")         "set terminal ",trim(output_type(output_typ))," enhanced color"
                end if
!               write(unit=666,fmt="(3a)")         "set terminal ",trim(output_type(output_typ))," color"
                write(unit=666,fmt="(a,"//format)  "set output ""grafico",call_count,".",trim(output_extension(output_typ)),""""
                write(unit=666,fmt="(a)")          "replot"

	else

                write(unit=666,fmt="(/,a,f0.0)")   "pause ",slides
        end if
        close (unit=666)

!*************************************************************************************************
! GnuPlot 4: use the next instruction. Background seems to be white by default
!
!       call system ("gnuplot ""gnuplot.gnu""")
!*************************************************************************************************

	if (slides/=0.0) then
        	call system (".gnu &")
        	call wait(0.5*slides)
	else
!	        call system ("gnuplot -geometry 1260x742 -background white ""gnuplot.gnu""")
	        call system ("gnuplot -geometry +0+0 -background white ""gnuplot.gnu""")
	end if
end if

end subroutine plot

end module graph
