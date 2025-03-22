
class OverArch:
    def __init__(self, password):
        self.BadRB = BadmintonRegBot(password)

    def FridayBadmintonLoop(self):
        self.sch = sched.Scheduler()
        self.sch.schedule_task('sunday', '14:24', 3, 'seconds', self.BadRB.navigate)