# SlitScanCameraConcept
Proof of concept for a demo involving a slit scan camera being simulated based on a webcam

# Instructionsusage:
`main.py [-h] [--camera {piv2,web}] [--mode {0,1,2,3,4,5,6,7}] [--outputVid OUTPUTVID]`

```
optional arguments:
  -h, --help            show this help message and exit
  --camera {piv2,web}   select what camera you are using
  --mode {0,1,2,3,4,5,6,7}
                        select a mode. For webcam you may need to try
                        different numbers including zero. For Pi v 2 camera, a
                        higher mode should be lower res but higher fps, don't
                        try zero for pi though
  --outputVid OUTPUTVID
                        path to save video of attempt to. will delete whatever
                        it is pointed at.  Tested with .avi
```



# todo:
- [ ] add CLI options so that it doesn't have to be edited to change behavior 
- [ ] Turn into library that can be imported rather that just a demo
- [ ] Add unittesting
