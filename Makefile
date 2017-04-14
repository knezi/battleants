DOCHTML=doc/exceptions.html doc/box_container.html doc/player_control.html doc/player_instance.html doc/game.html

all: gui test

gui: src/gui/gui.ui
	pyuic4 src/gui/gui.ui > src/gui/gui_class.py

test:
	python3 test.py

doc: doc/doc.html $(DOCHTML)

doc/doc.html: doc/doc.md $(DOCHTML)
	pandoc -o doc/doc.html doc/doc.md -t html -f markdown

$(DOCHTML): doc/%.html: src/%.py
	pydoc -w $<
	mv `basename $@` doc/

.PHONY: clean

clean:
	rm arenas/testing_cycle_out arenas/testing_out
	rm src/gui/gui_class.py
