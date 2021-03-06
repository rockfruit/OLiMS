from lims.utils import isActive
from dependencies.dependency import ClassSecurityInfo
from dependencies.dependency import schemata
from dependencies import atapi
from dependencies.dependency import registerType
from dependencies.dependency import getToolByName
from lims.browser.bika_listing import BikaListingView
from lims.config import PROJECTNAME
from lims import bikaMessageFactory as _
from lims.utils import t
from lims.content.bikaschema import BikaFolderSchema
from dependencies.dependency import IFolderContentsView
from dependencies.folder import ATFolder, ATFolderSchema
from dependencies.dependency import IViewView
from lims.interfaces import IARTemplates
from dependencies.dependency import implements

class TemplatesView(BikaListingView):
    implements(IFolderContentsView, IViewView)
    def __init__(self, context, request):
        super(TemplatesView, self).__init__(context, request)
        self.catalog = "bika_setup_catalog"
        self.contentFilter = {
            'portal_type': 'ARTemplate',
            'sort_order': 'sortable_title',
            'path': {
                "query": "/".join(self.context.getPhysicalPath()),
                "level" : 0 },
        }
        self.show_sort_column = False
        self.show_select_row = False
        self.show_select_column = True
        self.icon = self.portal_url + "/++resource++bika.lims.images/artemplate_big.png"
        self.title = self.context.translate(_("AR Templates"))
        self.description = ""
        self.context_actions = {_('Add Template'):
                                {'url': 'createObject?type_name=ARTemplate',
                                 'icon': '++resource++bika.lims.images/add.png'}}

        self.columns = {
            'Title': {'title': _('Template'),
                      'index': 'sortable_title'},
            'Description': {'title': _('Description'),
                            'index': 'description'},
        }

        self.review_states = [
            {'id':'default',
             'title': _('Active'),
             'contentFilter': {'inactive_state':'active'},
             'columns': ['Title',
                         'Description']},
            {'id':'inactive',
             'title': _('Dormant'),
             'contentFilter': {'inactive_state':'inactive'},
             'columns': ['Title',
                         'Description']},
            {'id':'all',
             'title': _('All'),
             'contentFilter':{},
             'columns': ['Title',
                         'Description']},
        ]

    def folderitems(self):
        items = BikaListingView.folderitems(self)
        for x in range(len(items)):
            if not items[x].has_key('obj'): continue
            obj = items[x]['obj']
            items[x]['Title'] = obj.Title()
            items[x]['replace']['Title'] = "<a href='%s'>%s</a>" % \
                 (items[x]['url'], items[x]['title'])
        return items

schema = ATFolderSchema.copy()
class ARTemplates(ATFolder):
    implements(IARTemplates)
    displayContentsTab = False
    schema = schema

schemata.finalizeATCTSchema(schema, folderish = True, moveDiscussion = False)
atapi.registerType(ARTemplates, PROJECTNAME)
