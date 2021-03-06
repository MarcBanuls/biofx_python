#!/usr/bin/env bash

# Benchmark all the solutions

PRGS=$(find . -name solution\* | sort | xargs echo | sed "s/ /,/g")
hyperfine --warmup 1 -L prg $PRGS '{prg} seqs.fa'
