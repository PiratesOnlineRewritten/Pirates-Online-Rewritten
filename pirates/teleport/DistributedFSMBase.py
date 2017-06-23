from direct.fsm.FSM import FSM, FSMException, AlreadyInTransition, RequestDenied

class DistributedFSMBase(FSM):
    pass


class DistributedFSMErrors():
    Undefined = 0
    Success = Undefined
    Undefined += 1
    InTransition = Undefined
    Undefined += 1
    RequestDenied = Undefined
    Undefined += 1
    AlreadyInState = Undefined
    Undefined += 1