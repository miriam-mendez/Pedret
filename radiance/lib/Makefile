 .PHONY : all
all: pedret1 pedret2 gwindow lwindow candle

pedret1: 
	obj2mesh -a mat/pedret1.mat obj/pedret1.obj obj/pedret1.rtm
pedret2:
	obj2mesh -a mat/pedret2.mat obj/pedret2.obj obj/pedret2.rtm
lwindow:
	obj2mesh -a mat/lwindow.mat obj/window.obj obj/lwindow.rtm
gwindow:
	obj2mesh -a mat/gwindow.mat obj/window.obj obj/gwindow.rtm
candle:
	obj2mesh -a mat/candle.mat obj/candle.obj obj/candle.rtm
	
clean: 
	rm obj/*.rtm