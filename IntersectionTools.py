import Rhino
import scriptcontext
from Smart import SmartFeature

from Rhino.Geometry import Vector3d

def SmartCurveLayerProject(curveLayerName, surfaceLayerName,
        objectAttributes=None, vector=Vector3d(0.0,0.0,1.0),
        tolerance=0.001):
    '''Project a layer contining only curves onto a layer containing a surface,
    and maintain UserString associations between the original and projected curves.
    ObjectAttributes can be passed in to predetermine a layer or other data. Returns
    a list of (Geometry, ObjAttributes) pairs, with user keys set. If anything fails,
    should print an error message and return an empty set.'''
    # get the curves
    objs = scriptcontext.doc.Objects.FindByLayer(curveLayerName)
    if len(objs) == 0:
        print 'No Curves found on that layer'
        return []
    # get the surface(s)
    srfObjs = scriptcontext.doc.Objects.FindByLayer(surfaceLayerName)
    if len(srfObjs) == 0:
        print 'no surfaces found on that layer'
        return []
    else:
        srf = srfObjs[0].Geometry
    # deal with ObjectAttributes
    if objectAttributes:
        att = objectAttributes
    else:
        att = Rhino.DocObjects.ObjectAttributes()
    resultSet = []
    # project everything
    for crvObj in objs:
        smartCurve = SmartFeature(crvObj)
        smartAtt = smartCurve.objAttributes(att)
        projCurves = smartCurve.geom.ProjectToBrep(smartCurve.geom,
                                                srf,
                                                vector,
                                                tolerance)
        for crv in projCurves:
            smartPair = (crv, smartAtt)
            resultSet.append(smartPair)

    return resultSet

