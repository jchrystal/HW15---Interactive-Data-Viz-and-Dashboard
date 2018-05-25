# import necessary libraries
import numpy as np
from flask import (
    Flask,
    render_template,
    jsonify,
    request)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Database Setup
#################################################
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

OTU = Base.classes.otu

Samples = Base.classes.samples

Samples_Metadata = Base.classes.samples_metadata

session = Session(engine)

@app.route("/")
def home():
    return jsonify(Base.classes.keys())


@app.route('/otu')
def otu_list():
    results = session.query(OTU.lowest_taxonomic_unit_found).all()

    otu_list = []

    for result in results:
        otu_list.append(result)
    
    return jsonify(otu_list)

@app.route('/names')
def names():
    results = session.query(Samples_Metadata.SAMPLEID).all()
    
    names = []
    for result in results:
        names.append("BB_"+str(result[0]))

    return jsonify(names)

@app.route('/metadata/<sample>')
def metadata(sample):
    dict_ = {}
    for row in session.query(Samples_Metadata).filter(Samples_Metadata.SAMPLEID==sample[3:]):
        dict_['AGE'] = row.AGE
        dict_['BBTYPE'] = row.BBTYPE
        dict_['ETHNICITY'] = row.ETHNICITY
        dict_['GENDER'] = row.GENDER
        dict_['LOCATION'] = row.LOCATION
        dict_['SAMPLEID'] = row.SAMPLEID
    return jsonify(dict_)

@app.route('/wfreq/<sample>')
def wfreq_int(sample):
    
    for result in session.query(Samples_Metadata.WFREQ).filter(Samples_Metadata.SAMPLEID==sample[3:]):
        wfreq = result[0]

    return jsonify(wfreq)

@app.route('/samples/<sample>')
def samples(sample):
    


if __name__ == "__main__":
    app.run(debug=True)