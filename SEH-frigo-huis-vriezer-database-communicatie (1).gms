$onempty
$GDXIN %SupplyDataFileName%
Sets
         t time period
         app   appliances of category three
         cat4   appliances of category four  /heat_house1,heat_house2/
$ LOAD t, app
;

Parameters

         TEMP_AMB(t)     Temperature of the environment (in K) -> time

         UA_REF(app)     isolation constant of the refrigator
         COP_REF(app)    coefficient of performance of the refrigator
         PCOOL_REF(app)  power needed for the refrigator
         MASS_REF(app)   mass of the cooled air inside the refrigator
$ LOAD TEMP_AMB, UA_REF, COP_REF, PCOOL_REF, MASS_REF
;

Variables
         Qin_ref(t)      Heat we put in the refrigator (neg.)
         Qout_ref(t)     Heat which escapes from the refrigator
         temp_ref(t)     Temperature of the refrigator(in K)
         dfr_ref         Power consumated by the refrigator


         dfr_total       Total power used by the quarter
*                                                (quarter = wijk )
         ;

binary variables
          zfr_ref(t)  Defines whether the refrigator is on or off
;


Scalar CP thermodynamic coeficient /1.005/;

Equations
         q_temp_equ_ref(t,app)       links heat difference and temperature difference for the refrigator
         q_heat_loss_ref(t,app)      loss of heat for the refrigator
         q_heat_gain_ref(t,app)      gain of heat for the refrigator
         q_power_ref(app)             power used by the refrigator
         q_tmin_ref(t)           minimum temperature of the refrigator
         q_tmax_ref(t)           maximum temperature of the refrigator

         q_temp_equ_frez(t)       links heat difference and temperature difference for the refrigator
         q_heat_loss_frez(t)      loss of heat for the refrigator
         q_heat_gain_frez(t)      gain of heat for the refrigator
         q_power_frez             power used by the refrigator
         q_tmin_frez(t)           minimum temperature of the refrigator
         q_tmax_frez(t)           maximum temperature of the refrigator

         q_temp_equ_house(t)     links heat difference and temperature difference for the house
         q_heat_loss_house(t)    loss of heat for the house
         q_heat_gain_house(t)    gain of heat for the house
         q_power_house           power used by the house
         q_tmin_house(t)         minimum temperature of the house
         q_tmax_house(t)         maximum temperature of the house
         q_zfr_max_house(t)      minimum power level of the boiler
         q_zfr_min_house(t)      maximum power level of the boiler

         q_total_power_use       total power used by the quarter
;


************
*refrigator*
************

q_power_ref(app)..
         dfr_ref
                 =e=
                         sum(t, zfr_ref(t)*PCOOL_REF(app))
                         ;

q_temp_equ_ref(t,app)..
         MASS_REF(app)*CP*(temp_ref(t++1)-temp_ref(t))
                 =e=
                         Qin_ref(t) - Qout_ref(t)   ;

q_heat_loss_ref(t,app)..
         Qout_ref(t)
                 =e=
                         UA_REF(app)*(temp_ref(t) - 290)  ;

q_heat_gain_ref(t,app)..
         Qin_ref(t)
                 =e=
                         COP_REF(app)*zfr_ref(t)*PCOOL_REF(app)            ;
q_tmin_ref(t)..
         temp_ref(t)
                 =g=
                         270;
q_tmax_ref(t)..
         temp_ref(t)
                 =l=
                         277;



Model fridge /q_power_ref, q_temp_equ_ref, q_heat_loss_ref,q_heat_gain_ref,
q_tmin_ref,q_tmax_ref/ ;

Model freezer /q_temp_equ_frez,q_power_frez,q_heat_loss_frez,q_heat_gain_frez,
q_tmin_frez,q_tmax_frez/;

Model house /q_power_house,q_temp_equ_house,q_heat_loss_house,q_heat_gain_house,
q_tmin_house,q_tmax_house,q_zfr_max_house,q_zfr_min_house/;

Model quarter /all/;

option limrow = 25 ;

Solve fridge using mip minimizing dfr_ref ;

*Solve freezer using mip minimizing dfr_frez ;

*Solve house using mip minimizing dfr_house ;

*Solve quarter using mip minimizing dfr_total ;
