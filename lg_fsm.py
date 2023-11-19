
def Error(fsm):
    #print 'That does not compute.',
    #print fsm.state_changes
    pass
    
def Period(fsm):
    #print str(fsm.memory.pop())
    #print 'period(%d)' % (fsm.counter)
    return ['period', fsm.counter]

def Root(fsm):
    fsm.counter = fsm.counte