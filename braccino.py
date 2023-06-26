def dancing(timer):
    import maestro
    import time 
    servo = maestro.Controller()
    t0=time.time()
    while time.time()-t0 < timer:
        servo.setTarget(1, 6000) #spalla sinistra da davanti
        servo.setTarget(3, 7000) #spalla destra da davanti

        servo.setTarget(2, 7000) #gomito sinistro
        servo.setTarget(0, 4000)
        servo.setTarget(4, 500)#braccio destro
        servo.setTarget(5, 8000)#gomito destro

        time.sleep(1)

        servo.setTarget(2, 7000) #gomito sinistro
        servo.setTarget(0, 8000)
        servo.setTarget(4, 8000)#braccio destro
        servo.setTarget(5, 6000)#gomito destro

        time.sleep(1)
    servo.close()

