
reset

set term postscript eps dashed color enhanced 24


set output "output.eps"

set bmargin 7

#set key samplen 6
#set key spacing 15
#set key default
#set key at 2.5,1
#set key out horizontal top left
set size 4.8,1.3


set key out horizontal top

set key font "Helvetica,46,bold"
set xlabel font "Helvetica,42,bold"
set ylabel font "Helvetica,42,bold"
set xtics font "Helvetica,36,bold"
set ytics font "Helvetica,36,bold"
set title font "Helvetica,42,bold"



set multiplot layout 1,4

set xrange [10:50]
set xlabel 'k' offset 0,-1
set ylabel 'o_{kC}' offset -3
#set title 'cora, 0.1,0.1'
set ytics 0.03
set xtics 20
#set key at 1,0.46
set key at screen 1.25,1.29
set size 1.1,1.2
set origin 0.05,0

set label "(a) accidents" at 30,0.28	 center font "Helvetica,48,bold"

plot	"accident/ourkc.txt" using 1:2  lw 10 ps 7 pt 8 lt 2  pointinterval 2 lc 1 with linespoint t '{/Symbol b}-IC',\
		"accident/ikc.txt" using 1:2  lw 10 ps 7 pt 9 lt 2   pointinterval 2 lc 2 with linespoint t 'IKC',\
		"accident/kc.txt" using 1:2  lw 10 ps 7 pt 10 lt 2   pointinterval 3 lc 3 with linespoint t '' ,\
		"accident/ric.txt" using 1:2  lw 10 ps 7 pt 12 lt 2   pointinterval 3 lc 4 with linespoint t '',\
		"accident/newbase.txt" using 1:2  lw 10 ps 7 pt 13 lt 2   pointinterval 3 lc 5 with linespoint t '',\

unset label

set size 1.1,1.2
set origin 1.25,0
set key at screen 1.65,1.29

#set yrange [0:1]


set xtics 0,50,200


set xlabel 'k' offset 0,-1
set ylabel 'o_{kC}' offset -5
set ytics 300000
set xtics 20

#set title 'cora, 0.1,0.1'
set label "(b) adult" at 30,-400000.417	 center font "Helvetica,48,bold"

plot	"adult/ourkc.txt" using 1:2 lw 10 ps 7 pt 8 lt 2  pointinterval 1 lc 1 with linespoint t '',\
		"adult/ikc.txt" using 1:2 lw 10 ps 7 pt 9 lt 2  pointinterval 2 lc 2 with linespoint t '',\
		"adult/kc.txt" using 1:2 lw 10 ps 7 pt 10 lt 2  pointinterval 2 lc 3 with linespoint t 'KC' ,\
		"adult/ric.txt" using 1:2 lw 10 ps 7 pt 12 lt 2  pointinterval 3 lc 4 with linespoint t '',\
		"adult/newbase.txt" using 1:2 lw 10 ps 7 pt 13 lt 2  pointinterval 3 lc 5 with linespoint t '',\


unset label
#unset key
set key at screen 2.06,1.29
set size 1.1,1.2
set origin 2.45,0


set xlabel 'k' offset 0,-1
set ylabel 'o_{kC}' offset -5
set ytics 30000
set xtics 20
set yrange [0:110000]
#set title 'cora, 0.1,0.1'


set style line 1 lt 1 lw 16 pt 1 lc rgb "black"
set label "(c) crime" at 30,-38000	 center font "Helvetica,48,bold"

plot	"crime/ourkc.txt" using 1:2 lw 10 ps 7 pt 8 lt 2  pointinterval 1 lc 1 with linespoint t '',\
		"crime/ikc.txt" using 1:2 lw 10 ps 7 pt 9 lt 2  pointinterval 2 lc 2 with linespoint t '',\
		"crime/kc.txt" using 1:2 lw 10 ps 7 pt 10 lt 2  pointinterval 2 lc 3 with linespoint t '' ,\
		"crime/ric.txt" using 1:2 lw 10 ps 7 pt 12 lt 2  pointinterval 3 lc 4 with linespoint t 'KC_F',\
		"crime/newbase.txt" using 1:2 lw 10 ps 7 pt 13 lt 2  pointinterval 2 lc 5 with linespoint t '',\

unset label

set key  at screen 2.45,1.29
set size 1.1,1.2
set origin 3.65,0
set xlabel 'k' offset 0,-1
set ylabel 'o_{kC}' offset -5
set xtics 20
set yrange [0:550000]
set ytics 150000
#set title 'cora, 0.1,0.1'
set label "(d) sanitation" at 30,-190000	 center font "Helvetica,48,bold"
plot	"sanitation/ourkc.txt" using 1:2 lw 10 ps 7 pt 8 lt 2  pointinterval 1 lc 1 with linespoint t '',\
		"sanitation/ikc.txt" using 1:2 lw 10 ps 7 pt 9 lt 2  pointinterval 2 lc 2 with linespoint t '',\
		"sanitation/kc.txt" using 1:2 lw 10 ps 7 pt 10 lt 2  pointinterval 2 lc 3 with linespoint t '' ,\
		"sanitation/ric.txt" using 1:2 lw 10 ps 7 pt 12 lt 2  pointinterval 3 lc 4 with linespoint t '',\
		"sanitation/newbase.txt" using 1:2  lw 10 ps 7 pt 13 lt 2   pointinterval 3 lc 5 with linespoint t 'P_F',\
