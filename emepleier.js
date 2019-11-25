

// show single instance video
s0.initCam(0)
src(s0).out()


//show 4 instances of videos
s0.initCam(1)
src(s0).diff(osc(20),0.5).out(o0)
s1.initCam(2)
src(s1).saturate(30).out(o1)
s2.initCam(3)
src(s2).scale(2).kaleid(10).out(o2)
s3.initCam(4)
src(s3).out(o3)
render()
