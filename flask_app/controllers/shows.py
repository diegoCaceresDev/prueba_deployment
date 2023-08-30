from flask import render_template, flash, redirect, session, request
from flask_app import app
from flask_app.models.shows import Show



@app.route('/')
def inicio():

    if 'usuario' not in session:
        flash("Debes iniciar sesion", "error")
        return redirect("/login")


    return redirect("/shows/")

@app.route('/shows/')
def shows():

    if 'usuario' not in session:
        flash("Debes iniciar sesion", "error")
        return redirect("/login")

    shows = Show.get_all()
    print(shows[0])
    return render_template(
        'dashboard/inicio.html', shows=shows
    )

@app.route('/new_shows/')
def new_show():
    
    return render_template("/dashboard/new_show.html")


@app.route('/add_show/', methods=["post"])
def add_show():
    
    errores = Show.validar(request.form)
    if len(errores) > 0:
        for error in errores:
            flash(error, "error")
        return redirect("/login")
        
    data= {
        'title': request.form['title'],
        'network': request.form['network'],
        'description': request.form['description'],
        'released_date': str(request.form['released_date']),
        'user_id': session['usuario']['id']
    }
    
    Show.save(data)
    
    return redirect('/shows/')


@app.route('/shows/<int:id>')
def show_by_id(id):
    
    show = Show.get_by_id(id)
    
    return render_template("/dashboard/show.html", show  = show)


@app.route('/shows/delete/<int:id>')
def delete_by_id(id):
    
    Show.delete(id)
    flash("El show fue eliminado correctamente", "error")

    return redirect("/shows/")


@app.route('/shows/edit/<int:id>')
def edit_show(id):
    
    show = Show.get_by_id(id)
    
    return render_template("dashboard/edit_show.html", show = show)


@app.route('/edit/<id>', methods=["post"])
def edit_by_id(id):
    
    errores = Show.validar(request.form)
    if len(errores) > 0:
        for error in errores:
            flash(error, "error")
        return redirect("/login")
        
    
    data= {
        'title': request.form['title'],
        'network': request.form['network'],
        'description': request.form['description'],
        'released_date': request.form['released_date'],
        'id': id
    }
    
    Show.update(data)
    
    flash(data['title'] + " fue actualizado correctamente", "success")
    return redirect("/shows/")    
