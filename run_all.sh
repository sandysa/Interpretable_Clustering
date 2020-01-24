bash fig2b.sh > adult_log.txt
bash fig2a.sh > accident_log.txt

bash fig2d.sh > sanitation_log.txt
bash fig2c.sh > crime_log.txt

python testCluster.py 5 0 0 > accident_ikc
python testCluster.py 5 0 1 > accident_kc
python testCluster.py 5 0 2 > accident_p
python testCluster.py 5 0 3 > accident_kcf

python testCluster.py 5 1 3 > sanitation_kcf
python testCluster.py 5 1 2 > sanitation_p
python testCluster.py 5 1 1 > sanitation_kc
python testCluster.py 5 1 0 > sanitation_ikc

python testCluster.py 5 2 0 > crime_ikc
python testCluster.py 5 2 1 > crime_kc
python testCluster.py 5 2 2 > crime_p
python testCluster.py 5 2 3 > crime_kcf


python testCluster.py 5 3 0 > adult_ikc
python testCluster.py 5 3 1 > adult_kc
python testCluster.py 5 3 2 > adult_p
python testCluster.py 5 3 3 > adult_kcf


