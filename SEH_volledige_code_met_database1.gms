$onempty
$GDXIN %SupplyDataFileName%
$eolcom #

Sets
         t       time period
         cat2    appliances of category two
         cat3    appliances of category three
;
$LOAD t, cat2, cat3
ALIAS(t,ta);
ALIAS(t,tt);

Parameters
*        Global
         TEMP_AMB(t)     Temperature of the environment (in K) -> time
         PRICE(t)        price of energy
         RESLOC(t)       local supply of renewables

*        Cat1
         D_TOT_CAT1(t)            category 1 demand (fixed)


*        Cat2
         D_CYCLE_CAT2(cat2, ta)   demand cycle per cat2 appliance
         N_CYCLES_CAT2(cat2)      number of cycles per day
         DUR_CAT2(cat2)           duration of wm cycle


*        Cat3
         UA_CAT3(cat3)          isolation constant of the refrigator
         COP_CAT3(cat3)         coefficient of performance of the refrigator
         PCOOL_CAT3(cat3)       power needed for the refrigator
         MASS_CAT3(cat3)        mass of the cooled air inside the refrigator
         T_MIN_CAT3(cat3)      minimal temperature inside the cat3 device
         T_MAX_CAT3(cat3)      maximal temperature inside the cat3 device

*        Cat4
         T_MIN_CAT4(t)   minimal temperature inside the cat3 device
         T_MAX_CAT4(t)     maximal temperature inside the cat3 device

*        scalars




;
$LOAD TEMP_AMB, PRICE, RESLOC,
$LOAD D_TOT_CAT1,
$LOAD D_CYCLE_CAT2, N_CYCLES_CAT2, DUR_CAT2,
$LOAD UA_CAT3, COP_CAT3, PCOOL_CAT3, MASS_CAT3, T_MIN_CAT3, T_MAX_CAT3,
$LOAD T_MIN_CAT4, T_MAX_CAT4
* $LOAD UA_HOUSE, COP_HOUSE, PHEAT_HOUSE, MASS_HOUSE, Pload_battery, Capacity_battery

SCALAR
         PRICECURT        price of curtailing RES [€]  /45/
         CP               thermodynamic coeficient      /1.005/
         POWER_LIMIT      maximal power the house can take from the grid (in kW) /9400/
         Pload_battery    laadvermogen batterij (in W) /%PLOAD%/
         Capacity_battery capaciteit batterij (in Wh)  /%CAP%/
         UA_HOUSE         Isolation constant of the house  /%UA%/
         COP_HOUSE        coefficient of performance of the house /%COP%/
         PHEAT_HOUSE      power needed for the boiler of the house /%PHEAT%/
         MASS_HOUSE       mass of the heated air inside the house  /%MASS%/
;


Variables
         zcost            the energycost
         objective        the objective function
*cat3
         Qin_cat3(t,cat3)      Heat we put in the refrigator (neg.)
         Qout_cat3(t,cat3)     Heat which escapes from the refrigator
         temp_cat3(t,cat3)     Temperature of the refrigator(in K)
         d_cat3(t,cat3)      Power consumed by the refrigator
*cat4
         Qin_cat4(t)    Heat we put in the house (neg.)
         Qout_cat4(t)   Heat which escapes from the house
         temp_cat4(t)   Temperature of the house (in K)
         d_cat4(t)    Power consumated by the house
         z_cat4(t)    Defines at which % the boiler is using power to heat

         d_total       Total power used by the quarter
*         cat4_total      total of cat4
*                                                (quarter = wijk )
*Cat5
         Pin_battery(t)  Power we put into the battery
         energy_cat5(t)  Amount of enegry stored in the battery
         penalty_function
         ;

POSITIVE VARIABLES
P_conv(t)        Conventional power supply
P_cat1(t)        Demand of appliances of category 1
P_cat2(t)        Demand of appliances of category 2
P_cat3(t)        Demand of appliances of category 3
P_cat4(t)        Demand of appliances of category 4
P_cat5(t)        Demand of appliances of category 5
Curt(t)          Curtailed local renewable energy
z_cat4(t)     Defines whether the heating is on or off
;

BINARY VARIABLES
ti(t, cat2)    1 if cat 2 cycle starts at t and 0 otherwise
z_cat3(t,cat3)
z_cat5(t)
u(t)


;



Equations

*GLOBAL
         q_objective_function    objective function
         q_zcoste                 Cost function
         q_balance(t)             Electricity balance
         q_power_limit(t)         power limit of the house
         q_cat1(t)                Demand for appliances of category 1
         q_cat2(t)                Demand for appliances of category 2
         q_cat3(t)                Demand for appliances of category 3
         q_cat4(t)                Demand for appliances of category 4
         q_cat5(t)                Demand for appliances of category 5

*CAT2
         q_n_cycles_cat2(cat2)           Ensure the dishwasher works the needed amount of cycles
         q_no_overlap(t,cat2)           Ensure cycles of one appliance don't overlap and don't follow each other immediately. (Have to be able to put in clothes)
*CAT3
         q_temp_equ_cat3(t,cat3)      links heat difference and temperature difference for the refrigator
         q_heat_loss_cat3(t,cat3)     loss of heat for the refrigator
         q_heat_gain_cat3(t,cat3)     gain of heat for the refrigator
         q_power_cat3(t,cat3)         power used by the refrigator
         q_tmin_cat3(t,cat3)           minimum temperature of the refrigator
         q_tmax_cat3(t,cat3)           maximum temperature of the refrigator


*CAT4
         q_temp_equ_cat4(t)     links heat difference and temperature difference for the house
         q_heat_loss_cat4(t)    loss of heat for the house
         q_heat_gain_cat4(t)    gain of heat for the house
         q_power_cat4(t)        power used by the house
         q_tmin_cat4(t)         minimum temperature of the house
         q_tmax_cat4(t)         maximum temperature of the house
         q_z_max_cat4(t)      minimum power level of the boiler
         q_z_min_cat4(t)      maximum power level of the boiler
*CAT5
         q_power_cat5(t)         power used by the battery
         q_capacity_cat5         maximum capacity of the battery
         q_energy_cat5(t)
         q_penalty(t)
         q_penalty_function
;

q_objective_function..
         objective
                 =e=
                         zcost + penalty_function  ;

q_zcoste..
         zcost
                 =e=
                         sum(t, P_conv(t)*PRICE(t)+Curt(t)*PRICECURT);

q_balance(t)..
         P_conv(t) + RESloc(t)
                 =e=
                         P_cat1(t) + P_cat2(t) + P_cat3(t) + P_cat4(t)+ P_cat5(t) + Curt(t);
q_power_limit(t)..
         P_conv(t)
                 =l=
                         POWER_LIMIT  ;

q_cat1(t)..
         P_cat1(t)
                 =e=
                        D_TOT_CAT1(t);
q_cat2(t)..
         P_cat2(t)
                 =e=
                        sum(cat2, sum(ta$DUR_CAT2(cat2), ti(t-(ord(ta)-1),cat2)*D_CYCLE_CAT2(cat2, ta)));
q_cat3(t)..
         P_cat3(t)
                 =e=
                         sum(cat3,d_cat3(t,cat3));
q_cat4(t)..
         P_cat4(t)
                 =e=
                         d_cat4(t);
q_cat5(t)..
         P_cat5(t)
                 =e=
                         Pin_battery(t) ;



******
*cat2*
******
q_n_cycles_cat2(cat2)..
         N_CYCLES_CAT2(cat2)
                 =e=
                         sum(t$(ord(t)<card(t)-(DUR_CAT2(cat2)-2)),ti(t,cat2));

q_no_overlap(t,cat2)..
         sum(ta$(ord(ta)<=DUR_CAT2(cat2)), ti(t-(ord(ta)-1),cat2))
                 =l=
                         1;



************
****cat3****
************

q_power_cat3(t,cat3)..
         d_cat3(t,cat3)
                 =e=
                         z_cat3(t,cat3)*PCOOL_CAT3(cat3)
                         ;

q_temp_equ_cat3(t,cat3)..
         MASS_CAT3(cat3)*CP*(temp_cat3(t++1,cat3)-temp_cat3(t,cat3))
                 =e=
                         Qin_cat3(t,cat3) - Qout_cat3(t,cat3)   ;

q_heat_loss_cat3(t,cat3)..
         Qout_cat3(t,cat3)
                 =e=
                         (UA_CAT3(cat3))*(temp_cat3(t,cat3) - temp_cat4(t))  ;

q_heat_gain_cat3(t,cat3)..
         Qin_cat3(t,cat3)
                 =e=
                         COP_CAT3(cat3)*z_cat3(t,cat3)*PCOOL_CAT3(cat3)            ;
q_tmin_cat3(t,cat3)..
         temp_cat3(t,cat3)
                 =g=
                         T_MIN_CAT3(cat3);
q_tmax_cat3(t,cat3)..
         temp_cat3(t,cat3)
                 =l=
                         T_MAX_CAT3(cat3);

**********
**HOUSE**
*********


q_power_cat4(t)..
         d_cat4(t)
                 =e=
                         z_cat4(t)*PHEAT_HOUSE ;

q_temp_equ_cat4(t)..
         MASS_HOUSE*cp*(temp_cat4(t++1)-temp_cat4(t))
                 =e=
                         Qin_cat4(t) - Qout_cat4(t)   ;

q_heat_loss_cat4(t)..
         Qout_cat4(t)
                 =e=
                         UA_HOUSE*(temp_cat4(t) - TEMP_AMB(t)) ;
q_heat_gain_cat4(t)..
         Qin_cat4(t)
                 =e=
                         COP_HOUSE*z_cat4(t)*PHEAT_HOUSE           ;
q_tmin_cat4(t)..
         temp_cat4(t)
                 =g=
                         T_MIN_CAT4(t);
q_tmax_cat4(t)..
         temp_cat4(t)
                 =l=
                         T_MAX_CAT4(t);
q_z_max_cat4(t)..
         z_cat4(t)
                 =l=
                         1;
q_z_min_cat4(t)..
         z_cat4(t)
                 =g=
                         0;

********
**CAT5**
********
q_power_cat5(t)..
         Pin_battery(t)
                 =e=
                         Pload_battery * z_cat5(t);
q_capacity_cat5..
          sum(t,Pin_battery(t))
                        =e=
                         Capacity_battery ;
q_energy_cat5(t)..
         energy_cat5(t)
                 =e=
                         sum(tt$(ord(tt)<= ord(t)),Pin_battery(tt));
q_penalty(t)..
         (Capacity_battery*0.2-energy_cat5(t))-u(t)*1000000
                                                 =l=
                                                         0   ;
q_penalty_function..
         penalty_function
                         =e=
                                 sum(t,u(t)*1000000)   ;



Model refrigerator /q_power_cat3, q_temp_equ_cat3, q_heat_loss_cat3,q_heat_gain_cat3,
q_tmin_cat3,q_tmax_cat3/ ;

Model house /q_power_cat4,q_temp_equ_cat4,q_heat_loss_cat4,q_heat_gain_cat4,
q_tmin_cat4,q_tmax_cat4,q_z_max_cat4,q_z_min_cat4,q_cat4/;



Model quarter /all/;

option limrow = 25 ;
option threads = 0;
*quarter.optcr = 0.01;



*Solve fridge using mip minimizing d_cat3 ;

*Solve freezer using mip minimizing dfr_frez ;

*Solve house using mip minimizing cat4_total ;

Solve quarter using mip minimizing objective ;

Display PRICE;


