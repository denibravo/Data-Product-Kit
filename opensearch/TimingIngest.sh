#!/bin/bash
# test this with different number of comments in various orders of magnitude


for i in {1..10}
do
     python ingest.py 10
     python delete_index.py --yes
done

for i in {1..10}
do
     python ingest.py 100
     python delete_index.py --yes
done

for i in {1..10}
do
     python ingest.py 1000
     python delete_index.py --yes
done

for i in {1..10}
do
     python ingest.py 10000
     python delete_index.py --yes
done

for i in {1..5}
do
     python ingest.py 100000
     python delete_index.py --yes
done

for i in {1..5}
do
     python ingest.py 1000000
     python delete_index.py --yes
done


for i in {1..10}
do
     python ingest-bulk-from-local.py 10
     python delete_index.py --yes
done

for i in {1..10}
do
     python ingest-bulk-from-local.py 100
     python delete_index.py --yes
done

for i in {1..10}
do
     python ingest-bulk-from-local.py 1000
     python delete_index.py --yes
done

for i in {1..10}
do 
    python ingest-bulk-from-local.py 10000
    python delete_index.py --yes
done

for i in {1..5}
do
    python ingest-bulk-from-local.py 100000
    python delete_index.py --yes
done

for i in {1..5}
do
    python ingest-bulk-from-local.py 1000000
    python delete_index.py --yes
done


