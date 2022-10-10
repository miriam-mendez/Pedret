.PHONY : lib
lib :
	cd lib; $(MAKE)  all

view:
	make lib
	rad -o x11 scene.rif

render:
	make lib
	rad scene.rif

clean:
	cd lib; $(MAKE) clean
	rm *.oct *.amb