import recastdb.models as dbmodels
from recastdb.database import db

def createAnalysisFromForm(app,form,current_user):
  with app.app_context():
    user_query = dbmodels.User.query.filter(dbmodels.User.name == current_user.name()).all()
    assert len(user_query)==1
    

    analysis = dbmodels.Analysis(owner_id = user_query[0].id,
        description_of_original_analysis = form.analysis_description.data,
        run_condition_id = int(form.run_condition_choice.data)
        )

    db.session.add(analysis)
    db.session.commit()