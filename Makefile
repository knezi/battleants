DOC=src/exceptions.py src/box_container.py

all: gui test

gui: src/gui/gui.ui
	pyuic4 src/gui/gui.ui > src/gui/gui_class.py

test:
	python3 test.py

doc: doc/doc.md $(DOC)
	pandoc -o doc/doc.html doc/doc.md -t html -f markdown
	pydoc -w $(DOC)
	mv $(DOC) doc/

.PHONY: clean

clean:
	rm arenas/testing_cycle_out arenas/testing_out
	rm src/gui/gui_class.py
