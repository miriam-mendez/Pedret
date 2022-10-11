# Pedret
======
> This repository has been made in the research environment, so there are files that cannot be shared publicly, and this has affected the radiance folder, which is not compilable due to the lack of models and textures. However, all rendered results and code can be viewed.

## Content
```
radiance
├── lib # 3D model library
|   |          
│   ├── mat # physical properties of the 3D model materials
|   |   └── *.mat
|   |   
|   └── rad # geometry of 3D models
|       └── *.rad 
|
├── lib_ies # IES file library              
|   └── *.ies 
|
├── lib_view # view file library              
|   └── *.vf 
|
└── scenes # all the scenes rendered with Radiance
    |
    ├── pedret1
    |   ├── img # rendering results
    |   |   └── *.hdr or *.png
    |   ├── scene.rad # scene definition
    |   └── scene.rif # render configuration file
    └── ...
``` 

## Images
![alt text](radiance/scenes/pedret2/img/lux11%3A00_door.png)

