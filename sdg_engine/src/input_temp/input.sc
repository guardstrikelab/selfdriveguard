map = "Town03";

// ego car
ego_init_position = (-110,3); //default coordinate frame is ENU
ego_target_position = (170,-60); //default coordinate frame is ENU
ego_init_state = (ego_init_position);
ego_target_state = (ego_target_position);

car_model = "Lincoln MKZ 2017";
car_color = (255, 0, 0);
vehicle_type = (car_model, car_color);
ego_vehicle = AV(ego_init_state, ego_target_state, vehicle_type);

// npcs
npc1=Vehicle(((-3,-45),,-1),,((245.3,-75)));
npc2=Vehicle(((-3,-52),,-1),, ((245.3,-60)));
npc3=Vehicle(((-85,-40),,-1),, ((234.8,120)));
npc4=Vehicle(((-85,-50),,-1),, ((234.8,50)));
npc5=Vehicle(((-88.5,-43),,-1),,((234.8,150)));
npc6=Vehicle(((-77,30),,-1),,((140,-1)));
npc7=Vehicle(((-77,-37),,-1),,((170,-4.5)));
npc8=Vehicle(((23,23),,-1),,((170,-4.5)));
npc9=Vehicle(((-67,230),,-1),,((170,-4.5)));
npc10=Vehicle(((89,77),,-1),,((170,-4.5)));
npc11=Vehicle(((-250,199),,-1),,((170,-4.5)));
npc12=Vehicle(((-63,0),,-1),,((170,-4.5)));
npc13=Vehicle(((-55,0),,-1),,((170,-4.5)));
npc14=Vehicle(((-45,1),,-1),,((170,-4.5)));
npc15=Vehicle(((-35,3),,-1),,((170,-4.5)));
npc16=Vehicle(((-25,3),,-1),,((170,-4.5)));
npc17=Vehicle(((-15,3),,-1),,((170,-4.5)));
npc18=Vehicle(((-5,3),,-1),,((170,-4.5)));
npc19=Vehicle(((5,3),,-1),,((170,-4.5)));
npc20=Vehicle(((-77,-45),,-1),,((170,-4.5)));
npc21=Vehicle(((-20,-6),,-1),,((170,-4.5)));
npc22=Vehicle(((-88,-5),,-1),,((170,-4.5)));
npc23=Vehicle(((20,3),,-1),,((170,-4.5)));
npc24=Vehicle(((40,3),,-1),,((170,-4.5)));
npc25=Vehicle(((65,0),,-1),,((170,-4.5)));
npc26=Vehicle(((45,-3),,-1),,((170,-4.5)));
npc27=Vehicle(((30,-3),,-1),,((170,-4.5)));
npc28=Vehicle(((15,-3),,-1),,((170,-4.5)));
npc29=Vehicle(((5,-3),,-1),,((170,-4.5)));
npc30=Vehicle(((-5,-3),,-1),,((170,-4.5)));
npc31=Vehicle(((-15,-3),,-1),,((170,-4.5)));
npc32=Vehicle(((-25,-3),,-1),,((170,-4.5)));
npc33=Vehicle(((5,35),,-1),,((170,-4.5)));
npc34=Vehicle(((-80,1),,-1),,((170,-4.5)));
npc35=Vehicle(((-85,1),,-1),,((170,-4.5)));
npc36=Vehicle(((-63,-3),,-1),,((170,-4.5)));
npc37=Vehicle(((45,-3),,-1),,((170,-4.5)));
npc38=Vehicle(((55,-3),,-1),,((170,-4.5)));
npc39=Vehicle(((65,-6),,-1),,((170,-4.5)));
npc40=Vehicle(((75,-6),,-1),,((170,-4.5)));
npc41=Vehicle(((3,63),,-1),,((170,-4.5)));
npc42=Vehicle(((-3,53),,-1),,((170,-4.5)));
npc43=Vehicle(((3,43),,-1),,((170,-4.5)));
npc44=Vehicle(((6,33),,-1),,((170,-4.5)));
npc45=Vehicle(((-3,23),,-1),,((170,-4.5)));
npc46=Vehicle(((6,13),,-1),,((170,-4.5)));
npc47=Vehicle(((3,3),,-1),,((170,-4.5)));
npc48=Vehicle(((3,-5),,-1),,((170,-4.5)));
npc49=Vehicle(((6,-15),,-1),,((170,-4.5)));
npc50=Vehicle(((3,-25),,-1),,((170,-4.5)));
npc51=Vehicle(((-3,63),,-1),,((170,-4.5)));
npc52=Vehicle(((-5,53),,-1),,((170,-4.5)));
npc53=Vehicle(((-3,43),,-1),,((170,-4.5)));
npc54=Vehicle(((-5,33),,-1),,((170,-4.5)));
npc55=Vehicle(((-3,23),,-1),,((170,-4.5)));
npc56=Vehicle(((-5,13),,-1),,((170,-4.5)));
npc57=Vehicle(((5,23),,-1),,((170,-4.5)));
npc58=Vehicle(((-3,-6),,-1),,((170,-4.5)));
npc59=Vehicle(((-3,-16),,-1),,((170,-4.5)));
npc60=Vehicle(((-3,-32),,-1),,((-170,-4.5)));

npcs = {npc1,npc2,npc3,npc4,npc5,npc6,npc7,npc8,npc9,npc10,npc11,npc12,npc13,npc14,npc15,npc16,npc17,npc18,npc19,npc20};

// pedestrian
pedestrian_type = (1.65, black);
pedestrian1 = Pedestrian(((-15.9, 110), ,0.5), , ((-56, 123), ,0), pedestrian_type);
pedestrian2 = Pedestrian(((101, 62), ,0.5), , ((120, 144), ,0), pedestrian_type);
pedestrians = {pedestrian1, pedestrian2};

// env
time = 10:00;
weather = {sunny: 0.8};
env = Environment(time, weather);

//traffic requirements
speed_range = (0,20);
speed_limit = SpeedLimit("52.-1", speed_range);
intersection = Intersection(1, 1, 0, 1);
traffic = {intersection, speed_limit};

scenario = CreateScenario{load(map);
        ego_vehicle;
        npcs;
        {};
        {};
        env;
        traffic;
};