python -m modules.doc_opener 0 2 &
p1=$!
# python -m modules.doc_opener 1 2 &
# p2=$!
# python -m modules.doc_opener 2 2 &
# p3=$!
# python -m modules.doc_opener 3 2 &
# p4=$!
# python -m modules.doc_opener 4 10 &
# p5=$!
# python -m modules.doc_opener 5 10 &
# p6=$!
# python -m modules.doc_opener 6 10 &
# p7=$!
# python -m modules.doc_opener 7 10 &
# p8=$!
# python -m modules.doc_opener 8 10 &
# p9=$!
# python -m modules.doc_opener 9 10 &
# p10=$!

# wait $p1 $p2 $p3 $p4 $p5 $p6 $p7 $p8 $p9 $p10
wait $p1
sleep 1000