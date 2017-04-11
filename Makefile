all: gui_class.py test

gui_class.py: gui.ui
	pyuic4 src/gui/gui.ui > src/gui/gui_class.py

test:
	python3 test.py

.PHONY: clean

clean:
	rm arenas/testing_cycle_out arenas/testing_out
	rm src/gui/gui_class.py
