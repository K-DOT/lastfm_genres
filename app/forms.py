from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField
from wtforms.validators import Required


class MainForm(Form):
    choices = [('7days', '7 Days'), ('1month', '1 Month'), ('3month', '3 Months'), ('6month', '6 Months'), ('12month', '12 Months'), ('overall', 'Overall')]
    username = TextField('Username', validators = [Required()])
    period = SelectField('Period', choices=choices)
    limit = TextField('Username', validators = [Required()], default="50")