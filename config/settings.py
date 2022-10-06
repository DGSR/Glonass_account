BASE_URL = 'https://nav.tspb.su/api/'

AUTH_URL = 'auth/login'
AUTH_CHECK_URL = 'v3/auth/check'
AUTH_LOGOUT_URL = 'auth/logout'

CLIENTS_FIND_URL = 'v3/agents'
CLIENTS_BASE_URL = 'agents/'

USERS_BASE_URL = 'users/'
USERS_FIND_URL = 'v3/users/find'

VEHICLE_MODEL_BASE_URL = 'models/'

VEHICLE_BASE_URL = 'vehicles/'
VEHICLE_FIND_URL = 'v3/vehicles/find'
VEHICLE_GET_COUNTER_URL = 'vehiclecounters/getvehiclecounters/'
VEHICLE_PUT_COUNTER_URL = 'vehiclecounters/putvehiclecounters/'

SENSORS_BASE_URL = 'vehicles/%s/sensors'
SENSORS_TYPES = 'v3/sensors/types'

COMMANDS_GET_URL = 'CommandsTemplate/'
COMMANDS_PUT_URL = 'CommandsTemplates/put'
COMMANDS_DELETE_URL = 'commandstemplates/delete'

MESSAGES_BASE_URL = 'messages/'
MESSAGES_FOR_VEHICLE = 'load/'

TEMPLATES_BASE_URL = 'templates/'

GEO_OBJECT_BASE_URL = 'gis/'
GEO_OBJECT_WKT_INFO = 'gis/getwktwithinfo'
GEO_OBJECT_DELETE = 'gis/deleteByIds'

REPORTS_LIST_URL = 'reports/listtree'
EXPORT_USER_REPORT_URL = 'reports/exportUserReport'

INSPECTIONS_TASKS_BASE_URL = 'vehicleinspectiontasks/getbyvehicle/'

HEADERS = {'Content-Type': 'application/json',
           'Referer': 'https://nav.tspb.su/admin.html',
           'X-Auth': ''}
