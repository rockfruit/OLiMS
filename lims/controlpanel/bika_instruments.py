from dependencies.dependency import ClassSecurityInfo
from dependencies.dependency import schemata
from dependencies import atapi
from dependencies.dependency import registerType
from dependencies.dependency import permissions
from dependencies.dependency import getToolByName
from lims.browser import BrowserView
from lims.browser.bika_listing import BikaListingView
from lims.config import PROJECTNAME
from lims import bikaMessageFactory as _
from lims.utils import t
from lims.content.bikaschema import BikaFolderSchema
from lims.interfaces import IInstruments
from dependencies.dependency import IViewView
from dependencies.dependency import IFolderContentsView
from dependencies.folder import ATFolder, ATFolderSchema
from dependencies.dependency import implements
from operator import itemgetter

class InstrumentsView(BikaListingView):
    implements(IFolderContentsView, IViewView)
    def __init__(self, context, request):
        super(InstrumentsView, self).__init__(context, request)
        self.catalog = 'bika_setup_catalog'
        self.contentFilter = {'portal_type': 'Instrument',
                              'sort_on': 'sortable_title'}
        self.context_actions = {_('Add'):
                                {'url': 'createObject?type_name=Instrument',
                                 'icon': '++resource++bika.lims.images/add.png'}}
        self.title = self.context.translate(_("Instruments"))
        self.icon = self.portal_url + "/++resource++bika.lims.images/instrument_big.png"
        self.description = ""
        self.show_sort_column = False
        self.show_select_row = False
        self.show_select_column = True
        self.pagesize = 25
        
        self.columns = {
            'Title': {'title': _('Instrument'),
                      'index': 'sortable_title'},
            'Type': {'title': _('Type'),
                     'index': 'getInstrumentTypeName',
                     'toggle': True,
                     'sortable': True},
            'Brand': {'title': _('Brand'),
                      'toggle': True},
            'Model': {'title': _('Model'),
                      'index': 'getModel',
                      'toggle': True},
            'ExpiryDate': {'title': _('Expiry Date'),
                           'toggle': True},
            'WeeksToExpire': {'title': _('Weeks To Expire'),
                           'toggle': False},
            'Method': {'title': _('Method'),
                           'toggle': True},
            }

        self.review_states = [
            {'id':'default',
             'title': _('Active'),
             'contentFilter': {'inactive_state': 'active'},
             'transitions': [{'id':'deactivate'}, ],
             'columns': ['Title',
                         'Type',
                         'Brand',
                         'Model',
                         'ExpiryDate',
                         'WeeksToExpire',
                         'Method']},
            {'id':'inactive',
             'title': _('Dormant'),
             'contentFilter': {'inactive_state': 'inactive'},
             'transitions': [{'id':'activate'}, ],
             'columns': ['Title',
                         'Type',
                         'Brand',
                         'Model',
                         'ExpiryDate',
                         'WeeksToExpire',
                         'Method']},
            {'id':'all',
             'title': _('All'),
             'contentFilter':{},
             'columns': ['Title',
                         'Type',
                         'Brand',
                         'Model',
                         'ExpiryDate',
                         'WeeksToExpire',
                         'Method']},
            ]

    def folderitems(self):
        items = BikaListingView.folderitems(self)
        for x in range(len(items)):
            if not items[x].has_key('obj'): continue
            obj = items[x]['obj']

            itype = obj.getInstrumentType()
            items[x]['Type'] = itype.Title() if itype else ''
            ibrand = obj.getManufacturer()
            items[x]['Brand'] = ibrand.Title() if ibrand else ''
            items[x]['Model'] = obj.getModel()

            data = obj.getCertificateExpireDate()
            if data == '':
                items[x]['ExpiryDate'] = "No date avaliable"
            else:
                items[x]['ExpiryDate'] = data.asdatetime().strftime(self.date_format_short)
                
            if obj.isOutOfDate():
                items[x]['WeeksToExpire'] = "Out of date"
            else:
                date = int(str(obj.getWeeksToExpire()).split(',')[0].split(' ')[0])
                weeks,days = divmod(date,7)
                items[x]['WeeksToExpire'] = str(weeks)+" weeks"+" "+str(days)+" days"
                
            if obj.getMethod():
                items[x]['Method'] = obj.getMethod().Title() 
                items[x]['replace']['Method'] = "<a href='%s'>%s</a>" % \
                    (obj.getMethod().absolute_url(), items[x]['Method'])
            else:
                items[x]['Method'] = ''
            items[x]['replace']['Title'] = "<a href='%s'>%s</a>" % \
                (items[x]['url'], items[x]['Title'])

        return items

schema = ATFolderSchema.copy()
class Instruments(ATFolder):
    implements(IInstruments)
    displayContentsTab = False
    schema = schema

schemata.finalizeATCTSchema(schema, folderish = True, moveDiscussion = False)
atapi.registerType(Instruments, PROJECTNAME)
