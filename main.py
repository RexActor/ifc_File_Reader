import pathlib
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util
import ifcopenshell.util.element
import json
from flask import Flask, render_template

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

final_result = {}


def GetIfcInformation():
    rebar_Each = {}
    rebar_values = {}
    rebar_main = {}
    for beam in geometries.by_type(geometry_beam_name):

        if beam.Name == 'BEAM':

            count = 1
            for rebrar in ifcopenshell.util.element.get_parts(beam):

                if rebrar.Name == 'REBAR':

                    rebar_Each[f'{rebrar.Name}-{count}'] = rebrar[0]

                    rebar_values[f'{rebrar[0]}'] = ifcopenshell.util.element.get_psets(
                        rebrar)
                    rebar_main[f'{rebrar.Name}-{count}'] = rebar_values
                    count = count+1

                    rebar_values = {}

        final_result[f'{beam[7]}'] = rebar_main
        rebar_Each = {}
        rebar_main = {}

    return final_result


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("/index.html")


@app.route('/result', methods=['POST', 'GET'])
def result():
    GetIfcInformation()
    result = final_result

    with open(f"{rootPath}/hmm.json", "w") as file:
        json.dump(final_result, file)
    return render_template("result.html", result=result)


if "__name__" == "__main__":
    app.run(debug=True)
