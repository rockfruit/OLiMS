from dependencies.dependency import ClassSecurityInfo
from dependencies.dependency import DateTime
from dependencies.dependency import schemata
from dependencies.dependency import RecordsField
from dependencies import atapi
from dependencies.dependency import *
from dependencies.dependency import HoldingReference
from dependencies.dependency import getToolByName
from dependencies.dependency import safe_unicode
from lims import bikaMessageFactory as _
from lims.utils import t
from lims.browser.widgets import ScheduleInputWidget
from lims.config import PROJECTNAME
from lims.content.bikaschema import BikaSchema

schema = BikaSchema.copy() + Schema((

    ReferenceField('Instrument',
        allowed_types=('Instrument',),
        relationship='InstrumentScheduledTaskInstrument',
        widget=StringWidget(
            visible=False,
        )
    ),

    ComputedField('InstrumentUID',
        expression = 'context.getInstrument() and context.getInstrument().UID() or None',
        widget=ComputedWidget(
            visible=False,
        ),
    ),

    StringField('Type',
        vocabulary = "getTaskTypes",
        widget = ReferenceWidget(
            checkbox_bound = 0,
            label = _("Task type",
                      "Type"),
        ),
    ),

    RecordsField('ScheduleCriteria',
        required=1,
        type='schedulecriteria',
        widget=ScheduleInputWidget(
            label=_("Criteria"),
        ),
    ),

    TextField('Considerations',
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            label=_("Considerations"),
            description=_("Remarks to take into account before performing the task"),
        ),
    ),
))

IdField = schema['id']
schema['description'].required = False
schema['description'].widget.visible = True
schema['description'].schemata = 'default'
schema.moveField('description', before='Considerations')

# Title is not needed to be unique
schema['title'].validators = ()
schema['title']._validationLayer()

class InstrumentScheduledTask(BaseFolder):
    security = ClassSecurityInfo()
    schema = schema
    displayContentsTab = False

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def getTaskTypes(self):
        """ Return the current list of task types
        """
        types = [('Calibration', safe_unicode(_('Calibration')).encode('utf-8')),
                 ('Enhancement', safe_unicode(_('Enhancement')).encode('utf-8')),
                 ('Preventive',safe_unicode(_('Preventive')).encode('utf-8')),
                 ('Repair', safe_unicode(_('Repair')).encode('utf-8')),
                 ('Validation', safe_unicode(_('Validation')).encode('utf-8'))]

        return DisplayList(types)

    def getCriteria(self):
        criteria = "";
        criterias = self.getScheduleCriteria()
        if criterias and len(criterias) > 0:
            crit = criterias[0]
            if crit['fromenabled'] == True and crit['fromdate']:
                criteria += _('From') + " " + crit['fromdate'] + " "
            if crit['repeatenabled'] == True and crit['repeatunit'] and crit['repeatperiod']:
                criteria += _("repeating every") + " " + crit['repeatunit'] + " " + _(crit['repeatperiod']) + " "
            if crit['repeatuntilenabled'] == True and crit['repeatuntil']:
                criteria += _("until") + " " + crit['repeatuntil']
        return criteria;

atapi.registerType(InstrumentScheduledTask, PROJECTNAME)
