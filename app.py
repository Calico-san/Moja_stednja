from flask import Flask, jsonify, request, make_response, render_template, redirect, url_for
from datetime import datetime
from pony import orm
from decimal import Decimal

DB = orm.Database()
app = Flask(__name__)

class Transakcija(DB.Entity):
    id = orm.PrimaryKey (int, auto=True)
    namjena = orm.Required(str)
    vrsta_transakcije = orm.Required(str)
    iznos = orm.Required(Decimal, precision=10, scale=2)
    datum = orm.Required(datetime)

DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)


# Prikaz svih transakcija
@app.route("/", methods=["GET"])
def home():
    try:

        vrsta_transakcije = request.args.get('vrsta_transakcije')
        namjena = request.args.get('namjena')
        sort = request.args.get('sort')

        with orm.db_session:
            db_query = orm.select(x for x in Transakcija)

            # Filtriranje po vrsti transakcije
            if vrsta_transakcije:
                db_query = db_query.filter(lambda t: t.vrsta_transakcije == vrsta_transakcije)

            # Filtriranje po namjeni
            if namjena:
                db_query = db_query.filter(lambda t: namjena.lower() in t.namjena.lower())

            # Sortiranje po iznosu i datumu
            if sort == "iznos_asc":
                db_query = db_query.order_by(Transakcija.iznos)
            elif sort == "iznos_desc":
                db_query = db_query.order_by(orm.desc(Transakcija.iznos))
            elif sort == "datum_asc":
                db_query = db_query.order_by(Transakcija.datum)
            elif sort == "datum_desc":
                db_query = db_query.order_by(orm.desc(Transakcija.datum))

            db_query = list(db_query)

            ukupno_uplaceno = sum(x.iznos for x in db_query if x.vrsta_transakcije == 'Uplata')
            ukupno_isplaceno = sum(x.iznos for x in db_query if x.vrsta_transakcije == 'Isplata')
            trenutno_ustedeno = ukupno_uplaceno - ukupno_isplaceno

            results_list = []
            for r in db_query:
                results_list.append(r.to_dict())

            response = {"response": "Success", "data": results_list}
            return make_response(render_template("index.html", transakcije=response["data"], vrsta_transakcije=vrsta_transakcije, namjena=namjena, ukupno_uplaceno=ukupno_uplaceno, ukupno_isplaceno=ukupno_isplaceno, trenutno_ustedeno=trenutno_ustedeno), 200)
    except Exception as e:
        return make_response(jsonify({"response": "Fail", "error": str(e)}), 400)


# Dodavanje nove transakcije
@app.route("/dodaj/transakciju", methods=["POST"])
def dodaj_transakciju():
    try:
        json_request = {}
        for key, value in request.form.items():
            if value == "":
                json_request[key] = None
            else:
                json_request[key] = value

        namjena = json_request["namjena"]
        vrsta_transakcije = json_request["vrsta_transakcije"]
        iznos = Decimal(json_request["iznos"])
        datum = datetime.strptime(json_request["datum"], '%Y-%m-%d')

        with orm.db_session:
            Transakcija(vrsta_transakcije=vrsta_transakcije, namjena=namjena, iznos=iznos, datum=datum)
        return redirect(url_for('home'))
    except Exception as e:
        return make_response(jsonify({"response": "Fail", "error": str(e)}), 400)


# Uređivanje transakcije
@app.route("/transakcija/<int:transakcija_id>", methods=["POST"])
def uredi_transakciju(transakcija_id):
    try:
        json_request = {}
        for key, value in request.form.items():
            if value == "":
                json_request[key] = None
            else:
                json_request[key] = value

        namjena = json_request["namjena"]
        vrsta_transakcije = json_request["vrsta_transakcije"]
        iznos = Decimal(json_request["iznos"])
        datum = datetime.strptime(json_request["datum"], '%Y-%m-%d')

        with orm.db_session:
            to_update = Transakcija[transakcija_id]
            to_update.vrsta_transakcije = vrsta_transakcije
            to_update.namjena = namjena
            to_update.iznos = iznos
            to_update.datum = datum

        return redirect(url_for('home'))
    except Exception as e:
        return make_response(jsonify({"response": "Fail", "error": str(e)}), 400)


# Brisanje transakcije
@app.route("/transakcija/<int:transakcija_id>", methods=["DELETE"])
def obrisi_transakciju(transakcija_id):
    try:
        with orm.db_session:
            to_delete = Transakcija[transakcija_id]
            to_delete.delete()
            response = {"response": "Success"}
            return make_response(jsonify(response), 200)
    except orm.ObjectNotFound as e:
        return make_response(
            jsonify({"response": "Fail", "error": f"Transakcija s ID brojem {transakcija_id} nije nađena"}), 404)
    except Exception as e:
        return make_response(jsonify({"response": "Fail", "error": str(e)}), 400)


# Grafovi
@app.route('/vizualizacija', methods=['GET'])
def vizualizacija():
    try:
        graph_type = request.args.get('graph_type', 'uplate')  # Default je uplate
        labels = []
        data = []

        with orm.db_session:
            if graph_type == 'uplate':
                query = orm.select((t.namjena, float(sum(t.iznos))) for t in Transakcija if t.vrsta_transakcije == 'Uplata')
                results = dict(query)
                labels = list(results.keys())
                data = list(results.values())

            elif graph_type == 'isplate':
                query = orm.select((t.namjena, float(sum(t.iznos))) for t in Transakcija if t.vrsta_transakcije == 'Isplata')
                results = dict(query)
                labels = list(results.keys())
                data = list(results.values())

            elif graph_type == 'stednja':
                uplate_query = orm.select((t.namjena, float(sum(t.iznos))) for t in Transakcija if t.vrsta_transakcije == 'Uplata')
                uplate = dict(uplate_query)

                isplate_query = orm.select((t.namjena, float(sum(t.iznos))) for t in Transakcija if t.vrsta_transakcije == 'Isplata')
                isplate = dict(isplate_query)

                results = {}
                for namjena, iznos in uplate.items():
                    results[namjena] = iznos

                for namjena, iznos in isplate.items():
                    if namjena in results:
                        results[namjena] -= iznos
                    else:
                        results[namjena] = -iznos

                labels = list(results.keys())
                data = [value for value in results.values()]  # Štednja ne može biti negativna

        return render_template('vizualizacija.html', labels=labels, data=data, graph_type=graph_type)

    except Exception as e:
        error_response = {"response": "Error", "error_message": str(e)}
        return make_response(jsonify(error_response), 500)


if __name__ == "__main__":
    app.run(port=8080, host='0.0.0.0', debug=True)
