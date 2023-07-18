while inotifywait -r -e modify source/
do
    make html
done
