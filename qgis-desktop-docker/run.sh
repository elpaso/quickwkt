
IMAGE=qgis-desktop-nightly


# Lancia QGIS nel display corrente
xhost +; docker run --rm -it --name qgis-desktop -v /tmp/.X11-unix:/tmp/.X11-unix -v `pwd`/qgishome:/qgishome -e DISPLAY=unix$DISPLAY $IMAGE qgis


# Lancia in BG per usare poi exec e i test in

docker run -d --name $IMAGE -v /tmp/.X11-unix:/tmp/.X11-unix -v /home/ale/.qgis2/python/plugins/.quickwkt:/tests_directory -e DISPLAY=:99 $IMAGE

# -d needs -it
docker exec -it $IMAGE sh -c "qgis_testrunner.py travis_tests.test_TravisTest"
