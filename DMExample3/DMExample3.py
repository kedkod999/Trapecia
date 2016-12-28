import units

def createMyFeature(ag):
    AA = ExtAPI.CreateFeature("OctaFeature")

def generateOctagonGeom(feature,fct):

    # This command writes messages to log file...
	ExtAPI.Log.WriteMessage("Generating MyFeature...")    
    
    # Collect all property values in meter unit
	fromUnit, toUnit = ExtAPI.DataModel.CurrentUnitFromQuantityName("Length"), "m"
    
    # Get span of the Octagon from "Span" property and convert it to present unit system
	Niz = units.ConvertUnit(feature.Properties["Niz"].Value, fromUnit, toUnit)
	Ver = units.ConvertUnit(feature.Properties["Ver"].Value, fromUnit, toUnit)
	Sdvid = units.ConvertUnit(feature.Properties["Sdvid"].Value, fromUnit, toUnit)
	H = units.ConvertUnit(feature.Properties["H"].Value, fromUnit, toUnit)
	Width = units.ConvertUnit(feature.Properties["Width"].Value, fromUnit, toUnit)
	Radius = units.ConvertUnit(feature.Properties["Radius"].Value, fromUnit, toUnit)
    
    # Calculate side length of octagon
	x1=0.
	y1=0.
	x2=Sdvid
	y2=H
	x3=Sdvid+Ver
	y3=H
	x4=Niz
	y4=0.
    
    # Declare variables...
	bodies=[]
	bodies1=[]
	bodies2=[]
	builder = ExtAPI.DataModel.GeometryBuilder
        
	ExtAPI.Log.WriteMessage("Operations.Extrude")
	polGen = builder.Primitives.Sheet.CreatePolygon([x1,y1,0.,x2,y2,0.,x3,y3,0.,x4,y4,0.])
	bPol = polGen.Generate()
	extrude = builder.Operations.CreateExtrudeOperation([0.,0.,1.],Width)
	bodies = extrude.ApplyTo(bPol)
	feature.Bodies = bodies
	
	primitive = ExtAPI.DataModel.GeometryBuilder.Primitives
	cylinder = primitive.Solid.CreateCylinder([Niz/2.,H/2.,0.],[0.,0.,Width],Radius)
	bCyl1 = cylinder.Generate()
	bodies1.Add(bCyl1)
	feature.Bodies = bodies1
	feature.MaterialType = MaterialTypeEnum.Freeze
	
	extrudeOperation = builder.Operations.CreateSubtractOperation(bodies1)
	bodies2 = extrudeOperation.ApplyTo(bodies)
	feature.Bodies = bodies2
	feature.MaterialType = MaterialTypeEnum.Freeze

	return True
