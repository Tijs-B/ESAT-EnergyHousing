$onempty
$GDXIN %SupplyDataFileName%
Sets
         t       time period /T01*T96/
         tw      Quarters that are not allowed to have the first part of the power curve of the washing machine /T01*T30,T70*T96/
         tlim(t) /T01/
         i       /0*2/
         cat1    appliances of category one
         cat2    appliances of category two
         cat3    appliances of category three
         cat4    appliances of category four
;
$LOAD cat1 cat2 cat3 cat4
ALIAS(t,ta);

Parameters
*        Global
         TEMP_AMB(t)     Temperature of the environment (in K) -> time
         PRICE(t)        price of energy
         RESLOC(t)       local supply of renewables

*        Cat1
         DCAT1(t)         catgeory 1 demand (fixed)


*        Cat2
         CYC_CAT2(cat2,ta)         demand of washing machine

*        Cat3
         UA_CAT3(cat3)          isolation constant of the refrigator
         COP_CAT3(cat3)         coefficient of performance of the refrigator
         PCOOL_CAT3(cat3)       power needed for the refrigator
         MASS_CAT3(cat3)        mass of the cooled air inside the refrigator


*        Cat4
         UA_CAT4(cat4)        isolation constant of the house
         COP_CAT4(cat4)       coefficient of performance of the house
         PHEAT_CAT4(cat4)     power needed for the boiler of the house
         MASS_CAT4(cat4)      mass of the heated air inside the house
;

SCALARS
         tstep            time step simulation [h]        /900/
         PRICECURT        price of curtailing RES [€]     /45/
         wmnc             number of cycles washing machine/1/
         wmn              number of washing machines      /1/
         wmdur            duration of wm cycle
         Tend             end time                        /10/
;
$LOAD PRICE RESLOC DCAT1 CYC_CAT2 UA_CAT3 COP_CAT3 PCOOL_CAT3 MASS_CAT3 UA_CAT4 COP_CAT4 PHEAT_CAT4 MASS_CAT4

wmdur = card(CYC_CAT2);


Variables
         zcost           Objective the energycost
*cat3
         Qin_CAT3(cat3,t)      Heat we put in the refrigator (neg.)
         Qout_CAT3(cat3,t)     Heat which escapes from the refrigator
         temp_CAT3(cat3,t)     Temperature of the refrigator(in K)
         dfr_CAT3(cat3,t)      Power consumated by the refrigator

*cat4
         Qin_CAT4(cat4,t)    Heat we put in the house (neg.)
         Qout_CAT4(cat4,t)   Heat which escapes from the house
         temp_CAT4(cat4,t)   Temperature of the house (in K)
         dfr_CAT4(cat4,t)    Power consumated by the house
         z_cat4(cat4,t)    Defines at which % the boiler is using power to heat

         dfr_total       Total power used by the quarter
*         cat4_total      total of cat4
*                                                (quarter = wijk )
         ;

POSITIVE VARIABLES
Ptot_conv(t)        Conventional power supply
Ptot_cat1(t)        Demand of appliances of category 1
Ptot_cat2(t)        Demand of appliances of category 2
Ptot_cat3(t)        Demand of appliances of category 3
Ptot_cat4(t)        Demand of appliances of category 4
Curt(t)              Curtailed local renewable energy
z_cat4(cat4,t)     Defines whether the heating is on or off
;

INTEGER VARIABLES
ti(t)            Start time for cycle
;

binary variables
          zfr_CAT3(cat3,t)  Defines whether the refrigator is on or off
;


TEMP_AMB(t) = 273;

Scalar CP thermodynamic coeficient /1.005/;

Equations

*GLOBAL
         q_zcoste                 Objective function cost
         q_balance(t)             Electricity balance
         q_cat1(t)                Demand for appliances of category 1
         q_cat2(t)                Demand for appliances of category 2
         q_cat3(t)                Demand for appliances of category 3
         q_cat4(t)                Demand for appliances of category 4

*CAT2
         wmnceq                  Ensure the dishwasher works the needed amount of cycles
         wmneq(t)                Ensure number of cycles running simultaneously is limited to number of washing machines
*CAT3
         q_temp_equ_CAT3(cat3,t)       links heat difference and temperature difference for the refrigator
         q_heat_loss_CAT3(cat3,t)      loss of heat for the refrigator
         q_heat_gain_CAT3(cat3,t)      gain of heat for the refrigator
         q_power_CAT3(cat3,t)          power used by the refrigator
         q_tmin_CAT3(cat3,t)           minimum temperature of the refrigator
         q_tmax_CAT3(cat3,t)           maximum temperature of the refrigator

*CAT
         q_temp_equ_CAT4(cat4,t)     links heat difference and temperature difference for the house
         q_heat_loss_CAT4(cat4,t)    loss of heat for the house
         q_heat_gain_CAT4(cat4,t)    gain of heat for the house
         q_power_CAT4(cat4,t)        power used by the house
         q_tmin_CAT4(cat4,t)         minimum temperature of the house
         q_tmax_CAT4(cat4,t)         maximum temperature of the house
         q_zfr_max_CAT4(cat4,t)      minimum power level of the boiler
         q_zfr_min_CAT4(cat4,t)      maximum power level of the boiler


;


q_zcoste..
         zcost
                 =e=
                         sum(t, P_conv(t)*PRICE(t)+Curt(t)*PRICECURT);

q_balance(t)..
         Ptot_conv(t) + RESloc(t)
                 =e=
                         P_cat1(t) + P_cat2(t) + P_cat3(t) + P_cat4(t) + Curt(t);

q_cat1(t)..
         Ptot_cat1(t)
                 =e=
                         DCAT1(t)  ;
q_cat2(t,cat2)..
         Ptot_cat2(t)
                 =e=
                         sum(cat2,sum(ta$CYC_CAT2, ti(t-(ord(ta)-1))*CYC_CAT2(cat2,ta)));
q_cat3(t,cat3)..
         Ptot_cat3(t)
                 =e=
                         sum(cat3,dfr_CAT3(cat3,t));
q_cat4(tcat4)..
         Ptot_cat4(t)
                 =e=
                         sum(cat4,dfr_CAT4(cat4,t));



******
*cat2*
******
wmnceq..
         wmnc
                 =e=
                         sum(t$(ord(t)<card(t)-(wmdur-2)),ti(t));
wmneq(t)..
         sum(ta, ti(t-(ord(ta)-1)))
                 =l=
                         wmn;



************
*refrigator*
************

q_power_CAT3(cat3,t)..
         dfr_CAT3(cat3,t)
                 =e=
                         zfr_CAT3(cat3,t)*PCOOL_CAT3(cat3)/4
                         ;

q_temp_equ_CAT3(cat3,t)..
         MASS_CAT3(cat3)*CP*(temp_CAT3(cat3,t++1)-temp_CAT3(cat3,t))
                 =e=
                         Qin_CAT3(cat3,t) - Qout_CAT3(cat3,t)   ;

q_heat_loss_CAT3(cat3,t)..
         Qout_CAT3(cat3,t)
                 =e=
                         UA_CAT3(cat3)/4*(temp_CAT3(cat3,t) - temp_CAT4(cat4,t))  ;

q_heat_gain_CAT3(cat3,t)..
         Qin_CAT3(cat3,t)
                 =e=
                         COP_CAT3(cat3)*zfr_CAT3(cat3,t)*PCOOL_CAT3(cat3)/4            ;
q_tmin_CAT3(cat3,t)..
         temp_CAT3(cat3,t)
                 =g=
                         270;
q_tmax_CAT3(cat3,t)..
         temp_CAT3(cat3,t)
                 =l=
                         277;

**********
**HOUSE**
*********


q_power_CAT4(cat4,t)..
         dfr_CAT4(cat4,t)
                 =e=
                         z_cat4(cat4,t)*PHEAT_CAT4(cat4)/4 ;

q_temp_equ_CAT4(cat4,t)..
         MASS_CAT4(cat4)*cp*(temp_CAT4(cat4,t++1)-temp_CAT4(cat4,t))
                 =e=
                         Qin_CAT4(cat4,t) - Qout_CAT4(cat4,t)   ;

q_heat_loss_CAT4(cat4,t)..
         Qout_CAT4(cat4,t)
                 =e=
                         UA_CAT4(cat4)/4*(temp_CAT4(cat4,t) - TEMP_AMB(t)) ;
q_heat_gain_CAT4(cat4,t)..
         Qin_CAT4(cat4,t)
                 =e=
                         COP_CAT4(cat4)*z_cat4(cat4,t)*PHEAT_CAT4(cat4)/4            ;
q_tmin_CAT4(cat4,t)..
         temp_CAT4(cat4,t)
                 =g=
                         292;
q_tmax_CAT4(cat4,t)..
         temp_CAT4(cat4,t)
                 =l=
                         296;
q_zfr_max_CAT4(cat4,t)..
         z_cat4(cat4,t)
                 =l=
                         1;
q_zfr_min_CAT4(cat4,t)..
         z_cat4(cat4,t)
                 =g=
                         0;




Model fridge /q_power_CAT3(cat3), q_temp_equ_CAT3(cat3), q_heat_loss_CAT3(cat3),q_heat_gain_CAT3(cat3),
q_tmin_CAT3(cat3),q_tmax_CAT3(cat3)/ ;

Model house /q_power_CAT4(cat4),q_temp_equ_CAT4(cat4),q_heat_loss_CAT4(cat4),q_heat_gain_CAT4(cat4),
q_tmin_CAT4(cat4),q_tmax_CAT4(cat4),q_zfr_max_CAT4(cat4),q_zfr_min_CAT4(cat4),q_cat4/;



Model quarter /all/;

option limrow = 25 ;



*Solve fridge using mip minimizing dfr_CAT3(cat3) ;

*Solve freezer using mip minimizing dfr_frez ;

*Solve house using mip minimizing cat4_total ;

Solve quarter using mip minimizing zcost ;

Display PRICE
