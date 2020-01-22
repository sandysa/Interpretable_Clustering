
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
set key font "Helvetica,103,bold"

set xlabel font "Helvetica,42,bold"
set ylabel font "Helvetica,42,bold"
set xtics font "Helvetica,36,bold"
set ytics font "Helvetica,36,bold"
set title font "Helvetica,42,bold"



set multiplot layout 1,4

set boxwidth 0.8 absolute
set style fill   pattern 1.00 border lt -1
set key samplen 1.5 spacing .5 font ",38"
set style histogram rowstacked


set xlabel 'I_F' offset 0,-1
set ylabel 'kC objective' offset -5
#set title 'cora, 0.1,0.1'
set ytics 0.2
set xtics 0.2
#set key at 1,0.46
set key at screen 1.25,1.25
set size 1.1,1.2
set origin 0.05,0


set datafile missing '-'
set style data histograms
set xtics border in scale 0,0 nomirror rotate by -45
#set xtics border in scale 0,0 nomirror rotate by 0
set xtics  norangelimit
set xtics   ()

set label "(a) {/Symbol b}=0.7" at 1.5,-0.35	 center font "Helvetica,48,bold"

set ylabel "FoI Distribution" offset -10
set xlabel "Clusters" offset 0,-1
set ylabel offset 0,0
set yrange [0:1.1]


plot 'explanation0.7/data.txt' using ($2):xtic(1) t "%latrines 0-25" lw 4 lc 1 lt 1, '' u ($3) t"" lw 4 lc 2 lt 1,  '' u ($4) t"" lw 4 lc 3 lt 1,  '' u ($5) t"" lw 4 lc 4 lt 1


unset label

set size 1.1,1.2
set origin 1.25,0
set key at screen 2.05,1.25

#set yrange [0:1]


set xtics 0,50,200


set ylabel "FoI Distribution" offset -10
set xlabel "Clusters" offset 0,-1
set ylabel offset 0,0
set yrange [0:1.1]

#set title 'cora, 0.1,0.1'
set label "(b) {/Symbol b}=0.8" at 1.5,-0.35	 center font "Helvetica,48,bold"

plot 'explanation0.8/data.txt' using ($2):xtic(1) t"" lw 4 lc 1 lt 1, '' u ($3) t"%latrines 25-50" lw 4 lc 2 lt 1,  '' u ($4) t"" lw 4 lc 3 lt 1,  '' u ($5) t"" lw 4 lc 4 lt 1


unset label
#unset key
set key at screen 2.85,1.25
set size 1.1,1.2
set origin 2.45,0


set ylabel "FoI Distribution" offset -10
set xlabel "Clusters" offset 0,-1
set ylabel offset 0,0
set yrange [0:1.1]


set style line 1 lt 1 lw 16 pt 1 lc rgb "black"
set label "(c) {/Symbol b}=0.9" at 1.5,-0.35	 center font "Helvetica,48,bold"

plot 'explanation0.9/data.txt' using ($2):xtic(1) t"" lw 4 lc 1 lt 1, '' u ($3) t"" lw 4 lc 2 lt 1,  '' u ($4) t"%latrines 50-75" lw 4 lc 3 lt 1,  '' u ($5) t"" lw 4 lc 4 lt 1

unset label

set key  at screen 3.6,1.25
set size 1.1,1.2
set origin 3.65,0
set ylabel "FoI Distribution" offset -10
set xlabel "Clusters" offset 0,-1
set ylabel offset 0,0
set yrange [0:1.1]

set label "(d) {/Symbol b}=1" at 1.5,-0.35	 center font "Helvetica,48,bold"

plot 'explanation1/data.txt' using ($2):xtic(1) t"" lw 4 lc 1 lt 1, '' u ($3) t"" lw 4 lc 2 lt 1,  '' u ($4) t"" lw 4 lc 3 lt 1,  '' u ($5) t"%latrines 75-100" lw 4 lc 4 lt 1
