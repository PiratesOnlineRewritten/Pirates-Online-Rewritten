from pirates.teleport.DistributedFSMBase import DistributedFSMErrors

class TeleportErrors(DistributedFSMErrors):
    Undefined = DistributedFSMErrors.Undefined
    Timeout = Undefined
    Undefined += 1
    Disconnect = Undefined
    Undefined += 1
    Aborted = Undefined
    Undefined += 1
    Interrupted = Undefined
    Undefined += 1