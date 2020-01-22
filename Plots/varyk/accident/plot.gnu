set key
set output "data.ps"
set terminal postscript dashed color

set xlabel 'k' offset 0,-1
set ylabel 'kC objective' offset -15
set xtics 10
set ytics 0.04
#set title 'cora, 0.1,0.1'
set key at 40,10.4700000
set key spacing 0.8
set key font "Helvetica,52,bold"
set xlabel font "Helvetica,52,bold"
set ylabel font "Helvetica,52,bold"
set xtics font "Helvetica,52,bold"
set ytics font "Helvetica,52,bold"
set title font "Helvetica,52,bold"


set style line 1 lt 1 lw 16 pt 1 lc rgb "black"
set style line 2 lt 2 lw 16 pt 2 lc rgb "blue"
set style line 3 lt 3 lw 16 pt 3 lc rgb "red"
set style line 4 lt 3 lw 16 pt 4 lc rgb "green"
set style line 5 lt 3 lw 16 pt 3 lc rgb "orange"
set style line 6 lt 3 lw 16 pt 3 lc rgb "red"
set style line 7 lt 3 lw 16 pt 3 lc rgb "pink"
set multiplot
plot	"ourkc.txt" using 1:2 lw 10 ps 3.5 pt 8 lt 2  pointinterval 1 lc 1 with linespoint t '{/Symbol b}-IC',\
		"ikc.txt" using 1:2 lw 10 ps 3.5 pt 9 lt 2  pointinterval 2 lc 2 with linespoint t 'IkC',\
		"kc.txt" using 1:2 lw 10 ps 3.5 pt 10 lt 2  pointinterval 2 lc 3 with linespoint t 'kc' ,\
		"ric.txt" using 1:2 lw 10 ps 3.5 pt 12 lt 2  pointinterval 3 lc 4 with linespoint t 'RIC',\
		"newbase.txt" using 1:2 lw 10 ps 3.5 pt 13 lt 2  pointinterval 3 lc 5 with linespoint t 'RIC'