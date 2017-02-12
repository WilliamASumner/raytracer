Intro: 
This is just a simplistic raytracer project for my own amusement.
I am currently in the process of learning c++ and would appreciate any and all suggestions to make my code better! 

Enjoy! :) 

To Set Up: 
To use simply run the script in IDLE or via the command line, the default scene should render without a problem. 
This verison supports spheres as well as both Lambertian and Phong shading. To edit the scene simply use .addObject or .addLight on mscene. 

Known Issues: 
- Runs a bit slow with resolutions beyond 200x200.
- Changing the aspect ratio to anything but a square (e.g. 100x100) creates weird warping of the spheres
- Adding lots of spheres can change affect the shading of all the others
