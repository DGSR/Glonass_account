from marshmallow import Schema, fields, EXCLUDE


class GradeTablesSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    relevanceTime = fields.Str(allow_none=True)
    grades = fields.List(fields.Dict, allow_none=True)
    updateUserName = fields.Str(allow_none=True)
    updateTime = fields.Str(allow_none=True)

    id = fields.String(allow_none=True, load_default='0')  # If base class id is fixed, remove


class SensorSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True)
    sensorTypeId = fields.Int(required=True)
    kind = fields.Int(required=True)
    inputType = fields.Int(required=True)
    owner = fields.Str(allow_none=True)
    vehicleId = fields.Str(allow_none=True)

    custom = fields.Dict(fields.Raw, allow_none=True)
    gradesTables = fields.List(fields.Raw, allow_none=True)
    summaryMaxValue = fields.Float(allow_none=True)
    agrFunction = fields.Int(allow_none=True)
    gradeType = fields.Int(allow_none=True)
    disabled = fields.Bool(allow_none=True)
    isDeleted = fields.Bool(allow_none=True)
    showTooltip = fields.Bool(allow_none=True, load_default=False)
    showAsDutOnGraph = fields.Bool(allow_none=True)
    showLastValid = fields.Bool(allow_none=True)
    showWithoutIgn = fields.Bool(allow_none=True)
    childrenIds = fields.Str(allow_none=True)
    medianDegree = fields.Str(allow_none=True)
    ref = fields.Str(allow_none=True)
    inputNumber = fields.Int(allow_none=True)
    normalState = fields.Bool(allow_none=True)
    parentId = fields.Str(allow_none=True)
    expression = fields.Str(allow_none=True)
    id = fields.Str(allow_none=True)
    created = fields.Str(allow_none=True)
    updated = fields.Str(allow_none=True)
    extId = fields.Str(allow_none=True)
    color = fields.Str(allow_none=True)

