import pathlib
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util
import ifcopenshell.util.element
import json

rootPath = pathlib.Path(__file__).parent.resolve()
fileName = "File/test.ifc"
geometries = ifcopenshell.file.from_string(
    open(f'{rootPath}/{fileName}').read())
slabs = geometries.by_type('IfcSlab')  # get amount of "slabs"
singleSlab = slabs[0]
reinforcingBars = geometries.by_type('IfcReinforcingBar')
singleBarClass = reinforcingBars[0]

geometry_beam_name = 'IfcElementAssembly'
geometry_slab_name = 'IfcSlab'
geometry_bar_name = 'IfcReinforcingBar'

collected_Data = {}


def GetIfcInformation():
    for geometry in geometries:
        if geometry.is_a(geometry_beam_name):
            for subItem in geometries[geometry]:
                print(subItem)

                if geometry.is_a(geometry_bar_name):

                    collected_Data[f'{geometry[0]}'] = ifcopenshell.util.element.get_psets(
                        geometry)


rebar_dict = {}
rebar_values = {}
final_result = {}


for beam in geometries.by_type(geometry_beam_name):

    if beam.Name == 'BEAM':

        count = 1
        for rebrar in ifcopenshell.util.element.get_parts(beam):

            if rebrar.Name == 'REBAR':

                rebar_dict[f'{rebrar.Name}-{count}'] = rebrar[0]
                print(rebrar[0])
                rebar_values[f'{beam[7]}'] = ifcopenshell.util.element.get_psets(
                    rebrar)

                rebar_values = {}
                count = count+1
                rebar_dict[f'{rebrar[0]}'] = rebar_values

            final_result[f'{beam[7]}'] = rebar_dict
    rebar_dict = {}

with open(f"{rootPath}/hmm.json", "w") as file:
    json.dump(final_result, file)
