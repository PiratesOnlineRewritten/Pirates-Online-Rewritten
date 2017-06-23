

def getAcuteAngle(angle1, angle2):
    angle1 = getNormalizedAngle(angle1)
    angle2 = getNormalizedAngle(angle2)
    angleDifference = (angle1 - angle2) % 360
    if angleDifference == 0:
        return 0
    if abs(angleDifference) > 180:
        sign = angleDifference / abs(angleDifference)
        angleDifference = (angleDifference - 360) * sign
    return angleDifference


def getNormalizedAngle(angle):
    angle %= 360
    if angle < 0:
        angle = (360 + angle) % 360
    return angle