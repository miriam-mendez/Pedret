# Pedret


## Getting started

Basic rendering: 
```shell 
obj2mesh -a lib/mat/pedret.mat lib/obj/pedret.obj lib/obj/pedret.rtm
oconv sky.rad scene.rad > scene.oct
rad simple.rif &
ximage [-e auto] scene.hdr
```

## Radiance: useful commands
* to see the options of a scene.rif: ``rad -n -e simple.rif``
* to render without scene.rif: ``rpict [options] scene.oct > scene.pic``
* to interact with the scene:``rvu [options] scene.oct `` or ``rad -o x11 simple.rif``
* to create an ambient file: ``rpict [options] -af scene.amb scene.oct > scene.pic``
* to get information of binary files: ``getinfo scene.oct``

### Obtain falsecolor images:
* scene:``rpict [options] scene.oct | falsecolor -s 4000 -l cd/m^2 > falseScene.pic``
* sky: ``rpict -vta -vp 0 0 0 -vd 0 0 1 -vu 0 1 0 -vh 180 -vv 180 sky_day.oct | falsecolor -s 4000 -l cd/m^2 > falseSky.pic``

## Blender: useful commands
* Move active camera to view: ``Ctrl+Alt+Numpad 0``
* Copy python properties: ``Ctrl + Shift + C``
* Copy full python path: ``Ctrl+Alt+Shift+C``
* See available icons: ``Ctrl+Alt+T``

## Images
![alt text](radiance/scenes/pedret2/img/lux11%3A00_door.png)

<!-- 
## Radiance folder structure
```
.
├── lib                
│   ├── mat   
|   |   └── *.mat
│   ├── obj
|   |   ├── blender
|   |   |   └── pedret.blend
|   |   ├── *.obj
|   |   └── *.rtm
|   ├── rad
|   |   └── *.rad
|   ├── tex
|   |   └── *.hdr
|   └── Makefile
|
├── lib_ies                
|   └── *.ies
|
├── lib_view                 
|   └── *.vf
|
└── scenes
    ├── pedret1
    |   ├── img
    |   |   └── *.hdr
    |   ├── scene.amb
    |   ├── scene.oct
    |   ├── scene.rad
    |   └── scene.rif
    └── ...
``` -->