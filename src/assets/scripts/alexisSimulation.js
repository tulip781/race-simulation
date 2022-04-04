import everpolate from "everpolate";
// vehicle characteristics
// you can experiment changing these as well if you want!
let m, g, p, Cd, A, wheelr, G1,G2, GR, lm, rho, parameters, tEff, minrpm,maxrpm,drpm, irpm, T;

// mass of kart + driver
//  #kg
m = 96.5 + 85;
// m/s^2 (gravity)
g = 9.81 ;
// tyre pressure (not including differences due to tyre temp change)
// #bar (36 psi)
p = 2.48211;
// coefficient of drag
Cd = 0.5 ;
// frontal area
A = 0.4 ;
// #m #wheelradius
wheelr = 0.2794/2 ;
// define gear ratio
G1 = 20 ;
G2 = 71 ;
GR = G2/G1;
// mass factor (approximation, source: ADM yr. 3 course notes)
lm = 1 + 0.04 + 0.0025*(GR**2);
// density of air
// kg/m^3
rho = 1.23;
// these are irrelevant to this model
// clutch engagement speed
// RPM
engagedSpeed = 2000;
// total drivetrain efficiency (not including clutch) (constant)
tEff = 0.93

parameters = {'m': m, 'g': g, 'p': p, 'Cd': Cd, 'A': A, 'wheelr': wheelr, 'lm': lm, 'rho': rho,
              'engagedSpeed': engagedSpeed, 'tEff': tEff};

//  initialize torque curves
rpm = [2000, 2600, 3000, 3500, 4000, 5000, 6000, 6200, 6960]
// rpm = np.array(rpm)
// data based on gx160
trq = [5.0, 13.8, 14.88, 13.7, 12.5, 10.35, 7.3, 6.1, 1.0]
// data modified to fit track data 
trq = [5.0, 13.8, 15.0, 14.0, 13.0, 10.35, 7.0, 6.0, 1.0] 
// trq = np.array(trq)
// multiply by 2 cause we have two engines
trq.forEach((i, index) => trq[index] = 2*i);
// multiplication factor because we are using gx160 data not gx200

// trq = 1.03*trq 
trq.forEach((i, index) => trq[index] = 1.03*i);

// create interpolation function for engine torque to be used in simulate()
minrpm = rpm[0];
maxrpm = rpm[-1];
drpm = 1;
let  arrangeResult = []
for(i = minrpm; i < maxrpm; i++ ){
    arrangeResult.push(i);
}

// irpm = np.arange(minrpm, maxrpm+drpm, drpm);
irpm = arrangeResult;
// Array of little 
T = everpolate.polynomial(irpm, rpm, trq);
// Tinterp = sc.interp1d(rpm, trq, kind='cubic');
// T = Tinterp(
    

    
// )

//  #initialize a random track length
//  randInt = random.randint(2, 20)
//  distance = randInt * 50

// or choose a manual distance, and try different gear ratios
distance = 500
print("Your given drag race distance is: " + str(distance) + "m")

print("Choose a gear ratio to try:")
GR = input()
# #in case you want to manually set a gear ratio
# GR = 3
GR = float(GR)




const simulate = (GR, t, parameters, distance, initialVel = 0) => {
    let v, c, Fr, Fd, Ft, a, d,w1, w2, eng, maxRpm;

    let startingArray = []
    for (let i = 0; i < t; i++){
        startingArray.push(0)
    }
    v, c, Fr, Fd, Ft, a, d,w1, w2, eng = startingArray;
    // initial kart velocity in m/s
    // assumed 0 in this version
    v[0] = initialVel*(1000/(60*60));

    // use initial kart velocity to set an initial output shaft rotation speed
    w2[0] = v[0]/(0.2794*0.5) * (60/(2*3.14));
    w1[0] = w2[0] * GR;

    // idling engine speed (RPM)
    eng[0] = 2200;
    // set engine speed maximum limit (based on experimental data)
    maxRpm = 6960

    for (let i = 0; i < t; i++){
        // calculate rolling resistance (speed in km/h)
        c[i+1] = 0.005 + (1/parameters[p])*(0.01+0.0095*((v[i]*3.6)/100)**2)
        Fr[i+1] = c[i]*parameters[m] * parameters[g]
        Fd[i+1] = 0.5*parameters[rho]*parameters[Cd]*parameters[A]*(v[i]**2)

        // torque for each engine speed using engine power curves
        Tinterp = sc.interp1d(rpm, trq, kind='cubic')
        Teng = Tinterp(eng[i])

    }
}